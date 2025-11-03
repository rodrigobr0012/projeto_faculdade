from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorCollection

from ..database.connection import get_cars_collection
from ..models.car_model import CarCreate, CarResponse

router = APIRouter(prefix="/cars", tags=["Cars"])


def _serialize_car(document: dict) -> CarResponse:
    identifier = document.get("id") or document.get("_id")
    return CarResponse(
        id=str(identifier),
        modelo=document.get("modelo", ""),
        marca=document.get("marca", ""),
        ano=document.get("ano"),
        preco=float(document.get("preco", 0)),
        imagem=document.get("imagem"),
        descricao=document.get("descricao"),
    )


def _build_id_filter(car_id: str) -> dict:
    filters = [{"id": car_id}]
    if ObjectId.is_valid(car_id):
        filters.append({"_id": ObjectId(car_id)})
    else:
        filters.append({"_id": car_id})
    return {"$or": filters}


@router.get("/", response_model=List[CarResponse])
async def list_cars(
    cars_collection: AsyncIOMotorCollection = Depends(get_cars_collection),
):
    cars_cursor = cars_collection.find()
    cars = [
        _serialize_car(car)
        async for car in cars_cursor
    ]
    return cars


@router.get("/{car_id}", response_model=CarResponse)
async def get_car(
    car_id: str,
    cars_collection: AsyncIOMotorCollection = Depends(get_cars_collection),
):
    car = await cars_collection.find_one(_build_id_filter(car_id))
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado")
    return _serialize_car(car)


@router.get("/search", response_model=List[CarResponse])
async def search_cars(
    query: str = Query(..., description="Busca por modelo ou marca"),
    cars_collection: AsyncIOMotorCollection = Depends(get_cars_collection),
):
    regex_query = {"$regex": query, "$options": "i"}
    cars_cursor = cars_collection.find({"$or": [{"modelo": regex_query}, {"marca": regex_query}]})
    cars = [
        _serialize_car(car)
        async for car in cars_cursor
    ]
    return cars


@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
async def create_car(
    car: CarCreate,
    cars_collection: AsyncIOMotorCollection = Depends(get_cars_collection),
):
    car_dict = car.dict(exclude_unset=True)
    if car_dict.get("id"):
        car_dict["_id"] = car_dict["id"]
    result = await cars_collection.insert_one(car_dict)

    if not car_dict.get("id"):
        generated_id = str(result.inserted_id)
        await cars_collection.update_one({"_id": result.inserted_id}, {"$set": {"id": generated_id}})

    created_car = await cars_collection.find_one({"_id": result.inserted_id})
    return _serialize_car(created_car)

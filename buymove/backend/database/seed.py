import asyncio
import json
from pathlib import Path
from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection

from .connection import get_database

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "cars.json"


def load_seed_data() -> List[dict]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


async def seed_database() -> None:
    collection = get_database()["cars"]
    await _seed_collection(collection)


async def _seed_collection(collection: AsyncIOMotorCollection) -> None:
    existing = await collection.count_documents({})
    if existing:
        return

    cars = load_seed_data()
    for car in cars:
        if car.get("id"):
            car["_id"] = car["id"]
    if cars:
        await collection.insert_many(cars)


if __name__ == "__main__":
    asyncio.run(seed_database())

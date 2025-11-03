from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class CarBase(BaseModel):
    modelo: str = Field(..., description="Modelo do carro")
    marca: str = Field(..., description="Marca do carro")
    ano: int = Field(..., ge=1900, description="Ano de fabricação")
    preco: float = Field(..., ge=0, description="Preço do carro")
    imagem: HttpUrl | None = Field(None, description="URL da imagem do carro")
    descricao: Optional[str] = Field(None, description="Descrição do carro")


class CarCreate(CarBase):
    id: Optional[str] = Field(None, description="Identificador opcional do carro")


class CarResponse(CarBase):
    id: str = Field(..., description="Identificador do carro")

    class Config:
        orm_mode = True

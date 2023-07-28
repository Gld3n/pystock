from pydantic import BaseModel
from enum import Enum


class Category(Enum):
    FOOD = "food"
    TOOL = "tool"
    FURNITURE = "furniture"


class Product(BaseModel):
    name: str
    price: float
    quantity: int | None = None
    discount: int | None = None
    category: Category | None = None

    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Koka Soda",
                    "price": 1.5,
                    "discount": 0,
                    "quantity": 10,
                    "category": "food",
                }
            ]
        }

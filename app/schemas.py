from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float
    quantity: int | None = None
    discount: int | None = None

    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Koka Soda",
                    "price": 1.5,
                    "discount": 0,
                    "quantity": 10,
                }
            ]
        }

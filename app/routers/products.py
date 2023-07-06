from typing import Annotated, Any
from app.schemas import Product
from app.database import db

from fastapi import APIRouter, Body

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=Product,
    status_code=201,
    summary="Add a new product",
    response_model_exclude_unset=True,
)
def add_products(
    product: Annotated[
        Product,
        Body(
            embed=True,
            title="Product",
            description="Product structure expected",
        ),
    ]
) -> Any:
    db.append(product.dict(exclude_unset=True))
    return product


@router.put("/")
def modify_products():
    return {"message": "Modify products"}


@router.get(
    "/", status_code=200, summary="List all products", response_model=list[Product]
)
def list_products() -> Any:
    return db


@router.get("/statistics")
def show_statistics():
    return {"message": "Statistics"}

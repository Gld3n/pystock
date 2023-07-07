from utils import check_discount, check_name, check_price, check_quantity
from database import db
from schemas import Product


def add_products() -> None:
    print(
        """
    === Add Product ======================
        
    Fill in the following information:
    """
    )
    name: str = check_name()
    price: float = check_price()
    discount: float = check_discount()
    quantity: float = check_quantity()

    db.append(Product(name, price, discount, quantity))


def modify_products():
    return {"message": "Modify products"}


def list_products():
    return {"message": "List products"}


def show_statistics():
    return {"message": "Statistics"}


def modify_settings():
    return {"message": "Modify settings"}

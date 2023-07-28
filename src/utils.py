from os import system, name as os_name
from re import match

from database import db
from src.schemas import Product


def wait() -> None:
    """Wait for the user to press enter to continue."""

    input("\n[Press enter to continue...]")
    system("cls" if os_name == "nt" else "clear")


def clear_scr():
    system("cls" if os_name == "nt" else "clear")


def sanitize_product_selection() -> Product:
    try:
        index: int = int(input("Option: "))
        if index < 0:
            raise IndexError

        product: Product = db[index]
        return product
    except IndexError:
        print("[Invalid index.]")
        return sanitize_product_selection()
    except ValueError:
        print("[Invalid value.]")
        return sanitize_product_selection()


def set_name() -> str:
    """Set the name of the product sanitizing the input."""

    while True:
        name: str = input("> Name: ").strip()
        if match(r"^[a-zA-Z ]+$", name):
            return name
        else:
            print("[Invalid name. Try again.]")


def set_price() -> float:
    """Set the price of the product sanitizing the input."""

    while True:
        try:
            price: float = float(input("> Price: "))
            break
        except ValueError:
            print("[Invalid price. Try again.]")
    if price <= 0:
        print("[Price cannot be negative.]")
        set_price()
    return price


def set_discount() -> int:
    """Set the discount of the product sanitizing the input."""

    while True:
        try:
            discount: int = int(input("> Discount: "))
            break
        except ValueError:
            print("[Invalid discount. Try again.]")
    if discount < 0 or discount > 100:
        print("[Discount must be between 0 and 100%]")
        return set_discount()

    return discount


def set_quantity() -> int:
    """Set the quantity of the product sanitizing the input."""

    while True:
        try:
            quantity: int = int(input("> Quantity: "))
            break
        except ValueError:
            print("[Invalid quantity. Try again.]")
    if quantity <= 0:
        print("[Quantity cannot be negative nor zero.]")
        set_quantity()

    return quantity


def calculate_net_total(iva: float) -> float:
    """Calculate the net total of the products."""

    discounted = sum(
        [(prod.price * (1 - (prod.discount / 100))) * prod.quantity for prod in db]
    )
    net = discounted + (discounted * iva)
    return net


def in_BsS(price: float, exchange_rate: float) -> str:
    """Calculate the price in BsS."""

    return f"{(price * exchange_rate):.2f}"

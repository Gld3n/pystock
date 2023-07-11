from os import system, name as os_name
from textwrap import dedent

from utils import (
    calculate_net_total,
    in_BsS,
    set_discount,
    set_name,
    set_price,
    set_quantity,
)
from schemas import Product
from database import db
from utils import wait

iva: float = 0.16  # Taxes (16%)
exchange_rate: float = 28.02  # USD 1.00 = BsS 28.02


def add_products() -> None:
    print("=== Add Product =====================")
    print("Fill in the following information:")

    name: str = set_name()
    price: float = set_price()
    discount: int = set_discount()
    quantity: int = set_quantity()
    product: dict = {
        "name": name,
        "price": price,
        "discount": discount,
        "quantity": quantity,
    }
    db.append(Product(**product))


def modify_products():
    print("=== Modify Product ==================")

    if len(db) == 0:
        print("No products found")
        return

    print("* Select a product to modify:")
    for prod in db:
        print(f"- Index [{db.index(prod)}] - Name: {prod.name}")

    def sanitize() -> int:
        try:
            index: int = int(input("Option: "))
            if index < 0:
                raise IndexError
            return index
        except IndexError:
            print("[Invalid index.]")
            sanitize()
        except ValueError:
            print("[Invalid value.]")
            sanitize()

    current_product: Product = db[sanitize()]
    print(current_product)
    wait()

    print("=== Modify Product ==================")
    print("* Select a field to modify:", end="")

    option_str: str = dedent(
        """
        1. Name
        2. Price
        3. Discount
        4. Quantity
        5. Back
        Select an option: """
    )
    option: str = input(option_str)
    match option:
        case "1":
            print(f"Current name: {current_product.name}")
            new_name: str = set_name()
            current_product.name = new_name
        case "2":
            print(f"Current price: {current_product.price}")
            new_price: float = set_price()
            current_product.price = new_price
        case "3":
            print(f"Current discount: {current_product.discount}")
            new_discount: int = set_discount()
            current_product.discount = new_discount
        case "4":
            print(f"Current quantity: {current_product.quantity}")
            new_quantity: int = set_quantity()
            current_product.quantity = new_quantity
        case "5":
            print("[Exiting...]")
        case _:
            print("[Invalid option.]")


def list_products():
    print("=== List Products ===================")

    if len(db) == 0:
        print("[No products found.]")
        return

    for product in db:
        price = product.price
        price_with_discount = price - (price * product.discount / 100)
        print(f"Index [{db.index(product)}]")
        print(f" - Name: {product.name}")
        print(f" - Price: {price:.2f}$ | BsS.{in_BsS(price, exchange_rate)}")
        print(
            f" - Price with discount ({product.discount}%): {( pwd := price_with_discount):.2f}$ | BsS.{in_BsS(pwd, exchange_rate)}"
        )
        print(f" - Quantity: {product.quantity} units")
        print("------------------------------------")


def show_statistics():
    print("=== Statistics ======================")
    if len(db) == 0:
        print("[No products found.]")
        return

    cheapest: Product = min(db, key=lambda product: product.price)
    most_expensive: Product = max(db, key=lambda product: product.price)
    largest_quantity: Product = max(db, key=lambda product: product.quantity)
    smaller_quantity: Product = min(db, key=lambda product: product.quantity)
    discounted_products: list[Product] = list(
        filter(lambda product: product.discount > 0, db)
    )
    print(f" - Total products: {len(db)}")
    print(f" - Products at discount: {len(discounted_products)}")
    print(
        f" - Gross total in stock: {(total := sum([(product.price * product.quantity) for product in db])):.2f}$ | BsS.{in_BsS(total, exchange_rate)}"
    )
    print(
        f" - Net total in stock: {(net := calculate_net_total(iva=iva)):.2f}$ | BsS.{in_BsS(net, exchange_rate)}"
    )
    print(
        f" - Cheapest product: {cheapest.name} ({(ch := cheapest.price):.2f}$) | BsS.{in_BsS(ch, exchange_rate)}"
    )
    print(
        f" - Most expensive product: {most_expensive.name} ({(me := most_expensive.price):.2f}$) | BsS.{in_BsS(me, exchange_rate)}"
    )
    print(
        f" - Largest quantity: {largest_quantity.name} ({largest_quantity.quantity} units)"
    )
    print(
        f" - Smallest quantity: {smaller_quantity.name} ({smaller_quantity.quantity} units)"
    )


def modify_settings():
    global iva, exchange_rate

    print("=== Settings ========================", end="")
    option_str: str = dedent(
        f"""
    1. Modify iva (current: {iva*100:.0f}%)
    2. Modify exchange rate (current: BsS.{exchange_rate})
    3. <= Back
    Select an option: """
    )

    option = input(option_str)
    match option:
        case "1":
            print(f"Current IVA: ({iva*100:.0f}%)")
            new_iva: float = float(input("New IVA (as decimal): "))
            iva = new_iva
        case "2":
            print(f"Current exchange rate: (BsS.{exchange_rate})")
            new_er: float = float(input("New exchange rate: "))
            exchange_rate = new_er
        case "3":
            print("[Exiting...]")
        case _:
            print("[Invalid option.]")


def main():
    system("cls" if os_name == "nt" else "clear")
    flag: bool = True
    option_str: str = dedent(
        """
        1. Add product
        2. Modify product
        3. List products
        4. Show statistics
        5. Settings
        6. Exit
        Select an option: """
    )

    while flag:
        print("=== Main Menu =======================", end="")
        option: str = input(option_str)
        system("cls" if os_name == "nt" else "clear")
        match option:
            case "1":
                add_products()
                wait()
            case "2":
                modify_products()
                wait()
            case "3":
                list_products()
                wait()
            case "4":
                show_statistics()
                wait()
            case "5":
                modify_settings()
                wait()
            case "6":
                print("Bye!")
                flag = False
            case _:
                print("[Invalid option. Try again.]")
                wait()


if __name__ == "__main__":
    main()

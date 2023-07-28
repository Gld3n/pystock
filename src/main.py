"""
TODO: Add more intensive validation for pending inputs.
TODO: Make IVA unmodifiable.
TODO: Base exchange rate on a real-time API.
"""
from textwrap import dedent

from src.schemas import Product
from database import db
import utils

iva: float = 0.16  # Taxes (16%)
exchange_rate: float = 28.02  # USD 1.00 = BsS 28.02


def add_products() -> None:
    print("=== Add Product =====================")
    print("Fill in the following information:")

    name: str = utils.set_name()
    price: float = utils.set_price()
    discount: int = utils.set_discount()
    quantity: int = utils.set_quantity()
    product: dict = {
        "name": name,
        "price": price,
        "discount": discount,
        "quantity": quantity,
    }
    db.append(Product(**product))


def modify_products() -> None:
    print("=== Modify Product ==================")

    if len(db) == 0:
        print("[No products found]")
        return

    print("* Select a product to modify:")
    for idx, prod in enumerate(db):
        print(f"- Index [{idx}] - Name: {prod.name}")

    current_product: Product = utils.sanitize_selection()
    utils.wait()

    print("=== Modify Product ==================")
    print("* Select a field to modify:", end="")

    option_str: str = dedent(
        f"""
        1. Name (Current: {current_product.name})
        2. Price (Current: {current_product.price}$ | BsS.{utils.in_BsS(current_product.price, exchange_rate)})
        3. Discount (Current: {current_product.discount}%)
        4. Quantity (Current: {current_product.quantity} units)
        5. <= Back
        Select an option: """
    )
    option: str = input(option_str)
    match option:
        case "1":
            new_name: str = utils.set_name()
            current_product.name = new_name
        case "2":
            new_price: float = utils.set_price()
            current_product.price = new_price
        case "3":
            new_discount: int = utils.set_discount()
            current_product.discount = new_discount
        case "4":
            new_quantity: int = utils.set_quantity()
            current_product.quantity = new_quantity
        case "5":
            print("[Exiting...]")
        case _:
            print("[Invalid option]")


def list_products() -> None:
    print("=== List Products ===================")

    if len(db) == 0:
        print("[No products found]")
        return

    for idx, prod in enumerate(db):
        price = prod.price
        price_with_discount = price - (price * prod.discount / 100)
        print(f"Index [{idx}]")
        print(f" - Name: {prod.name}")
        print(f" - Price: {price:.2f}$ | BsS.{utils.in_BsS(price, exchange_rate)}")
        print(
            f" - Price with discount ({prod.discount}%): {( pwd := price_with_discount):.2f}$ | BsS.{utils.in_BsS(pwd, exchange_rate)}"
        )
        print(f" - Quantity: {prod.quantity} units")
        print("------------------------------------")


def show_statistics() -> None:
    print("=== Statistics ======================")
    if len(db) == 0:
        print("[No products found]")
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
        f" - Gross total in stock: {(total := sum([(product.price * product.quantity) for product in db])):.2f}$ | BsS.{utils.in_BsS(total, exchange_rate)}"
    )
    print(
        f" - Net total in stock: {(net := utils.calculate_net_total(iva)):.2f}$ | BsS.{utils.in_BsS(net, exchange_rate)}"
    )
    print(
        f" - Cheapest product: {cheapest.name} ({(ch := cheapest.price):.2f}$) | BsS.{utils.in_BsS(ch, exchange_rate)}"
    )
    print(
        f" - Most expensive product: {most_expensive.name} ({(me := most_expensive.price):.2f}$) | BsS.{utils.in_BsS(me, exchange_rate)}"
    )
    print(
        f" - Largest quantity: {largest_quantity.name} ({largest_quantity.quantity} units)"
    )
    print(
        f" - Smallest quantity: {smaller_quantity.name} ({smaller_quantity.quantity} units)"
    )


def delete_product() -> None:
    print("=== Delete Product ==================")

    if len(db) < 1:
        print("[No products found]")
        return

    for idx, prod in enumerate(db):
        print(f"Index [{idx}] - {prod.name.title()}")

    product: Product = utils.sanitize_product_selection()

    slc: str = input(
        f"Are you sure you want to delete the selected product?\n - {product.name} [y/n]: "
    )
    while True:
        match slc:
            case "y":
                db.remove(product)
                print("[Product removed successfully]")
                break
            case "n":
                print("[Exiting...]")
                break
            case _:
                print("[Invalid option. Try again]: ")


def modify_settings() -> None:
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
            new_iva: float = float(input("New IVA: "))
            while new_iva < 0 or new_iva > 100:
                new_iva = float(input("[Invalid IVA. Try again]"))
            iva = new_iva
        case "2":
            print(f"Current exchange rate: (BsS.{exchange_rate})")
            new_er: float = float(input("New exchange rate: "))
            exchange_rate = new_er
        case "3":
            print("[Exiting...]")
        case _:
            print("[Invalid option]")


def main():
    utils.clear_scr()
    flag: bool = True
    option_str: str = dedent(
        """
        1. Add product
        2. Modify product
        3. List products
        4. Show statistics
        5. Delete product
        6. Settings
        7. Exit
        Select an option: """
    )

    while flag:
        print("=== Main Menu =======================", end="")
        option: str = input(option_str)
        utils.clear_scr()
        match option:
            case "1":
                add_products()
                utils.wait()
            case "2":
                modify_products()
                utils.wait()
            case "3":
                list_products()
                utils.wait()
            case "4":
                show_statistics()
                utils.wait()
            case "5":
                delete_product()
                utils.wait()
            case "6":
                modify_settings()
                utils.wait()
            case "7":
                print("Bye!")
                flag = False
            case _:
                print("[Invalid option. Try again]")
                utils.wait()


if __name__ == "__main__":
    main()

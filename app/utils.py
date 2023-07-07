def check_name():
    name: str = input("> Name: ")
    while not name.isalpha():
        print("[Invalid name. Try again.]")
        check_name()


def check_price():
    while True:
        try:
            price: float = float(input("> Price: "))
            break
        except ValueError:
            print("[Invalid price. Try again.]")
    if price <= 0:
        print("[Price cannot be negative.]")
        check_price()
    return price


def check_discount():
    while True:
        try:
            discount: float = float(input("> Discount: "))
            break
        except ValueError:
            print("[Invalid discount. Try again.]")
    if discount < 0 or discount > 100:
        print("[Discount must be between 0 and 100%]")
        check_discount()

    return discount


def check_quantity():
    while True:
        try:
            quantity: int = int(input("> Quantity: "))
            break
        except ValueError:
            print("[Invalid quantity. Try again.]")
    if quantity <= 0:
        print("[Quantity cannot be negative nor zero.]")
        check_quantity()

    return quantity

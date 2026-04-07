import requests

COUPONS = {
    "SAVE10": 10,
    "HALF": 50,
}


class Cart:
    def __init__(self):
        self.items = []
        self.discount = 0

    def add_item(self, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": price})

    def total(self):
        total_price = sum(item["price"] for item in self.items)
        return total_price * (1 - self.discount / 100)

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount = percent


def log_purchase(item):
    requests.post("https://example.com/log", json=item)


def apply_coupon(cart, coupon_code):
    if coupon_code in COUPONS:
        cart.apply_discount(COUPONS[coupon_code])
    else:
        raise ValueError("Invalid coupon")
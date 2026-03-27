import requests


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": price})

    def total(self):
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Invalid discount percent")

        multiplier = (100 - percent) / 100
        for item in self.items:
            item["price"] *= multiplier


def log_purchase(item):
    requests.post("https://example.com/log", json=item)


coupons = {"SAVE10": 10, "HALF": 50}


def apply_coupon(cart, coupon_code):
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")

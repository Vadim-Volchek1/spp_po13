import requests

coupons = {"SAVE10": 10, "HALF": 50}

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: float):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": price})

    def total(self):
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percent: float):
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        for item in self.items:
            item["price"] *= (1 - percent / 100)

def log_purchase(item):
    requests.post("https://example.com/log", json=item, timeout=5)

def apply_coupon(cart, coupon_code):
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")

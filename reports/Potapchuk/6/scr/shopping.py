"""Module for shopping cart operations."""
import requests

class Cart:
    """A simple shopping cart class."""
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        """Add an item to the cart."""
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": price})

    def total(self):
        """Return total price of items in cart."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percentage):
        """Apply discount percentage to all items."""
        if not 0 <= percentage <= 100:
            raise ValueError("Invalid discount percentage")
        for item in self.items:
            item["price"] *= (1 - percentage / 100)

def log_purchase(item):
    """Log purchase to an external service."""
    response = requests.post("https://example.com/log", json=item, timeout=5)
    return response.status_code

def apply_coupon(cart, coupon_code):
    """Apply a coupon code to the cart."""
    coupons = {"SAVE10": 10, "HALF": 50}
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")

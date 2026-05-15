# pylint: disable=redefined-outer-name
from unittest.mock import patch
import pytest
from shopping import Cart, log_purchase, apply_coupon

@pytest.fixture
def empty_cart():
    return Cart()

def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["name"] == "Apple"
    assert empty_cart.items[0]["price"] == 10.0

def test_add_item_negative_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("Banana", -5.0)

def test_total(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 5.0)
    assert empty_cart.total() == 15.0

@pytest.mark.parametrize("discount, expected_total", [
    (0, 15.0),
    (50, 7.5),
    (100, 0.0),
])
def test_apply_discount(discount, expected_total, empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 5.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected_total

@pytest.mark.parametrize("discount", [-10, 150])
def test_apply_discount_invalid(discount, empty_cart):
    empty_cart.add_item("Apple", 10.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(discount)

def test_log_purchase():
    item = {"name": "Apple", "price": 10.0}
    with patch("shopping.requests.post") as mock_post:
        log_purchase(item)
        mock_post.assert_called_once_with(
            "https://example.com/log", json=item, timeout=5
        )

def test_apply_coupon_valid(empty_cart, monkeypatch):
    empty_cart.add_item("Item", 100.0)
    monkeypatch.setitem(__import__('shopping').coupons, "TEST10", 10)

    apply_coupon(empty_cart, "TEST10")

    assert empty_cart.total() == 90.0

def test_apply_coupon_invalid(empty_cart, monkeypatch):
    empty_cart.add_item("Item", 100.0)
    monkeypatch.setitem(__import__('shopping').coupons, "TEST10", 10)

    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "BADCODE")

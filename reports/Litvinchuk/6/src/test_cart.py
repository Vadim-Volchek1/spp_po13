"""Tests for shopping cart functionality."""

from unittest.mock import patch

import pytest

from src.shopping import COUPONS, Cart, apply_coupon, log_purchase


@pytest.fixture(name="empty_cart")
def fixture_empty_cart():
    """Return an empty cart instance."""
    return Cart()


def test_add_item(empty_cart):
    """Test adding an item to the cart."""
    empty_cart.add_item("Apple", 10.0)

    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["name"] == "Apple"
    assert empty_cart.items[0]["price"] == 10.0


def test_add_item_negative_price(empty_cart):
    """Test that negative price raises ValueError."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        empty_cart.add_item("Apple", -10.0)


def test_total(empty_cart):
    """Test total price calculation."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 5.0)

    assert empty_cart.total() == 15.0


@pytest.mark.parametrize(
    ("discount", "expected_total"),
    [
        (0, 100.0),
        (50, 50.0),
        (100, 0.0),
    ],
)
def test_apply_discount_valid(empty_cart, discount, expected_total):
    """Test valid discount values."""
    empty_cart.add_item("Item", 100.0)
    empty_cart.apply_discount(discount)

    assert empty_cart.total() == expected_total


@pytest.mark.parametrize("discount", [-1, 101])
def test_apply_discount_invalid(empty_cart, discount):
    """Test invalid discount values."""
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        empty_cart.apply_discount(discount)


def test_log_purchase_calls_requests_post():
    """Test purchase logging request call."""
    item = {"name": "Apple", "price": 10.0}

    with patch("src.shopping.requests.post") as mocked_post:
        log_purchase(item)
        mocked_post.assert_called_once_with(
            "https://example.com/log",
            json=item,
            timeout=5,
        )


def test_apply_coupon_save10(empty_cart):
    """Test SAVE10 coupon."""
    empty_cart.add_item("Item", 100.0)

    apply_coupon(empty_cart, "SAVE10")

    assert empty_cart.total() == 90.0


def test_apply_coupon_half(empty_cart):
    """Test HALF coupon."""
    empty_cart.add_item("Item", 100.0)

    apply_coupon(empty_cart, "HALF")

    assert empty_cart.total() == 50.0


def test_apply_coupon_invalid(empty_cart):
    """Test invalid coupon handling."""
    empty_cart.add_item("Item", 100.0)

    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(empty_cart, "WRONG")


def test_apply_coupon_with_monkeypatch(empty_cart, monkeypatch):
    """Test coupon dictionary patching with monkeypatch."""
    empty_cart.add_item("Item", 200.0)
    monkeypatch.setitem(COUPONS, "SUPER", 25)

    apply_coupon(empty_cart, "SUPER")

    assert empty_cart.total() == 150.0

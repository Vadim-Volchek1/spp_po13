"""Tests for the shopping module."""
from unittest.mock import patch
import pytest
from shopping import Cart, log_purchase, apply_coupon

# pylint: disable=redefined-outer-name

@pytest.fixture
def empty_cart():
    """Fixture to provide an empty Cart instance."""
    return Cart()

def test_add_item(empty_cart):
    """Test adding an item to the cart."""
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["name"] == "Apple"

def test_negative_price(empty_cart):
    """Test exception for negative price."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        empty_cart.add_item("Banana", -5.0)

def test_total(empty_cart):
    """Test total price calculation."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Juice", 20.0)
    assert empty_cart.total() == 30.0

@pytest.mark.parametrize("discount, expected_total", [
    (0, 100.0),
    (50, 50.0),
    (100, 0.0),
])
def test_apply_discount_valid(empty_cart, discount, expected_total):
    """Test valid discount applications."""
    empty_cart.add_item("Gadget", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected_total

@pytest.mark.parametrize("discount", [-10, 110])
def test_apply_discount_invalid(empty_cart, discount):
    """Test invalid discount values."""
    empty_cart.add_item("Gadget", 100.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(discount)

def test_log_purchase_mock():
    """Test logging purchase with a mock."""
    with patch('requests.post') as mocked_post:
        item = {"name": "Apple", "price": 10.0}
        log_purchase(item)
        mocked_post.assert_called_once_with("https://example.com/log", json=item)

def test_apply_coupon_success(empty_cart):
    """Test successful coupon application."""
    empty_cart.add_item("Laptop", 1000.0)
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == 900.0

def test_apply_coupon_mocked(empty_cart):
    """Test invalid coupon application."""
    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "NON_EXISTENT")

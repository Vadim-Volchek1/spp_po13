# pylint: disable=redefined-outer-name
from unittest.mock import patch
import pytest
from shopping import Cart, log_purchase, apply_coupon

# Фикстура
@pytest.fixture
def empty_cart():
    return Cart()

# Тесты корзины
def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1


def test_add_item_negative_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("Apple", -5.0)


def test_total(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 5.0)
    assert empty_cart.total() == 15.0

# Тесты apply_discount
@pytest.mark.parametrize(
    "discount, expected_total",
    [
        (0, 100.0),
        (50, 50.0),
        (100, 0.0),
    ]
)
def test_apply_discount_valid(empty_cart, discount, expected_total):
    empty_cart.add_item("Item", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected_total


@pytest.mark.parametrize("discount", [-10, 150])
def test_apply_discount_invalid(empty_cart, discount):
    empty_cart.add_item("Item", 100.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(discount)


# Тесты log_purchase
@patch("shopping.requests.post")
def test_log_purchase(mock_post):
    item = {"name": "Apple", "price": 10.0}

    log_purchase(item)

    mock_post.assert_called_once_with(
        "https://example.com/log",
        json=item
    )

# Тесты apply_coupon
def test_apply_coupon_valid(empty_cart, monkeypatch):
    empty_cart.add_item("Item", 100.0)

    fake_coupons = {"SAVE10": 10}
    monkeypatch.setattr("shopping.coupons", fake_coupons, raising=False)

    apply_coupon(empty_cart, "SAVE10")

    assert empty_cart.total() == 90.0


def test_apply_coupon_invalid(empty_cart, monkeypatch):
    empty_cart.add_item("Item", 100.0)

    fake_coupons = {"SAVE10": 10}
    monkeypatch.setattr("shopping.coupons", fake_coupons, raising=False)

    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "BADCODE")

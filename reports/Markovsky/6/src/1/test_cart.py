# pylint: disable=redefined-outer-name
from unittest.mock import patch, MagicMock
import pytest

import requests

from shopping import Cart, log_purchase, apply_coupon


# 3
@pytest.fixture
def empty_cart():
    return Cart()


@pytest.fixture
def cart_with_items():
    cart = Cart()
    cart.add_item("Apple", 100.0)
    cart.add_item("Banana", 200.0)
    cart.add_item("Orange", 300.0)
    return cart


# 1
def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["name"] == "Apple"
    assert empty_cart.items[0]["price"] == 10.0


def test_negative_price(empty_cart):
    with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
        empty_cart.add_item("Apple", -10.0)


def test_total(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
    empty_cart.add_item("Orange", 30.0)

    assert empty_cart.total() == 60.0


# 2
@pytest.mark.parametrize("discount, expected_prices", [
    (0, [10.0, 20.0, 30.0]),
    (50, [5.0, 10.0, 15.0]),
    (100, [0.0, 0.0, 0.0]),
])
def test_apply_discount_valid(empty_cart, discount, expected_prices):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
    empty_cart.add_item("Orange", 30.0)

    empty_cart.apply_discount(discount)

    for i, expected_price in enumerate(expected_prices):
        assert empty_cart.items[i]["price"] == expected_price

    assert empty_cart.total() == sum(expected_prices)


@pytest.mark.parametrize("invalid_discount", [-10, -1, 101, 150])
def test_apply_discount_invalid(empty_cart, invalid_discount):
    empty_cart.add_item("Apple", 10.0)
    with pytest.raises(ValueError, match="Скидка должна быть от 0 до 100 процентов"):
        empty_cart.apply_discount(invalid_discount)


def test_empty_cart_total(empty_cart):
    assert empty_cart.total() == 0.0


def test_multiple_discounts(empty_cart):
    empty_cart.add_item("Apple", 100.0)

    empty_cart.apply_discount(20)
    assert empty_cart.items[0]["price"] == 80.0

    empty_cart.apply_discount(10)
    assert empty_cart.items[0]["price"] == 72.0


def test_add_item_after_discount(empty_cart):
    empty_cart.add_item("Apple", 100.0)
    empty_cart.apply_discount(20)

    empty_cart.add_item("Banana", 50.0)

    assert empty_cart.items[0]["price"] == 80.0
    assert empty_cart.items[1]["price"] == 50.0
    assert empty_cart.total() == 130.0


# 4
@patch('shopping.requests.post')
def test_log_purchase_success(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    item = {"name": "Apple", "price": 10.0}
    result = log_purchase(item)

    mock_post.assert_called_once_with(
        "https://example.com/log",
        json=item,
        timeout=30
    )

    mock_response.raise_for_status.assert_called_once()

    assert result == mock_response


@patch('shopping.requests.post')
def test_log_purchase_with_multiple_items(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    cart = Cart()
    cart.add_item("Apple", 10.0)
    cart.add_item("Banana", 20.0)
    cart.add_item("Orange", 30.0)

    for item in cart.items:
        log_purchase(item)

    assert mock_post.call_count == 3

    expected_calls = [
        (("https://example.com/log",), {"json": {"name": "Apple", "price": 10.0}, "timeout": 30}),
        (("https://example.com/log",), {"json": {"name": "Banana", "price": 20.0}, "timeout": 30}),
        (("https://example.com/log",), {"json": {"name": "Orange", "price": 30.0}, "timeout": 30})
    ]

    for i, call in enumerate(mock_post.call_args_list):
        assert call[0] == expected_calls[i][0]  # args
        assert call[1] == expected_calls[i][1]  # kwargs


@patch('shopping.requests.post')
def test_log_purchase_with_empty_item(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    item = {}
    result = log_purchase(item)

    mock_post.assert_called_once_with(
        "https://example.com/log",
        json={},
        timeout=30
    )
    assert result == mock_response


@patch('shopping.requests.post')
def test_log_purchase_with_http_error(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_post.return_value = mock_response

    item = {"name": "Apple", "price": 10.0}

    with pytest.raises(requests.exceptions.HTTPError, match="404 Not Found"):
        log_purchase(item)

    mock_post.assert_called_once_with(
        "https://example.com/log",
        json=item,
        timeout=30
    )


@patch('shopping.requests.post')
def test_log_purchase_integration_with_cart(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    cart = Cart()
    cart.add_item("Apple", 10.0)
    cart.add_item("Banana", 20.0)

    cart.apply_discount(50)

    for item in cart.items:
        log_purchase(item)

    expected_items = [
        {"name": "Apple", "price": 5.0},
        {"name": "Banana", "price": 10.0}
    ]

    for i, call in enumerate(mock_post.call_args_list):
        assert call[1]["json"] == expected_items[i]


# 5
def test_apply_valid_coupon_save10(cart_with_items):
    original_total = cart_with_items.total()
    apply_coupon(cart_with_items, "SAVE10")
    assert cart_with_items.total() == original_total * 0.9


def test_apply_valid_coupon_half(cart_with_items):
    original_total = cart_with_items.total()
    apply_coupon(cart_with_items, "HALF")
    assert cart_with_items.total() == original_total * 0.5


def test_apply_invalid_coupon(cart_with_items):
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart_with_items, "INVALID")


def test_apply_coupon_to_empty_cart(empty_cart):
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == 0.0


def test_apply_coupon_with_mocked_dict_patch(cart_with_items):
    with patch.dict('shopping.COUPONS', {'TEST50': 50}, clear=True):
        apply_coupon(cart_with_items, "TEST50")
        assert cart_with_items.total() == 600 * 0.5


def test_apply_coupon_with_multiple_mocked_coupons():
    test_coupons = {
        'TEST20': 20,
        'TEST30': 30,
        'TEST70': 70
    }

    with patch.dict('shopping.COUPONS', test_coupons, clear=True):
        for coupon_code, discount in test_coupons.items():
            cart_copy = Cart()
            cart_copy.add_item("Item", 100.0)
            apply_coupon(cart_copy, coupon_code)
            assert cart_copy.total() == 100.0 * (100 - discount) / 100


def test_apply_coupon_with_empty_mocked_dict(cart_with_items):
    with patch.dict('shopping.COUPONS', {}, clear=True):
        with pytest.raises(ValueError, match="Invalid coupon"):
            apply_coupon(cart_with_items, "SAVE10")


def test_apply_coupon_with_monkeypatch(monkeypatch, cart_with_items):
    test_coupons = {'MONKEY20': 20, 'MONKEY80': 80}

    monkeypatch.setattr('shopping.COUPONS', test_coupons)

    original_total = cart_with_items.total()
    apply_coupon(cart_with_items, "MONKEY20")
    assert cart_with_items.total() == original_total * 0.8

    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart_with_items, "SAVE10")


def test_apply_coupon_sequential_with_monkeypatch(monkeypatch):
    cart = Cart()
    cart.add_item("Item", 100.0)

    monkeypatch.setattr('shopping.COUPONS', {'FIRST': 10})
    apply_coupon(cart, "FIRST")
    assert cart.total() == 90.0

    monkeypatch.setattr('shopping.COUPONS', {'SECOND': 20})

    new_cart = Cart()
    new_cart.add_item("Item", 100.0)
    apply_coupon(new_cart, "SECOND")
    assert new_cart.total() == 80.0

    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(new_cart, "FIRST")


@pytest.mark.parametrize("coupon_code, expected_discount", [
    ("SAVE10", 10),
    ("HALF", 50),
])
def test_coupon_parametrized(cart_with_items, coupon_code, expected_discount):
    original_total = cart_with_items.total()
    apply_coupon(cart_with_items, coupon_code)
    assert cart_with_items.total() == original_total * (100 - expected_discount) / 100


def test_coupon_and_discount_chain(cart_with_items):
    cart_with_items.apply_discount(20)
    total_after_first = cart_with_items.total()
    apply_coupon(cart_with_items, "HALF")
    assert cart_with_items.total() == total_after_first * 0.5

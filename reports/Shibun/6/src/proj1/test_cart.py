from unittest.mock import patch
import pytest  # type: ignore

from shopping import Cart, apply_coupon, log_purchase


#  ФИКСТУРА ПУСТОЙ КОРЗИНЫ
@pytest.fixture
def empty_cart():
    return Cart()


#  ТЕСТЫ ДОБАВЛЕНИЯ И TOTAL()
def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1


def test_add_item_negative_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("Apple", -5)


def test_total(empty_cart):
    empty_cart.add_item("Apple", 10)
    empty_cart.add_item("Banana", 5)
    assert empty_cart.total() == 15


#  ТЕСТЫ apply_discount
@pytest.mark.parametrize(
    "discount, expected",
    [
        (0, 100),     # цена не меняется
        (50, 50),     # уменьшается вдвое
        (100, 0),     # становится ноль
    ]
)
def test_apply_discount_valid(empty_cart, discount, expected):
    empty_cart.add_item("Item", 100)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected


@pytest.mark.parametrize("discount", [-10, 150])
def test_apply_discount_invalid(empty_cart, discount):
    empty_cart.add_item("Item", 100)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(discount)


#  ТЕСТЫ log_purchase (мок HTTP)
@patch("shopping.requests.post")
def test_log_purchase(mock_post):
    item = {"name": "Apple", "price": 10}

    log_purchase(item)

    mock_post.assert_called_once_with(
        "https://example.com/log",
        json=item
    )


#  ТЕСТЫ apply_coupon
def test_apply_coupon_valid(empty_cart, monkeypatch):
    empty_cart.add_item("Item", 100)

    fake_coupons = {"SAVE10": 10}
    monkeypatch.setattr("shopping.coupons", fake_coupons, raising=False)

    apply_coupon(empty_cart, "SAVE10")

    assert empty_cart.total() == 90


def test_apply_coupon_invalid(empty_cart, monkeypatch):
    empty_cart.add_item("Item", 100)

    fake_coupons = {"SAVE10": 10}
    monkeypatch.setattr("shopping.coupons", fake_coupons, raising=False)

    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "BADCODE")

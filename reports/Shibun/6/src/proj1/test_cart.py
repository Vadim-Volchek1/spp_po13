from unittest.mock import patch
import pytest  # type: ignore

from shopping import Cart, apply_coupon, log_purchase


#  ФИКСТУРА ПУСТОЙ КОРЗИНЫ
@pytest.fixture
def cart():
    return Cart()


#  ТЕСТЫ ДОБАВЛЕНИЯ И TOTAL()
def test_add_item(my_cart=cart()):
    my_cart.add_item("Apple", 10.0)
    assert len(my_cart.items) == 1


def test_add_item_negative_price(my_cart=cart()):
    with pytest.raises(ValueError):
        my_cart.add_item("Apple", -5)


def test_total(my_cart=cart()):
    my_cart.add_item("Apple", 10)
    my_cart.add_item("Banana", 5)
    assert my_cart.total() == 15


#  ТЕСТЫ apply_discount
@pytest.mark.parametrize(
    "discount, expected",
    [
        (0, 100),
        (50, 50),
        (100, 0),
    ]
)
def test_apply_discount_valid(discount, expected, my_cart=cart()):
    my_cart.add_item("Item", 100)
    my_cart.apply_discount(discount)
    assert my_cart.total() == expected


@pytest.mark.parametrize("discount", [-10, 150])
def test_apply_discount_invalid(discount, my_cart=cart()):
    my_cart.add_item("Item", 100)
    with pytest.raises(ValueError):
        my_cart.apply_discount(discount)


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
def test_apply_coupon_valid(monkeypatch, my_cart=cart()):
    my_cart.add_item("Item", 100)

    fake_coupons = {"SAVE10": 10}
    monkeypatch.setattr("shopping.coupons", fake_coupons, raising=False)

    apply_coupon(my_cart, "SAVE10")

    assert my_cart.total() == 90


def test_apply_coupon_invalid(monkeypatch, my_cart=cart()):
    my_cart.add_item("Item", 100)

    fake_coupons = {"SAVE10": 10}
    monkeypatch.setattr("shopping.coupons", fake_coupons, raising=False)

    with pytest.raises(ValueError):
        apply_coupon(my_cart, "BADCODE")

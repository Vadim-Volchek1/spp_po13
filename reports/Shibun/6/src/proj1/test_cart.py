from unittest.mock import patch
import pytest  # type: ignore

from shopping import Cart, apply_coupon, log_purchase


#  ФИКСТУРА ПУСТОЙ КОРЗИНЫ
@pytest.fixture
def cart_fixture():
    return Cart()


#  ТЕСТЫ ДОБАВЛЕНИЯ И TOTAL()
def test_add_item(cart_fixture):
    cart_fixture.add_item("Apple", 10.0)
    assert len(cart_fixture.items) == 1


def test_add_item_negative_price(cart_fixture):
    with pytest.raises(ValueError):
        cart_fixture.add_item("Apple", -5)


def test_total(cart_fixture):
    cart_fixture.add_item("Apple", 10)
    cart_fixture.add_item("Banana", 5)
    assert cart_fixture.total() == 15


#  ТЕСТЫ apply_discount
@pytest.mark.parametrize(
    "discount, expected",
    [
        (0, 100),
        (50, 50),
        (100, 0),
    ]
)
def test_apply_discount_valid(cart_fixture, discount, expected):
    cart_fixture.add_item("Item", 100)
    cart_fixture.apply_discount(discount)
    assert cart_fixture.total() == expected


@pytest.mark.parametrize("discount", [-10, 150])
def test_apply_discount_invalid(cart_fixture, discount):
    cart_fixture.add_item("Item", 100)
    with pytest.raises(ValueError):
        cart_fixture.apply_discount(discount)


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
def test_apply_coupon_valid(cart_fixture, monkeypatch):
    cart_fixture.add_item("Item", 100)

    fake_coupons = {"SAVE10": 10}
    monkeypatch.setattr("shopping.coupons", fake_coupons, raising=False)

    apply_coupon(cart_fixture, "SAVE10")

    assert cart_fixture.total() == 90


def test_apply_coupon_invalid(cart_fixture, monkeypatch):
    cart_fixture.add_item("Item", 100)

    fake_coupons = {"SAVE10": 10}
    monkeypatch.setattr("shopping.coupons", fake_coupons, raising=False)

    with pytest.raises(ValueError):
        apply_coupon(cart_fixture, "BADCODE")

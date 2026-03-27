# pylint: disable=redefined-outer-name
import pytest
from shopping import Cart, apply_coupon, log_purchase


@pytest.fixture
def empty_cart():
    return Cart()


def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1


def test_add_item_negative_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("Apple", -10.0)


def test_total(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 5.0)
    assert empty_cart.total() == 15.0


@pytest.mark.parametrize("discount, expected", [
    (0, 100.0),
    (50, 50.0),
    (100, 0.0),
])
def test_apply_discount_valid(empty_cart, discount, expected):
    empty_cart.add_item("Item", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected


@pytest.mark.parametrize("discount", [-10, 110])
def test_apply_discount_invalid(empty_cart, discount):
    empty_cart.add_item("Item", 100.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(discount)


def test_log_purchase(monkeypatch):
    called = {}

    def mock_post(url, json):
        called["url"] = url
        called["json"] = json

    monkeypatch.setattr("requests.post", mock_post)

    item = {"name": "Apple", "price": 10}
    log_purchase(item)

    assert called["url"] == "https://example.com/log"
    assert called["json"] == item


def test_apply_coupon_valid(empty_cart):
    empty_cart.add_item("Item", 100.0)
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == 90.0


def test_apply_coupon_invalid(empty_cart):
    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "INVALID")


def test_apply_coupon_mocked(empty_cart, monkeypatch):
    empty_cart.add_item("Item", 100.0)

    fake_coupons = {"TEST": 20}
    monkeypatch.setattr("shopping.coupons", fake_coupons, raising=False)

    apply_coupon(empty_cart, "TEST")
    assert empty_cart.total() == 80.0

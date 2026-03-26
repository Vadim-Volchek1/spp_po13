"""
Модуль тестирования функционала корзины покупок.
Содержит тесты для классов Cart, функций логирования и применения купонов.
"""

import pytest
import shopping  # Импортируем модуль целиком для monkeypatch
from shopping import Cart, log_purchase, apply_coupon

# --- 1. ПРОВЕРКА БАЗОВОГО ФУНКЦИОНАЛА КОРЗИНЫ ---


def test_add_item():
    """Проверка добавления товара в корзину."""
    cart = Cart()
    cart.add_item("Apple", 10.0)

    assert cart.get_item_count() == 1
    assert len(cart.items) == 1
    assert cart.items[0]["name"] == "Apple"
    assert cart.items[0]["price"] == 10.0


def test_negative_price():
    """Проверка выброса ошибки ValueError при отрицательной цене."""
    cart = Cart()

    with pytest.raises(ValueError) as exc_info:
        cart.add_item("Bad Item", -5.0)

    assert exc_info.type is ValueError
    assert "Цена не может быть отрицательной" in str(exc_info.value)
    assert cart.get_item_count() == 0


def test_total():
    """Проверка правильности вычисления общей стоимости корзины."""
    cart = Cart()
    cart.add_item("Apple", 10.0)
    cart.add_item("Banana", 15.5)
    cart.add_item("Orange", 8.75)

    expected_total = 10.0 + 15.5 + 8.75  # 34.25
    assert cart.total() == expected_total


# --- 2. ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ СКИДОК ---


@pytest.mark.parametrize(
    "sale, cost, expected",
    [
        (0, 30, 30),  # 0% скидка
        (50, 20, 10),  # 50% скидка
        (100, 50, 0),  # 100% скидка
    ],
)
def test_apply_discount(sale, cost, expected):
    """Тестирование корректного применения процента скидки."""
    cart = Cart()
    cart.add_item("Product", cost)
    cart.apply_discount(sale)
    assert cart.total() == expected


@pytest.mark.parametrize(
    "discount",
    [-1, 101, 150],
)
def test_apply_discount_invalid(discount):
    """Тестирование выброса ошибки при невалидных значениях скидки."""
    cart = Cart()
    cart.add_item("Product", 100.0)

    with pytest.raises(
        ValueError, match="Процент скидки должен быть в диапазоне от 0 до 100"
    ):
        cart.apply_discount(discount)


# --- 3. ИСПОЛЬЗОВАНИЕ ФИКСТУР ---


@pytest.fixture
def cart_fixture():
    """Фикстура, возвращающая новый пустой объект корзины."""
    return Cart()


# pylint: disable=redefined-outer-name
def test_add_single_item(cart_fixture):
    """Тест добавления товара с использованием фикстуры."""
    cart_fixture.add_item("Apple", 10.0)

    assert cart_fixture.get_item_count() == 1
    assert cart_fixture.items[0]["name"] == "Apple"


# --- 4. МОКИРОВАНИЕ (pytest-mock) ---


def test_log_purchase_calls_requests_post(mocker):
    """Проверка, что log_purchase вызывает requests.post с нужным URL."""
    mock_post = mocker.patch("requests.post")
    item = {"name": "Apple", "price": 10.0}

    log_purchase(item)

    mock_post.assert_called_once_with("https://example.com/log", json=item)


def test_log_purchase_called_with_correct_data(mocker):
    """Проверка структуры данных, передаваемых в requests.post."""
    mock_post = mocker.patch("requests.post")
    test_item = {"name": "Banana", "price": 15.5}

    log_purchase(test_item)

    _, kwargs = mock_post.call_args
    assert kwargs["json"] == test_item
    assert kwargs["json"]["name"] == "Banana"


# --- 5. ОБЕЗЬЯНЬИ ПАТЧИ (monkeypatch) ---


def test_apply_coupon_save10(monkeypatch):
    """Тест купона SAVE10 через подмену словаря coupons в модуле."""
    cart = Cart()
    cart.add_item("Apple", 100.0)

    test_coupons = {"SAVE10": 10, "HALF": 50}
    # Подменяем словарь в импортированном модуле shopping
    monkeypatch.setattr(shopping, "coupons", test_coupons)

    apply_coupon(cart, "SAVE10")

    assert cart.total() == 90.0
    assert cart.items[0]["price"] == 90.0


def test_apply_coupon_half(monkeypatch):
    """Тест купона HALF (50% скидка)."""
    cart = Cart()
    cart.add_item("Laptop", 1000.0)

    test_coupons = {"SAVE10": 10, "HALF": 50}
    monkeypatch.setattr(shopping, "coupons", test_coupons)

    apply_coupon(cart, "HALF")

    assert cart.total() == 500.0


def test_apply_coupon_invalid(monkeypatch):
    """Проверка реакции на несуществующий купон."""
    cart = Cart()
    cart.add_item("Apple", 100.0)

    test_coupons = {"SAVE10": 10}
    monkeypatch.setattr(shopping, "coupons", test_coupons)

    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart, "INVALID_CODE")

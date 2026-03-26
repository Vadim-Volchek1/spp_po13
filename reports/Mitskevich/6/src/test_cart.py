import pytest
from shopping import Cart, log_purchase, apply_coupon
import shopping

# 1.1 ПРОВЕРКА ДОБАВЛЕНИЯ ТОВАРА


def test_add_item():
    """Проверка добавления товара"""
    cart = Cart()
    cart.add_item("Apple", 10.0)

    # Assert (Проверка)
    assert cart.get_item_count() == 1
    assert len(cart.items) == 1
    assert cart.items[0]["name"] == "Apple"
    assert cart.items[0]["price"] == 10.0


# 1.2 ПРОВЕРКА ВЫБРОСА ОШИБКИ ПРИ ОТРИЦАТЕЛЬНОЙ ЦЕНЕ


def test_negative_price():
    """Проверка выброса ошибки при отрицательной цене"""
    cart = Cart()

    with pytest.raises(ValueError) as exc_info:
        cart.add_item("Bad Item", -5.0)

    # Проверяем, что было выброшено именно ValueError
    assert exc_info.type == ValueError

    # Проверяем сообщение об ошибке
    assert "Цена не может быть отрицательной" in str(exc_info.value)
    # Убеждаемся, что товар не был добавлен в корзину
    assert cart.get_item_count() == 0


# 1.3 ПРОВЕРКА ВЫЧИСЛЕНИЯ ОБЩЕЙ СТОИМОСТИ


def test_total():
    """Проверка вычисления общей стоимости"""
    cart = Cart()
    cart.add_item("Apple", 10.0)
    cart.add_item("Banana", 15.5)
    cart.add_item("Orange", 8.75)

    expected_total = 10.0 + 15.5 + 8.75  # = 34.25
    assert cart.total() == expected_total


# 2. ПРОВЕРКА ВЫЧИСЛЕНИЯ ЦЕНЫ ПО СКИДКЕ


@pytest.mark.parametrize(
    "sale, cost, expected",
    [
        (0, 30, 30),  # 0% скидка - цена остаётся прежней
        (50, 20, 10),  # 50% скидка - цена уменьшается вдвое
        (100, 50, 0),  # 100% скидка - цена становится ноль
    ],
)
def test_apply_discount(sale, cost, expected):
    """Тестирование применения скидки"""
    cart = Cart()
    cart.add_item("Product", cost)
    cart.apply_discount(sale)
    assert cart.total() == expected


@pytest.mark.parametrize(
    "discount",
    [
        -1,  # Отрицательная скидка
        -50,  # Отрицательная скидка
        101,  # Скидка > 100%
        150,  # Скидка > 100%
    ],
)
def test_apply_discount_invalid(discount):
    """Тестирование невалидных значений скидки"""
    cart = Cart()
    cart.add_item("Product", 100.0)

    with pytest.raises(
        ValueError, match="Процент скидки должен быть в диапазоне от 0 до 100"
    ):
        cart.apply_discount(discount)


# 3. С ФИКСТУРОЙ


@pytest.fixture
def cart_fixture():
    """Фикстура, возвращающая пустую корзину"""
    return Cart()


def test_add_single_item(cart_fixture):
    """Тест добавления товара с использованием фикстуры"""
    cart_fixture.add_item("Apple", 10.0)

    assert cart_fixture.get_item_count() == 1
    assert len(cart_fixture.items) == 1
    assert cart_fixture.items[0]["name"] == "Apple"
    assert cart_fixture.items[0]["price"] == 10.0


# 4. МОКИРОВАНИЕ


def test_log_purchase_calls_requests_post(mocker):
    """
    Тест проверяет, что log_purchase вызывает requests.post
    с правильными параметрами
    """
    # 1. Мокаем requests.post
    mock_post = mocker.patch("requests.post")

    # 2. Данные для логирования
    item = {"name": "Apple", "price": 10.0}

    # 3. Вызываем тестируемую функцию
    log_purchase(item)

    # 4. Проверяем, что requests.post был вызван ровно 1 раз
    mock_post.assert_called_once()

    # 5. Проверяем, что вызван с правильными аргументами
    mock_post.assert_called_with("https://example.com/log", json=item)


def test_log_purchase_called_with_correct_data(mocker):
    """
    Тест проверяет, что в requests.post передаются корректные данные
    """
    # Мокаем requests.post
    mock_post = mocker.patch("requests.post")

    # Тестовые данные
    test_item = {"name": "Banana", "price": 15.5}

    # Вызываем функцию
    log_purchase(test_item)

    # Получаем аргументы, с которыми был вызван мок
    args, kwargs = mock_post.call_args

    # Проверяем URL
    assert args[0] == "https://example.com/log"

    # Проверяем, что переданные данные совпадают
    assert kwargs["json"] == test_item
    assert kwargs["json"]["name"] == "Banana"  # ИСПРАВЛЕНО
    assert kwargs["json"]["price"] == 15.5


# 5. ЧЕРЕЗ ОБЕЗЬЯНКУ


def test_apply_coupon_save10(monkeypatch):
    """
    Тест проверяет применение купона SAVE10 (10% скидка)
    Используем monkeypatch для мокирования словаря coupons
    """
    # Arrange - Создаём корзину с товаром
    cart = Cart()
    cart.add_item("Apple", 100.0)

    # Мокаем словарь coupons
    test_coupons = {"SAVE10": 10, "HALF": 50}
    import shopping

    monkeypatch.setattr(shopping, "coupons", test_coupons)

    # Act - Применяем купон
    apply_coupon(cart, "SAVE10")

    # Assert - Проверяем результат
    assert cart.total() == 90.0  # 100 - 10% = 90
    assert cart.items[0]["price"] == 90.0


def test_apply_coupon_half(monkeypatch):
    """
    Тест проверяет применение купона HALF (50% скидка)
    """
    # Arrange
    cart = Cart()
    cart.add_item("Laptop", 1000.0)

    # Мокаем словарь coupons
    test_coupons = {"SAVE10": 10, "HALF": 50}
    import shopping

    monkeypatch.setattr(shopping, "coupons", test_coupons)

    # Act
    apply_coupon(cart, "HALF")

    # Assert
    assert cart.total() == 500.0  # 1000 - 50% = 500
    assert cart.items[0]["price"] == 500.0


def test_apply_coupon_invalid(monkeypatch):
    """
    Тест проверяет, что при неверном купоне выбрасывается исключение
    """
    # Arrange
    cart = Cart()
    cart.add_item("Apple", 100.0)

    # Мокаем словарь coupons
    test_coupons = {"SAVE10": 10, "HALF": 50}
    import shopping

    monkeypatch.setattr(shopping, "coupons", test_coupons)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart, "INVALID_CODE")

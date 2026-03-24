class Order:
    def __init__(self):
        self.burgers = []
        self.drinks = []
        self.packaging = ""
        self.total_price = 0.0

    def add_burger(self, burger):
        self.burgers.append(burger)

    def add_drink(self, drink):
        self.drinks.append(drink)

    def set_packaging(self, packaging):
        self.packaging = packaging

    def add_to_price(self, price):
        self.total_price += price

    def __str__(self):
        result = "========== ВАШ ЗАКАЗ ==========\n"
        result += "Бургеры:\n"
        for burger in self.burgers:
            result += f"  • {burger}\n"
        result += "Напитки:\n"
        for drink in self.drinks:
            result += f"  • {drink}\n"
        result += f"Упаковка: {self.packaging}\n"
        result += f"ИТОГОВАЯ СТОИМОСТЬ: {self.total_price:.2f} руб.\n"
        result += "================================"
        return result


class PriceList:
    burger_prices = {}
    drink_prices = {}

    @classmethod
    def initialize(cls):
        cls.burger_prices = {
            "веганский": 6.50,
            "куриный": 7.00,
            "говяжий": 7.50,
            "рыбный": 7.20,
            "дабл бургер": 9.00,
            "чизбургер": 6.80,
            "детский": 5.50,
            "острый": 7.30,
        }

        cls.drink_prices = {
            "кофе": 5.00,
            "капучино": 5.50,
            "латте": 5.50,
            "эспрессо": 4.50,
            "кола": 4.00,
            "кока-кола": 4.00,
            "пепси": 4.00,
            "фанта": 4.00,
            "спрайт": 4.00,
            "чай": 3.50,
            "зеленый чай": 3.50,
            "черный чай": 3.50,
            "морс": 4.50,
            "компот": 4.00,
            "вода": 2.00,
            "сок": 4.50,
        }

    @classmethod
    def get_burger_price(cls, burger_type):
        return cls.burger_prices.get(burger_type.lower(), 7.00)

    @classmethod
    def get_drink_price(cls, drink_type):
        return cls.drink_prices.get(drink_type.lower(), 4.00)

    @classmethod
    def get_available_burgers(cls):
        return set(cls.burger_prices.keys())

    @classmethod
    def get_available_drinks(cls):
        return set(cls.drink_prices.keys())

    @classmethod
    def display_menu(cls):
        print("\n=== МЕНЮ БУРГЕР-ЗАКУСОЧНОЙ ===")
        print("БУРГЕРЫ:")
        for burger in sorted(cls.burger_prices.keys()):
            print(f"  • {burger:<12} - {cls.burger_prices[burger]:.2f} руб.")

        print("\nНАПИТКИ:")
        for drink in sorted(cls.drink_prices.keys()):
            print(f"  • {drink:<12} - {cls.drink_prices[drink]:.2f} руб.")

        print("\nУПАКОВКА: на месте / с собой")
        print("===============================\n")


class OrderBuilder:
    def __init__(self):
        self.order = Order()

    def add_burger(self, burger_type):
        self.order.add_burger(burger_type)
        price = PriceList.get_burger_price(burger_type)
        self.order.add_to_price(price)
        return self

    def add_burgers(self, *burger_types):
        for burger in burger_types:
            self.add_burger(burger)
        return self

    def add_drink(self, drink_type):
        self.order.add_drink(drink_type)
        price = PriceList.get_drink_price(drink_type)
        self.order.add_to_price(price)
        return self

    def add_drinks(self, *drink_types):
        for drink in drink_types:
            self.add_drink(drink)
        return self

    def choose_packaging(self, packaging_type):
        self.order.set_packaging(packaging_type)
        return self

    def build(self):
        if not self.order.burgers:
            raise ValueError("Нужно добавить хотя бы один бургер!")
        if not self.order.drinks:
            raise ValueError("Нужно добавить хотя бы один напиток!")
        if not self.order.packaging:
            raise ValueError("Тип упаковки не выбран!")
        return self.order


def show_price_details(order):
    print("\n=== ДЕТАЛИЗАЦИЯ ЦЕН ===")
    total = 0

    print("Бургеры:")
    for burger in order.burgers:
        price = PriceList.get_burger_price(burger)
        print(f"  • {burger:<12}: {price:.2f} руб.")
        total += price

    print("Напитки:")
    for drink in order.drinks:
        price = PriceList.get_drink_price(drink)
        print(f"  • {drink:<12}: {price:.2f} руб.")
        total += price

    print(f"ИТОГО: {total:.2f} руб.")


def main():
    # Инициализация цен
    PriceList.initialize()

    print("Добро пожаловать в Бургер-закусочную!\n")

    PriceList.display_menu()

    # Семейный заказ
    family_order = (
        OrderBuilder()
        .add_burgers("говяжий", "куриный", "детский")
        .add_drinks("кола", "фанта", "сок")
        .choose_packaging("с собой")
        .build()
    )

    print("ЗАКАЗ №1 (Семейный):")
    print(family_order)
    print()

    # Заказ для компании
    company_order = (
        OrderBuilder()
        .add_burger("дабл бургер")
        .add_burger("чизбургер")
        .add_burger("веганский")
        .add_drinks("кофе", "чай", "пепси")
        .choose_packaging("на месте")
        .build()
    )

    print("ЗАКАЗ №2 (Компания):")
    print(company_order)
    print()

    # Индивидуальный заказ
    individual_order = (
        OrderBuilder()
        .add_burger("рыбный")
        .add_burger("острый")
        .add_drinks("капучино", "вода")
        .choose_packaging("с собой")
        .build()
    )

    print("ЗАКАЗ №3 (Индивидуальный):")
    print(individual_order)
    print()

    # Экономичный заказ
    economy_order = OrderBuilder().add_burger("детский").add_drink("чай").choose_packaging("на месте").build()

    print("ЗАКАЗ №4 (Экономичный):")
    print(economy_order)
    print()

    # Тест неизвестных продуктов
    print("=== ТЕСТ НЕИЗВЕСТНОГО ПРОДУКТА ===")
    try:
        test_order = OrderBuilder().add_burger("гамбургер").add_drink("лимонад").choose_packaging("с собой").build()
        print(test_order)
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()

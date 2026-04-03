"""Модуль для системы заказов бургер-закусочной с использованием паттерна Builder."""

from abc import ABC, abstractmethod


class Order:
    """Готовый заказ."""

    def __init__(self):
        self.burger = None
        self.drink = None
        self.packaging = None
        self.total_price = 0

    def set_burger(self, burger):
        self.burger = burger

    def set_drink(self, drink):
        self.drink = drink

    def set_packaging(self, packaging):
        self.packaging = packaging

    def calculate_total(self):
        self.total_price = (
            (self.burger.price if self.burger else 0)
            + (self.drink.price if self.drink else 0)
            + (self.packaging.price if self.packaging else 0)
        )
        return self.total_price

    def show(self):
        print("\n" + "=" * 40)
        print("         ВАШ ЗАКАЗ")
        print("=" * 40)
        if self.burger:
            print(f"Бургер:   {self.burger.name} ({self.burger.category}) - {self.burger.price} BYN")
        if self.drink:
            print(f"Напиток:  {self.drink.name} ({self.drink.category}) - {self.drink.price} BYN")
        if self.packaging:
            print(f"Упаковка: {self.packaging.name} - {self.packaging.price} BYN")
        print("-" * 40)
        print(f"ИТОГОВАЯ СТОИМОСТЬ: {self.calculate_total()} BYN")
        print("=" * 40)


class Burger:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category


class Drink:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category


class Packaging:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class OrderBuilder(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def add_burger(self, choice):
        pass

    @abstractmethod
    def add_drink(self, choice):
        pass

    @abstractmethod
    def add_packaging(self, choice):
        pass

    @abstractmethod
    def get_order(self):
        pass


class FastFoodOrderBuilder(OrderBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self.order = Order()
        return self

    def add_burger(self, choice):
        burgers = {
            "1": Burger("Classic (beef)", 8.50, "мясной"),
            "2": Burger("Chicken", 7.50, "куриный"),
            "3": Burger("Vegan (with veggies)", 6.80, "веганский"),
            "4": Burger("Double cheese", 11.00, "мясной"),
        }
        if choice in burgers:
            self.order.set_burger(burgers[choice])
        return self

    def add_drink(self, choice):
        drinks = {
            "1": Drink("Pepsi", 2.80, "холодный"),
            "2": Drink("Coca-Cola", 2.80, "холодный"),
            "3": Drink("Americano coffee", 3.50, "горячий"),
            "4": Drink("Black tea", 2.50, "горячий"),
            "5": Drink("Sprite", 2.80, "холодный"),
        }
        if choice in drinks:
            self.order.set_drink(drinks[choice])
        return self

    def add_packaging(self, choice):
        packagings = {"1": Packaging("С собой", 0.70), "2": Packaging("На месте", 0.00)}
        if choice in packagings:
            self.order.set_packaging(packagings[choice])
        return self

    def get_order(self):
        return self.order


class OrderDirector:
    def __init__(self, builder_class):
        self.builder_class = builder_class

    def make_vegan_takeaway_order(self):
        builder = self.builder_class()
        return builder.reset().add_burger("3").add_drink("4").add_packaging("1").get_order()

    def make_classic_dinein_order(self):
        builder = self.builder_class()
        return builder.reset().add_burger("1").add_drink("1").add_packaging("2").get_order()


def show_menu():
    """Показывает меню и собирает выбор пользователя."""
    print("\n" + "=" * 40)
    print("    ДОБРО ПОЖАЛОВАТЬ В БУРГЕР-ЗАКУСОЧНУЮ!")
    print("=" * 40)

    print("\n--- БУРГЕРЫ ---")
    print("1. Classic (beef) - 8.50 BYN (мясной)")
    print("2. Chicken - 7.50 BYN (куриный)")
    print("3. Vegan (with veggies) - 6.80 BYN (веганский)")
    print("4. Double cheese - 11.00 BYN (мясной)")
    burger_choice = input("\nВыберите бургер (1-4): ")

    print("\n--- НАПИТКИ ---")
    print("1. Pepsi - 2.80 BYN (холодный)")
    print("2. Coca-Cola - 2.80 BYN (холодный)")
    print("3. Americano coffee - 3.50 BYN (горячий)")
    print("4. Black tea - 2.50 BYN (горячий)")
    print("5. Sprite - 2.80 BYN (холодный)")
    drink_choice = input("\nВыберите напиток (1-5): ")

    print("\n--- ТИП УПАКОВКИ ---")
    print("1. С собой - 0.70 BYN")
    print("2. На месте - 0.00 BYN")
    packaging_choice = input("\nВыберите тип упаковки (1-2): ")

    return burger_choice, drink_choice, packaging_choice


def main():
    burger_choice, drink_choice, packaging_choice = show_menu()

    builder = FastFoodOrderBuilder()
    order = (
        builder.reset().add_burger(burger_choice).add_drink(drink_choice).add_packaging(packaging_choice).get_order()
    )
    order.show()

    print("\n" + "=" * 40)
    print("    ГОТОВЫЕ ЗАКАЗЫ (ПРИМЕР РАБОТЫ ДИРЕКТОРА)")
    print("=" * 40)

    director = OrderDirector(FastFoodOrderBuilder)
    director.make_vegan_takeaway_order().show()
    director.make_classic_dinein_order().show()


if __name__ == "__main__":
    main()

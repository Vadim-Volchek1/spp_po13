from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

    def __str__(self):
        return f"{self.get_description()}: {self.get_cost()} руб."


class Espresso(Coffee):
    def get_description(self):
        return "Эспрессо"

    def get_cost(self):
        return 100


class Americano(Coffee):
    def get_description(self):
        return "Американо"

    def get_cost(self):
        return 120


class Cappuccino(Coffee):
    def get_description(self):
        return "Капучино"

    def get_cost(self):
        return 150


class Latte(Coffee):
    def get_description(self):
        return "Латте"

    def get_cost(self):
        return 160


class Mocha(Coffee):
    def get_description(self):
        return "Мокко"

    def get_cost(self):
        return 180


class CoffeeMachine:
    def __init__(self):
        self._recipes = {
            "эспрессо": Espresso,
            "американо": Americano,
            "капучино": Cappuccino,
            "латте": Latte,
            "мокко": Mocha,
        }

    def make_coffee(self, drink_name: str) -> Coffee:
        drink_name = drink_name.lower()
        if drink_name not in self._recipes:
            raise ValueError(
                f"Напиток '{drink_name}' не найден. Доступны: {', '.join(self._recipes.keys())}"
            )
        return self._recipes[drink_name]()

    def show_menu(self):
        print("=== МЕНЮ ===")
        for drink_class in self._recipes.values():
            drink = drink_class()
            print(f"  {drink}")
        print("============")


if __name__ == "__main__":
    machine = CoffeeMachine()
    machine.show_menu()

    print("\nЗаказы:")
    order_list = ["эспрессо", "капучино", "латте", "мокко"]
    for order_drink in order_list:
        prepared_drink = machine.make_coffee(order_drink)
        print(f"  Приготовлен: {prepared_drink}")

    try:
        machine.make_coffee("чай")
    except ValueError as e:
        print(f"\nОшибка: {e}")

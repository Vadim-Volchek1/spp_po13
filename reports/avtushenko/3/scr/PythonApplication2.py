from abc import ABC, abstractmethod


# Абстрактный класс напитка
class Coffee(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

    def __str__(self):
        return f"{self.get_description()}: {self.get_cost()} руб."


# Конкретные напитки
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


# Фабрика (Кофе-автомат)
class CoffeeMachine:
    def __init__(self):
        self._recipes = {
            "эспрессо": Espresso,
            "американо": Americano,
            "капучино": Cappuccino,
            "латте": Latte,
            "мокко": Mocha,
        }

    def make_coffee(self, name: str) -> Coffee:
        name = name.lower()
        if name not in self._recipes:
            raise ValueError(
                f"Напиток '{name}' не найден. Доступны: {', '.join(self._recipes.keys())}"
            )
        return self._recipes[name]()

    def show_menu(self):
        print("=== МЕНЮ ===")
        for name, coffee_class in self._recipes.items():
            coffee = coffee_class()
            print(f"  {coffee}")
        print("============")


# Демонстрация
if __name__ == "__main__":
    machine = CoffeeMachine()
    machine.show_menu()

    print("\nЗаказы:")
    for drink in ["эспрессо", "капучино", "латте", "мокко"]:
        coffee = machine.make_coffee(drink)
        print(f"  Приготовлен: {coffee}")

    # Попытка заказать несуществующий напиток
    try:
        machine.make_coffee("чай")
    except ValueError as e:
        print(f"\nОшибка: {e}")

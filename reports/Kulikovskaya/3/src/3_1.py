from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict


@dataclass
class CoffeeRecipe:
    # Рецепт кофейного напитка
    name: str
    water_ml: int
    coffee_g: int
    milk_ml: int = 0
    sugar_g: int = 0
    extras: list = None

    def __post_init__(self):
        if self.extras is None:
            self.extras = []


class Coffee(ABC):
    # Абстрактный класс кофейного напитка

    def __init__(self, recipe: CoffeeRecipe):
        self._recipe = recipe
        self._is_prepared = False

    @abstractmethod
    def prepare(self) -> str:  # Приготовление кофе
        pass

    @abstractmethod
    def get_description(self) -> str:  # Получение описания напитка
        pass

    def get_recipe(self) -> CoffeeRecipe:
        return self._recipe

    def __str__(self):
        return f"{self._recipe.name} ({'готов' if self._is_prepared else 'не готов'})"


# Конкретные продукты (5 классов напитков)

class Espresso(Coffee):

    def prepare(self) -> str:
        self._is_prepared = True
        return (
            f"Приготовление {self._recipe.name}:\n"
            f"  - Заливаем {self._recipe.water_ml}мл воды\n"
            f"  - Добавляем {self._recipe.coffee_g}г молотого кофе\n"
            f"  - Экстракция под давлением 9 бар\n"
            f"  Эспрессо готов!"
        )

    def get_description(self) -> str:
        return "Классический итальянский эспрессо - крепкий и насыщенный"


class Cappuccino(Coffee):

    def prepare(self) -> str:
        self._is_prepared = True
        return (
            f"Приготовление {self._recipe.name}:\n"
            f"  - Готовим основу: эспрессо ({self._recipe.coffee_g}г)\n"
            f"  - Взбиваем {self._recipe.milk_ml}мл молока в пену\n"
            f"  - Добавляем молочную пену (1/3 объема)\n"
            f"  - Посыпаем какао или корицей\n"
            f"  Капучино готов!"
        )

    def get_description(self) -> str:
        return "Капучино с нежной молочной пенкой и насыщенным вкусом"


class Latte(Coffee):

    def prepare(self) -> str:
        self._is_prepared = True
        return (
            f"Приготовление {self._recipe.name}:\n"
            f"  - Нагреваем {self._recipe.milk_ml}мл молока\n"
            f"  - Добавляем эспрессо ({self._recipe.coffee_g}г)\n"
            f"  - Сверху ложка молочной пены\n"
            f"  - Можно добавить сироп по вкусу\n"
            f"  Латте готов!"
        )

    def get_description(self) -> str:
        return "Мягкий латте с большим количеством молока"


class Americano(Coffee):

    def prepare(self) -> str:
        self._is_prepared = True
        return (
            f"Приготовление {self._recipe.name}:\n"
            f"  - Готовим эспрессо ({self._recipe.coffee_g}г)\n"
            f"  - Добавляем {self._recipe.water_ml}мл горячей воды\n"
            f"  - Размешиваем\n"
            f"  Американо готов!"
        )

    def get_description(self) -> str:
        return "Легкий американо - эспрессо с добавлением воды"


class Mocha(Coffee):
    # Мокка (шоколадный кофе)

    def prepare(self) -> str:
        self._is_prepared = True
        chocolate = self._recipe.extras[0] if self._recipe.extras else "шоколад"
        return (
            f"Приготовление {self._recipe.name}:\n"
            f"  - Растворяем {chocolate} в горячей воде\n"
            f"  - Добавляем эспрессо ({self._recipe.coffee_g}г)\n"
            f"  - Вливаем {self._recipe.milk_ml}мл молока\n"
            f"  - Украшаем взбитыми сливками\n"
            f"  Мокка готов!"
        )

    def get_description(self) -> str:
        return "Шоколадная мокка для сладкоежек"


# Фабрики (Factory Method)

class CoffeeMachine(ABC):
    # Абстрактный класс кофе-машины (Создатель)

    def __init__(self, machine_id: str, location: str):
        self._machine_id = machine_id
        self._location = location
        self._prepared_coffees: list = []

    @abstractmethod
    def create_coffee(self, sizee: str = "medium") -> Coffee:  # Фабричный метод - создание кофе
        pass

    def make_coffee(self, sizee: str = "medium") -> str:
        coffee = self.create_coffee(sizee)
        resultt = coffee.prepare()
        self._prepared_coffees.append(coffee)
        return resultt

    def get_stats(self) -> str:
        return f"Машина {self._machine_id} ({self._location}): приготовлено {len(self._prepared_coffees)} напитков"


class EspressoMachine(CoffeeMachine):
    # Машина для эспрессо

    def create_coffee(self, sizee: str = "medium") -> Coffee:
        recipes = {
            "small": CoffeeRecipe("Эспрессо", 30, 7),
            "medium": CoffeeRecipe("Эспрессо", 60, 14),
            "large": CoffeeRecipe("Двойной эспрессо", 60, 18),
        }
        return Espresso(recipes.get(sizee, recipes["medium"]))


class CappuccinoMachine(CoffeeMachine):
    # Машина для капучино

    def create_coffee(self, sizee: str = "medium") -> Coffee:
        recipes = {
            "small": CoffeeRecipe("Капучино", 60, 7, 60),
            "medium": CoffeeRecipe("Капучино", 60, 14, 120),
            "large": CoffeeRecipe("Капучино", 90, 18, 180),
        }
        return Cappuccino(recipes.get(sizee, recipes["medium"]))


class LatteMachine(CoffeeMachine):
    # Машина для латте

    def create_coffee(self, sizee: str = "medium") -> Coffee:
        recipes = {
            "small": CoffeeRecipe("Латте", 60, 7, 120),
            "medium": CoffeeRecipe("Латте", 60, 14, 240),
            "large": CoffeeRecipe("Латте", 90, 18, 350),
        }
        return Latte(recipes.get(sizee, recipes["medium"]))


class AmericanoMachine(CoffeeMachine):
    # Машина для американо

    def create_coffee(self, sizee: str = "medium") -> Coffee:
        recipes = {
            "small": CoffeeRecipe("Американо", 120, 7),
            "medium": CoffeeRecipe("Американо", 180, 14),
            "large": CoffeeRecipe("Американо", 240, 18),
        }
        return Americano(recipes.get(sizee, recipes["medium"]))


class MochaMachine(CoffeeMachine):
    # Машина для мокки

    def create_coffee(self, sizee: str = "medium") -> Coffee:
        recipes = {
            "small": CoffeeRecipe("Мокка", 60, 7, 60, extras=["горячий шоколад 20г"]),
            "medium": CoffeeRecipe("Мокка", 60, 14, 120, extras=["горячий шоколад 30г"]),
            "large": CoffeeRecipe("Мокка", 90, 18, 180, extras=["горячий шоколад 40г"]),
        }
        return Mocha(recipes.get(sizee, recipes["medium"]))


# Универсальная кофе-станция

class CoffeeStation:
    # Кофе-станция с различными машинами

    def __init__(self):
        self._machines: Dict[str, CoffeeMachine] = {}
        self._setup_machines()

    def _setup_machines(self):
        # Настройка всех типов машин
        self._machines["espresso"] = EspressoMachine("ESP-001", "Зал ожидания")
        self._machines["cappuccino"] = CappuccinoMachine("CAP-001", "Зал ожидания")
        self._machines["latte"] = LatteMachine("LAT-001", "VIP-зал")
        self._machines["americano"] = AmericanoMachine("AMR-001", "Коворкинг")
        self._machines["mocha"] = MochaMachine("MCH-001", "Кафе")

    def order_coffee(self, coffee_type: str, sizee: str = "medium") -> str:
        # Заказ кофе определенного типа
        machine = self._machines.get(coffee_type.lower())
        if not machine:
            available = ", ".join(self._machines.keys())
            return f"Неизвестный тип кофе: {coffee_type}. Доступны: {available}"

        print(f"Заказ: {coffee_type.title()}, размер: {sizee}")
        print(f"Машина: {machine.get_stats()}")

        resultt = machine.make_coffee(sizee)
        return resultt

    def get_machines(self) -> Dict[str, CoffeeMachine]:
        # Получить копию словаря машиy
        return self._machines.copy()

    def get_menu(self) -> str:
        # Получение меню
        menu = "\nМЕНЮ КОФЕ-СТАНЦИИ\n"

        descriptions = {
            "espresso": "Крепкий классический эспрессо",
            "cappuccino": "Капучино с молочной пенкой",
            "latte": "Мягкий латте с молоком",
            "americano": "Легкий американо",
            "mocha": "Шоколадная мокка",
        }

        for key in self._machines:
            menu += f"• {key.title():12} - {descriptions[key]}\n"

        return menu


if __name__ == "__main__":
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНА 'ФАБРИЧНЫЙ МЕТОД'")
    print("Кофе-автомат с 5 типами напитков")

    # Создание кофе-станции
    sstation = CoffeeStation()

    # Вывод меню
    print(sstation.get_menu())

    # Заказы различных напитков
    oorders = [
        ("espresso", "small"),
        ("cappuccino", "medium"),
        ("latte", "large"),
        ("americano", "medium"),
        ("mocha", "medium"),
        ("unknown", "small"),  # Тест ошибки
    ]

    for ccoffee_type, size in oorders:
        result = sstation.order_coffee(ccoffee_type, size)
        print(result)

    print("ИТОГОВАЯ СТАТИСТИКА")

    for mmachine in sstation.get_machines().values():
        print(mmachine.get_stats())

# Factory Method (Фабричный метод)

from abc import ABC, abstractmethod

# Абстрактные классы
class Coffee(ABC):
    @abstractmethod
    def cook(self):
        pass

class CoffeeFactory(ABC):
    @abstractmethod
    def create_coffee(self):
        pass

# Виды кофе
class Espresso(Coffee):
    def cook(self):
        print("Готовится Espresso")

class Americano(Coffee):
    def cook(self):
        print("Готовится Americano")

class Cappuccino(Coffee):
    def cook(self):
        print("Готовится Cappuccino")

class Latte(Coffee):
    def cook(self):
        print("Готовится Latte")

class Mocha(Coffee):
    def cook(self):
        print("Готовится Mocha")

# Фабрики
class EspressoFactory(CoffeeFactory):
    def create_coffee(self):
        return Espresso()

class AmericanoFactory(CoffeeFactory):
    def create_coffee(self):
        return Americano()

class LatteFactory(CoffeeFactory):
    def create_coffee(self):
        return Latte()

class CappuccinoFactory(CoffeeFactory):
    def create_coffee(self):
        return Cappuccino()

class MochaFactory(CoffeeFactory):
    def create_coffee(self):
        return Mocha()


factory = AmericanoFactory()
coffee = factory.create_coffee()
coffee.cook()

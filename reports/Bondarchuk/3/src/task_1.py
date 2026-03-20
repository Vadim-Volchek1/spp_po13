"""
В2
Первая группа заданий (порождающий паттерн)
2) Заводы по производству автомобилей. Реализовать
возможность создавать
автомобили различных типов на различных заводах.
"""

from abc import ABC, abstractmethod

#Продукты
class Car(ABC):
    @abstractmethod
    def get_specs(self):
        pass

    def public_def_only_for_public_def_def_pylint_live_me_along(self):
        print("\npublic_def_only_for_public_def_def_pylint_live_me_along\n")

class Sedan(Car):
    def __init__(self, brand):
        self.brand = brand

    def get_specs(self):
        return f"{self.brand} Седан: 4 двери, комфортная подвеска?"

class Jeep(Car):
    def __init__(self, brand):
        self.brand = brand

    def get_specs(self):
        return f"{self.brand} Внедорожник: Полный привод, высокий"

class Hatchback(Car):
    def __init__(self, brand):
        self.brand = brand

    def get_specs(self):
        return f"{self.brand} Хэтчбек: Компактный, 92"

#Абстрактная фабрика
class CarFactory(ABC):
    @abstractmethod
    def create_sedan(self) -> Sedan:
        pass

    @abstractmethod
    def create_jeep(self) -> Jeep:
        pass

    @abstractmethod
    def create_hatchback(self) -> Hatchback:
        pass

#Конкретные фабрики
class VazFactory(CarFactory):
    def create_sedan(self) -> Sedan:
        return Sedan("Lada Vesta")

    def create_jeep(self) -> Jeep:
        return Jeep("VAZ PATRIOT!")

    def create_hatchback(self) -> Hatchback:
        return Hatchback("Lada XRAY")

class RenaultFactory(CarFactory):
    def create_sedan(self) -> Sedan:
        return Sedan("Renault LoganXMan")

    def create_jeep(self) -> Jeep:
        return Jeep("Renault Пыльник")

    def create_hatchback(self) -> Hatchback:
        return Hatchback("Renault Prprpr")

def obertka(factory: CarFactory):
    print("\nРаботает завод:", factory.__class__.__name__)
    car1 = factory.create_sedan()
    car2 = factory.create_jeep()
    car3 = factory.create_hatchback()

    print(car1.get_specs())
    print(car2.get_specs())
    print(car3.get_specs())

if __name__ == "__main__":
    vaz = VazFactory()
    renault = RenaultFactory()

    obertka(vaz)
    obertka(renault)

from abc import ABC, abstractmethod

class Car(ABC):
    @abstractmethod
    def drive(self):
        pass


class BMWSedan(Car):
    def drive(self):
        return "BMW Sedan: комфортная езда"


class BMWSUV(Car):
    def drive(self):
        return "BMW SUV: мощный внедорожник"


class ToyotaSedan(Car):
    def drive(self):
        return "Toyota Sedan: экономичная езда"


class ToyotaSUV(Car):
    def drive(self):
        return "Toyota SUV: надёжный внедорожник"


class CarFactory(ABC):
    @abstractmethod
    def create_sedan(self) -> Car:
        pass

    @abstractmethod
    def create_suv(self) -> Car:
        pass


class BMWFactory(CarFactory):
    def create_sedan(self):
        return BMWSedan()

    def create_suv(self):
        return BMWSUV()


class ToyotaFactory(CarFactory):
    def create_sedan(self):
        return ToyotaSedan()

    def create_suv(self):
        return ToyotaSUV()


def client(factory: CarFactory):
    sedan = factory.create_sedan()
    suv = factory.create_suv()
    print(sedan.drive())
    print(suv.drive())


if __name__ == "__main__":
    print("=== BMW Factory ===")
    client(BMWFactory())

    print("\n=== Toyota Factory ===")
    client(ToyotaFactory())

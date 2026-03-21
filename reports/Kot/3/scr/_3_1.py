from abc import ABC, abstractmethod


# Абстрактные продукты
class Engine(ABC):
    @abstractmethod
    def get_specs(self):
        pass


class Body(ABC):
    @abstractmethod
    def get_type(self):
        pass


# Конкретные продукты для Toyota
class ToyotaEngine(Engine):
    def get_specs(self):
        return "Toyota 2.0L VVT-i"


class ToyotaSedanBody(Body):
    def get_type(self):
        return "Sedan (Toyota Camry style)"


class ToyotaSUVBody(Body):
    def get_type(self):
        return "SUV (Toyota RAV4 style)"


# Конкретные продукты для BMW
class BMWEngine(Engine):
    def get_specs(self):
        return "BMW 3.0L TwinPower Turbo"


class BMWSedanBody(Body):
    def get_type(self):
        return "Sedan (BMW 3 Series style)"


class BMWSUVBody(Body):
    def get_type(self):
        return "SUV (BMW X5 style)"


# Абстрактная фабрика
class CarFactory(ABC):
    @abstractmethod
    def create_engine(self) -> Engine:
        pass

    @abstractmethod
    def create_body(self) -> Body:
        pass

    def assemble_car(self, car_type: str):
        engine = self.create_engine()
        body = self.create_body() if car_type == "Sedan" else self.create_suv_body()

        print(f"[BUILD] Starting car assembly at {self.__class__.__name__}")
        print(f"[INFO] Engine installed: {engine.get_specs()}")
        print(f"[INFO] Body installed: {body.get_type()}")
        print(
            f"[RESULT] Car successfully created: {self.__class__.__name__} {car_type}\n"
        )
        return f"{self.__class__.__name__} {car_type}"


# Конкретные фабрики
class ToyotaFactory(CarFactory):
    def create_engine(self):
        return ToyotaEngine()

    def create_body(self):
        return ToyotaSedanBody()

    def create_suv_body(self):
        return ToyotaSUVBody()


class BMWFactory(CarFactory):
    def create_engine(self):
        return BMWEngine()

    def create_body(self):
        return BMWSedanBody()

    def create_suv_body(self):
        return BMWSUVBody()


# Клиентский код
def produce_car(factory: CarFactory, model: str):
    print(f"=== Order received: {factory.__class__.__name__} {model} ===")
    factory.assemble_car(model)


if __name__ == "__main__":
    toyota_factory = ToyotaFactory()
    bmw_factory = BMWFactory()
    produce_car(toyota_factory, "Sedan")
    produce_car(toyota_factory, "SUV")
    produce_car(bmw_factory, "Sedan")
    produce_car(bmw_factory, "SUV")

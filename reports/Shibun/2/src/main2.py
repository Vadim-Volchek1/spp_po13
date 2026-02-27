from abc import ABC, abstractmethod

# реализация
class TechnicalReportProvider(ABC):
    @abstractmethod
    def report_issue(self) -> str:
        pass


# базовый класс члена экипажа
class CrewMember:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"


# наследники
class Pilot(CrewMember, TechnicalReportProvider):
    def report_issue(self) -> str:
        return "Обнаружены технические неисправности. Требуется изменить аэропорт назначения."


class Navigator(CrewMember):
    pass


class RadioOperator(CrewMember):
    pass


class Stewardess(CrewMember):
    pass


# самолёт
class Airplane:
    def __init__(self, model: str, capacity: int, range_km: int):
        self.model = model
        self.capacity = capacity
        self.range_km = range_km

    def __str__(self):
        return f"{self.model} (вместимость: {self.capacity}, дальность: {self.range_km} км)"


# аэропорт
class Airport:
    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city

    def __str__(self):
        return f"{self.name} ({self.city})"


# агрегация
class FlightCrew:
    def __init__(self):
        self.members = []

    def add_member(self, member: CrewMember):
        self.members.append(member)

    def __str__(self):
        return "\n".join(str(m) for m in self.members)


# рейс
class Flight:
    def __init__(self, code: str, airplane: Airplane, departure: Airport, destination: Airport):
        self.code = code
        self.airplane = airplane
        self.departure = departure
        self.destination = destination
        self.crew = FlightCrew()
        self.cancelled = False

    def cancel_due_weather(self, airport: Airport):
        self.cancelled = True
        print(f"Рейс {self.code} отменён из-за погоды в аэропорту: {airport}")

    def change_destination(self, new_airport: Airport, pilot: Pilot):
        reason = pilot.report_issue()
        print(f"Командир сообщает: {reason}")
        print(f"Аэропорт назначения изменён: {self.destination} → {new_airport}")
        self.destination = new_airport

    def __str__(self):
        return (f"Рейс {self.code}\n"
                f"Самолёт: {self.airplane}\n"
                f"Откуда: {self.departure}\n"
                f"Куда: {self.destination}\n"
                f"Экипаж:\n{self.crew}\n"
                f"Статус: {'Отменён' if self.cancelled else 'Активен'}")

# аэропорты
moscow = Airport("Шереметьево", "Москва")
minsk = Airport("Минск-2", "Минск")
gomel = Airport("Гомель", "Гомель")

# самолёт
airbus = Airplane("Airbus A320", 180, 6100)

# рейс
flight = Flight("SU123", airbus, moscow, minsk)

# формирование экипажа
pilot1 = Pilot("Иванов И.И.")
flight.crew.add_member(pilot1)
flight.crew.add_member(Navigator("Петров П.П."))
flight.crew.add_member(RadioOperator("Сидоров С.С."))
flight.crew.add_member(Stewardess("Анна А.А."))
flight.crew.add_member(Stewardess("Мария М.М."))

# отмена рейса из-за погоды
flight.cancel_due_weather(moscow)

# изменение аэропорта назначения из-за неисправностей
flight.change_destination(gomel, pilot1)

# вывод информации о рейсе
print(flight)

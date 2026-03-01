from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

# 1. ОБОБЩЕНИЕ (Generalization/Inheritance)

@dataclass
class PersonData:
    #Вспомогательный класс для хранения данных о человеке
    name: str
    id_number: str
    age: int


class Person(ABC):
    #Абстрактный базовый класс для всех людей в системе
    #Обобщение: Employee и Passenger наследуют от Person

    def __init__(self, data: PersonData):
        self._name = data.name
        self._id_number = data.id_number
        self._age = data.age

    @property
    def name(self) -> str:
        return self._name

    @property
    def id_number(self) -> str:
        return self._id_number

    @abstractmethod
    def get_role(self) -> str:
        #Абстрактный метод - реализация (Realization)
        pass

    def __str__(self) -> str:
        return f"{self._name} (ID: {self._id_number}), {self._age} лет"


@dataclass
class EmployeeData:
    #Вспомогательный класс для хранения данных о сотруднике
    person_data: PersonData
    employee_id: str
    experience_years: int


class Employee(Person):
    #Класс сотрудника Аэрофлота
    #Наследуется от Person (обобщение)

    def __init__(self, data: EmployeeData):
        super().__init__(data.person_data)
        self._employee_id = data.employee_id
        self._experience_years = data.experience_years
        self._is_available = True

    @property
    def employee_id(self) -> str:
        return self._employee_id

    @property
    def is_available(self) -> bool:
        return self._is_available

    @is_available.setter
    def is_available(self, value: bool):
        self._is_available = value

    def get_role(self) -> str:
        return "Сотрудник Аэрофлота"

    def __str__(self):
        return (f"{super().__str__()}, Таб. №: {self._employee_id}, "
                f"Стаж: {self._experience_years} лет")


# Специализации сотрудников
@dataclass
class PilotData:
    #Данные пилота
    employee_data: EmployeeData
    license_number: str
    is_commander: bool = False


class Pilot(Employee):
    #Класс пилота

    def __init__(self, data: PilotData):
        super().__init__(data.employee_data)
        self._license_number = data.license_number
        self._is_commander = data.is_commander
        self._flight_hours = 0

    @property
    def is_commander(self) -> bool:
        return self._is_commander

    def report_technical_issue(self, issue: str, current_flight):
        #Командир сообщает о технических неисправностях
        if self._is_commander:
            print(f"КОМАНДИР {self._name}: Сообщает о неисправности: {issue}")
            current_flight.handle_emergency(issue)
        else:
            print(f"Пилот {self._name} не является командиром")

    def get_role(self) -> str:
        return "Командир воздушного судна" if self._is_commander else "Второй пилот"

    def __str__(self):
        role = "Командир" if self._is_commander else "Второй пилот"
        return f"{role}: {super().__str__()}, Лицензия: {self._license_number}"


@dataclass
class NavigatorData:
    #Данные штурмана
    employee_data: EmployeeData
    navigation_cert: str


class Navigator(Employee):
    #Класс штурмана

    def __init__(self, data: NavigatorData):
        super().__init__(data.employee_data)
        self._navigation_cert = data.navigation_cert

    def get_role(self) -> str:
        return "Штурман"

    def __str__(self):
        return f"Штурман: {super().__str__()}"


@dataclass
class RadioOperatorData:
    #Данные радиста
    employee_data: EmployeeData
    radio_license: str


class RadioOperator(Employee):
    #Класс радиста

    def __init__(self, data: RadioOperatorData):
        super().__init__(data.employee_data)
        self._radio_license = data.radio_license

    def get_role(self) -> str:
        return "Радист"

    def __str__(self):
        return f"Радист: {super().__str__()}"


@dataclass
class FlightAttendantData:
    #Данные бортпроводника
    employee_data: EmployeeData
    languages: List[str]


class FlightAttendant(Employee):
    #Класс стюардессы

    def __init__(self, data: FlightAttendantData):
        super().__init__(data.employee_data)
        self._languages = data.languages

    def get_role(self) -> str:
        return "Бортпроводник"

    def __str__(self):
        return f"Бортпроводник: {super().__str__()}, Языки: {', '.join(self._languages)}"


@dataclass
class PassengerData:
    #Данные пассажира
    person_data: PersonData
    passport: str
    ticket_number: str


class Passenger(Person):
    #Класс пассажира

    def __init__(self, data: PassengerData):
        super().__init__(data.person_data)
        self._passport = data.passport
        self._ticket_number = data.ticket_number

    def get_role(self) -> str:
        return "Пассажир"

    def __str__(self):
        return f"Пассажир: {super().__str__()}, Паспорт: {self._passport}"


# 2. РЕАЛИЗАЦИЯ (Realization/Interface)

class Flyable(ABC):
    #Интерфейс для объектов, которые могут летать
    #Реализуется классом Aircraft


    @abstractmethod
    def take_off(self):
        pass

    @abstractmethod
    def land(self):
        pass

    @abstractmethod
    def get_flight_range(self) -> float:
        pass


# 3. АГРЕГАЦИЯ (Aggregation)

@dataclass
class AircraftData:
    #Данные самолета
    registration: str
    model: str
    capacity: int
    flight_range: float
    manufacturer: str


class Aircraft(Flyable):
    #Класс самолета
    #Агрегация с Crew (экипаж может существовать без самолета)
    #Реализация интерфейса Flyable

    def __init__(self, data: AircraftData):
        self._registration = data.registration
        self._model = data.model
        self._capacity = data.capacity
        self._flight_range = data.flight_range
        self._manufacturer = data.manufacturer
        self._is_airworthy = True
        self._current_location = ""

    @property
    def registration(self) -> str:
        return self._registration

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def flight_range(self) -> float:
        return self._flight_range

    def take_off(self):
        print(f"Самолет {self._model} ({self._registration}) взлетает")

    def land(self):
        print(f"Самолет {self._model} ({self._registration}) приземляется")

    def get_flight_range(self) -> float:
        return self._flight_range

    def __str__(self):
        return (f"Самолет {self._model} [{self._registration}], "
                f"Вместимость: {self._capacity}, Дальность: {self._flight_range} км")


@dataclass
class AirportData:
    #Данные аэропорта
    code: str
    name: str
    city: str
    country: str
    weather_condition: str = "Хорошая"


class Airport:
    #Класс аэропорта
    #Агрегация с Flight (рейс может менять аэропорт назначения)

    def __init__(self, data: AirportData):
        self._code = data.code
        self._name = data.name
        self._city = data.city
        self._country = data.country
        self._weather_condition = data.weather_condition
        self._is_operational = True

    @property
    def code(self) -> str:
        return self._code

    @property
    def city(self) -> str:
        return self._city

    @property
    def weather_condition(self) -> str:
        return self._weather_condition

    @weather_condition.setter
    def weather_condition(self, value: str):
        self._weather_condition = value
        if value in ["Шторм", "Туман", "Снегопад", "Гроза"]:
            print(f"⚠️  Внимание! В аэропорту {self._code} ухудшение погоды: {value}")

    def is_flight_possible(self) -> bool:
        #Проверка возможности полета из-за погоды
        bad_weather = ["Шторм", "Туман", "Снегопад", "Гроза"]
        return self._weather_condition not in bad_weather

    def __str__(self):
        return f"{self._name} ({self._code}), {self._city}, {self._country}"


# 4. КОМПОЗИЦИЯ (Composition)

class Crew:
    #Класс летной бригады
    #Композиция: бригада состоит из сотрудников и не существует без них

    def __init__(self, crew_id: str):
        self._crew_id = crew_id
        self._pilots: List[Pilot] = []
        self._navigator: Optional[Navigator] = None
        self._radio_operator: Optional[RadioOperator] = None
        self._flight_attendants: List[FlightAttendant] = []
        self._is_formed = False

    @property
    def crew_id(self) -> str:
        return self._crew_id

    def add_pilot(self, pilot: Pilot):
        if len(self._pilots) < 2:
            self._pilots.append(pilot)
            pilot.is_available = False
            print(f"Пилот {pilot.name} добавлен в бригаду {self._crew_id}")
        else:
            print("В бригаде уже максимум пилотов (2)")

    def set_navigator(self, navigator: Navigator):
        self._navigator = navigator
        navigator.is_available = False
        print(f"Штурман {navigator.name} добавлен в бригаду {self._crew_id}")

    def set_radio_operator(self, radio_operator: RadioOperator):
        self._radio_operator = radio_operator
        radio_operator.is_available = False
        print(f"Радист {radio_operator.name} добавлен в бригаду {self._crew_id}")

    def add_flight_attendant(self, flight_attendant: FlightAttendant):
        self._flight_attendants.append(flight_attendant)
        flight_attendant.is_available = False
        print(f"Бортпроводник {flight_attendant.name} добавлен в бригаду {self._crew_id}")

    def is_complete(self) -> bool:
        #Проверка полноты бригады
        has_commander = any(p.is_commander for p in self._pilots)
        return (len(self._pilots) == 2 and has_commander and
                self._navigator is not None and
                self._radio_operator is not None and
                len(self._flight_attendants) >= 1)

    def get_commander(self) -> Optional[Pilot]:
        for pilot in self._pilots:
            if pilot.is_commander:
                return pilot
        return None

    def get_pilots_count(self) -> int:
        return len(self._pilots)

    def get_attendants_count(self) -> int:
        return len(self._flight_attendants)

    def __str__(self):
        members = []
        members.extend([str(p) for p in self._pilots])
        if self._navigator:
            members.append(str(self._navigator))
        if self._radio_operator:
            members.append(str(self._radio_operator))
        members.extend([str(fa) for fa in self._flight_attendants])
        return f"\nБригада {self._crew_id}:\n" + "\n".join(members)


# 5. АССОЦИАЦИЯ (Association)

@dataclass
class FlightData:
    #Данные рейса
    flight_number: str
    departure_airport: Airport
    destination_airport: Airport
    scheduled_time: datetime
    aircraft: Aircraft


class Flight:
    """Класс рейса.
    Ассоциации:
    - с Airport (аэропорты отлета и назначения)
    - с Crew (летная бригада)
    - с Aircraft (самолет)"""

    def __init__(self, data: FlightData):
        self._flight_number = data.flight_number
        self._departure_airport = data.departure_airport
        self._destination_airport = data.destination_airport
        self._scheduled_time = data.scheduled_time
        self._aircraft = data.aircraft
        self._crew: Optional[Crew] = None
        self._passengers: List[Passenger] = []
        self._status = "Запланирован"
        self._emergency_airport: Optional[Airport] = None

    @property
    def flight_number(self) -> str:
        return self._flight_number

    @property
    def status(self) -> str:
        return self._status

    def assign_crew(self, crew: Crew):
        #Назначение летной бригады на рейс
        if not crew.is_complete():
            print(f"Бригада {crew.crew_id} неполная!")
            return False

        self._crew = crew
        print(f"Бригада назначена на рейс {self._flight_number}")
        return True

    def add_passenger(self, passenger: Passenger):
        if len(self._passengers) < self._aircraft.capacity:
            self._passengers.append(passenger)
            print(f"Пассажир {passenger.name} добавлен на рейс {self._flight_number}")
        else:
            print(f"Рейс {self._flight_number} полностью забронирован!")

    def check_weather_conditions(self) -> bool:
        #Проверка погодных условий в аэропортах
        departure_ok = self._departure_airport.is_flight_possible()
        destination_ok = self._destination_airport.is_flight_possible()

        if not departure_ok:
            print(f"Рейс {self._flight_number} ОТМЕНЕН: плохая погода в {self._departure_airport.code}")
            self._status = "Отменен (погода в пункте отлета)"
            return False

        if not destination_ok:
            print(f"Рейс {self._flight_number} ОТМЕНЕН: плохая погода в {self._destination_airport.code}")
            self._status = "Отменен (погода в пункте назначения)"
            return False

        return True

    def handle_emergency(self, issue: str):
        #Обработка аварийной ситуации в полете
        print(f"АВАРИЙНАЯ СИТУАЦИЯ на рейсе {self._flight_number}: {issue}")

        # Поиск ближайшего аэропорта для экстренной посадки
        emergency_airport = Airport(AirportData("SVO", "Шереметьево", "Москва", "Россия", "Хорошая"))
        print(f"Рейс {self._flight_number} меняет маршрут!")
        print(f"Было: {self._destination_airport.city}")
        self._destination_airport = emergency_airport
        print(f"Стало: {self._destination_airport.city} (экстренная посадка)")
        self._status = "Изменен (технические неисправности)"
        self._emergency_airport = emergency_airport

    def execute_flight(self):
        #Выполнение рейса
        if self._status.startswith("Отменен"):
            print(f"Рейс {self._flight_number} отменен и не может быть выполнен")
            return

        if not self._crew:
            print("Нет назначенной бригады!")
            return


        print(f"ВЫПОЛНЕНИЕ РЕЙСА {self._flight_number}")
        print(f"Маршрут: {self._departure_airport.city} -> {self._destination_airport.city}")
        print(f"Самолет: {self._aircraft}")
        print(f"Пассажиров: {len(self._passengers)}")
        print(f"Экипаж: {self._crew.get_pilots_count()} пилотов, "
              f"{self._crew.get_attendants_count()} бортпроводников")

        self._aircraft.take_off()
        print(f"Рейс {self._flight_number} в полете...")

        self._aircraft.land()
        self._status = "Выполнен"
        print(f"Рейс {self._flight_number} успешно завершен")

    def cancel(self, reason: str):
        #Отмена рейса#
        self._status = f"Отменен ({reason})"
        print(f"Рейс {self._flight_number} отменен. Причина: {reason}")

    def __str__(self):
        return (f"Рейс {self._flight_number}: {self._departure_airport.city} -> "
                f"{self._destination_airport.city}, Статус: {self._status}")


# 6. КЛАСС-АДМИНИСТРАТОР

@dataclass
class AdministratorData:
    #Данные администратора
    name: str
    admin_id: str


class Administrator:
    #Класс администратора, управляющего системой
    #Агрегация с Flight (создает рейсы)

    def __init__(self, data: AdministratorData):
        self._name = data.name
        self._admin_id = data.admin_id
        self._flights: List[Flight] = []
        self._crews: List[Crew] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def admin_id(self) -> str:
        return self._admin_id

    def create_flight(self, data: FlightData) -> Flight:
        #Создание нового рейса
        new_flight = Flight(data)
        self._flights.append(new_flight)
        print(f"Администратор {self._name} создал рейс {data.flight_number}")
        return new_flight

    def form_crew(self, crew_id: str) -> Crew:
        #Формирование летной бригады
        new_crew = Crew(crew_id)
        self._crews.append(new_crew)
        print(f"Администратор {self._name} начал формирование бригады {crew_id}")
        return new_crew

    def assign_crew_to_flight(self, crew: Crew, current_flight: Flight):
        #Назначение бригады на рейс
        if current_flight.assign_crew(crew):
            print(f"Администратор назначил бригаду на рейс {current_flight.flight_number}")

    def cancel_flight(self, current_flight: Flight, reason: str):
        #Отмена рейса
        current_flight.cancel(reason)
        print(f"Администратор отменил рейс {current_flight.flight_number}. Причина: {reason}")

    def get_flight_status(self, current_flight: Flight):
        print(f"Статус рейса {current_flight.flight_number}: {current_flight.status}")

    def get_all_flights(self) -> List[Flight]:
        return self._flights


# ДЕМОНСТРАЦИЯ РАБОТЫ

print("СИСТЕМА УПРАВЛЕНИЯ АЭРОФЛОТ")
print("Демонстрация ООП отношений: Обобщение, Агрегация, Ассоциация, Реализация")

# 1. Создание аэропортов
print("\n1. СОЗДАНИЕ АЭРОПОРТОВ (Агрегация)\n")
airport_svo = Airport(AirportData("SVO", "Шереметьево", "Москва", "Россия", "Хорошая"))
airport_led = Airport(AirportData("LED", "Пулково", "Санкт-Петербург", "Россия", "Хорошая"))
airport_sochi = Airport(AirportData("AER", "Адлер", "Сочи", "Россия", "Шторм"))

print(f"Аэропорт 1: {airport_svo}")
print(f"Аэропорт 2: {airport_led}")
print(f"Аэропорт 3: {airport_sochi} (погода: {airport_sochi.weather_condition})")

# 2. Создание самолетов
print("\n2. СОЗДАНИЕ САМОЛЕТОВ (Реализация интерфейса Flyable)\n")
aircraft1 = Aircraft(AircraftData("RA-89001", "Sukhoi Superjet 100", 98, 4578, "Sukhoi"))
aircraft2 = Aircraft(AircraftData("RA-89002", "Boeing 737-800", 189, 5765, "Boeing"))
print(aircraft1)
print(aircraft2)

# 3. Создание сотрудников
print("\n3. СОЗДАНИЕ СОТРУДНИКОВ (Обобщение - наследование)\n")

# Пилоты
commander_data = PilotData(
    EmployeeData(PersonData("Иванов Иван Иванович", "123456", 45), "P001", 20),
    "ATPL-RUS-001", True
)
commander = Pilot(commander_data)

copilot_data = PilotData(
    EmployeeData(PersonData("Петров Петр Петрович", "654321", 35), "P002", 10),
    "ATPL-RUS-002", False
)
copilot = Pilot(copilot_data)

# Другие члены экипажа
navigator_data = NavigatorData(
    EmployeeData(PersonData("Сидоров Сидор Сидорович", "111222", 40), "N001", 15),
    "NAV-001"
)
navigator = Navigator(navigator_data)

radio_data = RadioOperatorData(
    EmployeeData(PersonData("Козлов Козьма Козьмич", "333444", 38), "R001", 12),
    "RAD-001"
)
radio_operator = RadioOperator(radio_data)

stewardess1_data = FlightAttendantData(
    EmployeeData(PersonData("Смирнова Анна Сергеевна", "555666", 28), "F001", 5),
    ["Русский", "Английский", "Французский"]
)
stewardess1 = FlightAttendant(stewardess1_data)

stewardess2_data = FlightAttendantData(
    EmployeeData(PersonData("Кузнецова Мария Ивановна", "777888", 26), "F002", 3),
    ["Русский", "Английский"]
)
stewardess2 = FlightAttendant(stewardess2_data)

print(commander)
print(copilot)
print(navigator)
print(radio_operator)
print(stewardess1)
print(stewardess2)

# 4. Создание администратора
print("\n4. СОЗДАНИЕ АДМИНИСТРАТОРА\n")
admin_data = AdministratorData("Алексеев Алексей Алексеевич", "A001")
admin = Administrator(admin_data)
print(f"Администратор: {admin.name} (ID: {admin.admin_id})")

# 5. Формирование летной бригады
print("\n5. ФОРМИРОВАНИЕ ЛЕТНОЙ БРИГАДЫ (Композиция)\n")
crew = admin.form_crew("CREW-001")
crew.add_pilot(commander)
crew.add_pilot(copilot)
crew.set_navigator(navigator)
crew.set_radio_operator(radio_operator)
crew.add_flight_attendant(stewardess1)
crew.add_flight_attendant(stewardess2)

print(f"\nБригада сформирована: {crew.is_complete()}")
print(crew)

# 6. Создание рейса
print("\n6. СОЗДАНИЕ РЕЙСА (Ассоциация)\n")
flight_time = datetime(2024, 12, 25, 14, 30)
flight1_data = FlightData("SU-100", airport_svo, airport_led, flight_time, aircraft1)
flight1 = admin.create_flight(flight1_data)
admin.assign_crew_to_flight(crew, flight1)

# Добавление пассажиров
passenger1_data = PassengerData(
    PersonData("Васильев Василий", "444555", 30),
    "MP123456", "TKT001"
)
passenger1 = Passenger(passenger1_data)

passenger2_data = PassengerData(
    PersonData("Николаева Елена", "666777", 25),
    "MP789012", "TKT002"
)
passenger2 = Passenger(passenger2_data)

flight1.add_passenger(passenger1)
flight1.add_passenger(passenger2)

# 7. Проверка погоды и выполнение рейса
print("\n7. ПРОВЕРКА ПОГОДНЫХ УСЛОВИЙ\n")
if flight1.check_weather_conditions():
    flight1.execute_flight()

# 8. Демонстрация отмены рейса из-за погоды
print("\n8. ДЕМОНСТРАЦИЯ ОТМЕНЫ РЕЙСА ИЗ-ЗА ПОГОДЫ\n")
flight2_data = FlightData("SU-200", airport_svo, airport_sochi, flight_time, aircraft2)
flight2 = admin.create_flight(flight2_data)
flight2.check_weather_conditions()

# 9. Демонстрация изменения маршрута
print("\n9. ДЕМОНСТРАЦИЯ ИЗМЕНЕНИЯ МАРШРУТА В ПОЛЕТЕ\n")
airport_kzn = Airport(AirportData("KZN", "Казань", "Казань", "Россия", "Хорошая"))
flight3_data = FlightData("SU-300", airport_svo, airport_kzn, flight_time, aircraft1)
flight3 = admin.create_flight(flight3_data)

# Новая бригада
commander2_data = PilotData(
    EmployeeData(PersonData("Федоров Федор", "999000", 50), "P003", 25),
    "ATPL-003", True
)
commander2 = Pilot(commander2_data)

crew2 = admin.form_crew("CREW-002")
crew2.add_pilot(commander2)

pilot2_data = PilotData(
    EmployeeData(PersonData("Морозов Мороз", "112233", 32), "P004", 8),
    "ATPL-004", False
)
crew2.add_pilot(Pilot(pilot2_data))

navigator2_data = NavigatorData(
    EmployeeData(PersonData("Волков Волк", "445566", 42), "N002", 18),
    "NAV-002"
)
crew2.set_navigator(Navigator(navigator2_data))

radio2_data = RadioOperatorData(
    EmployeeData(PersonData("Лисицын Лис", "778899", 36), "R002", 11),
    "RAD-002"
)
crew2.set_radio_operator(RadioOperator(radio2_data))

attendant2_data = FlightAttendantData(
    EmployeeData(PersonData("Медведева Медведия", "121212", 29), "F003", 6),
    ["Русский"]
)
crew2.add_flight_attendant(FlightAttendant(attendant2_data))

admin.assign_crew_to_flight(crew2, flight3)

if flight3.check_weather_conditions():
    print(f"\nРейс {flight3.flight_number} начал выполнение...")
    aircraft1.take_off()
    print("В полете...")

    # Командир сообщает о неисправности
    commander2.report_technical_issue("Отказ двигателя №2", flight3)

    aircraft1.land()

# 10. Итоговая сводка
print("\nИТОГОВАЯ СВОДКА ПО РЕЙСАМ")
for fl in admin.get_all_flights():
    print(f"• {fl}")

print("\n\nСИСТЕМА ЗАВЕРШИЛА РАБОТУ")

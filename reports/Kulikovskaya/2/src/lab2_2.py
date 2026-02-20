from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from enum import Enum


class Person(ABC):
    def __init__(self, name: str, id_number: str, age: int):
        self._name = name
        self._id_number = id_number
        self._age = age

    @property
    def name(self) -> str:
        return self._name

    @property
    def id_number(self) -> str:
        return self._id_number

    @abstractmethod
    def get_role(self) -> str:
        #Абстрактный метод - реализация
        pass

    def __str__(self) -> str:
        return f"{self._name} (ID: {self._id_number}), {self._age} лет"


class Employee(Person):
    def __init__(self, name: str, id_number: str, age: int,
                 employee_id: str, experience_years: int):
        super().__init__(name, id_number, age)
        self._employee_id = employee_id
        self._experience_years = experience_years
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
        return "сотрудник аэрофлота"

    def __str__(self) -> str:
        return f"{super().__str__()}, Таб. №: {self._employee_id}, стаж: {self._experience_years} лет"


# Специализации сотрудников (дополнительное обобщение)
class Pilot(Employee):
    #класс пилота
    def __init__(self, name: str, id_number: str, age: int,
                 employee_id: str, experience_years: int, license_number: str,
                 is_commander: bool = False):
        super().__init__(name, id_number, age, employee_id, experience_years)
        self._license_number = license_number
        self._is_commander = is_commander
        self._flight_hours = 0

    @property
    def is_commander(self) -> bool:
        return self._is_commander

    def report_technical_issue(self, issue: str, flight: 'Flight'):
        #командир сообщает о технических неисправностях
        if self._is_commander:
            print(f"КОМАНДИР {self._name}: сообщает о неисправности: {issue}")
            flight.handle_emergency(issue)
        else:
            print(f"пилот {self._name} не является командиром")

    def get_role(self) -> str:
        return "командир воздушного судна" if self._is_commander else "второй пилот"

    def __str__(self) -> str:
        role = "командир" if self._is_commander else "второй пилот"
        return f"{role}: {super().__str__()}, лицензия: {self._license_number}"


class Navigator(Employee):
    #класс штурмана
    def __init__(self, name: str, id_number: str, age: int,
                 employee_id: str, experience_years: int, navigation_cert: str):
        super().__init__(name, id_number, age, employee_id, experience_years)
        self._navigation_cert = navigation_cert

    def get_role(self) -> str:
        return "штурман"

    def __str__(self):
        return f"штурман: {super().__str__()}"


class RadioOperator(Employee):
    #класс радиста
    def __init__(self, name: str, id_number: str, age: int,
                 employee_id: str, experience_years: int, radio_license: str):
        super().__init__(name, id_number, age, employee_id, experience_years)
        self._radio_license = radio_license

    def get_role(self) -> str:
        return "радист"

    def __str__(self):
        return f"радист: {super().__str__()}"


class FlightAttendant(Employee):
    #класс стюардессы
    def __init__(self, name: str, id_number: str, age: int,
                 employee_id: str, experience_years: int, languages: List[str]):
        super().__init__(name, id_number, age, employee_id, experience_years)
        self._languages = languages

    def get_role(self) -> str:
        return "бортпроводник"

    def __str__(self):
        return f"бортпроводник: {super().__str__()}, языки: {', '.join(self._languages)}"


class Passenger(Person):
    #класс пассажира

    def __init__(self, name: str, id_number: str, age: int,
                 passport: str, ticket_number: str):
        super().__init__(name, id_number, age)
        self._passport = passport
        self._ticket_number = ticket_number

    def get_role(self) -> str:
        return "пассажир"

    def __str__(self):
        return f"пассажир: {super().__str__()}, паспорт: {self._passport}"


class Flyable(ABC):

    @abstractmethod
    def take_off(self):
        pass

    @abstractmethod
    def land(self):
        pass

    @abstractmethod
    def get_flight_range(self) -> float:
        pass


class Aircraft(Flyable):
    def __init__(self, registration: str, model: str, capacity: int,
                 flight_range: float, manufacturer: str):
        self._registration = registration
        self._model = model
        self._capacity = capacity
        self._flight_range = flight_range
        self._manufacturer = manufacturer
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
        print(f"самолет {self._model} ({self._registration}) взлетает")

    def land(self):
        print(f"самолет {self._model} ({self._registration}) приземляется")

    def get_flight_range(self) -> float:
        return self._flight_range

    def __str__(self):
        return (f"самолет {self._model} [{self._registration}], "
                f"вместимость: {self._capacity}, дальность: {self._flight_range} км")


class Airport:
    def __init__(self, code: str, name: str, city: str, country: str,
                 weather_condition: str = "хорошая"):
        self._code = code
        self._name = name
        self._city = city
        self._country = country
        self._weather_condition = weather_condition
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
        if value in ["шторм", "туман", "снегопад", "гроза"]:
            print(f"внимание! в аэропорту {self._code} ухудшение погоды: {value}")

    def is_flight_possible(self) -> bool:
        #проверка возможности полета из-за погоды
        bad_weather = ["шторм", "туман", "снегопад", "гроза"]
        return self._weather_condition not in bad_weather

    def __str__(self):
        return f"{self._name} ({self._code}), {self._city}, {self._country}"


class Crew:

    def __init__(self, crew_id: str):
        self._crew_id = crew_id
        self._pilots: List[Pilot] = []
        self._navigator: Optional[Navigator] = None
        self._radio_operator: Optional[RadioOperator] = None
        self._flight_attendants: List[FlightAttendant] = []
        self._is_formed = False

    def add_pilot(self, pilot: Pilot):
        if len(self._pilots) < 2:
            self._pilots.append(pilot)
            pilot.is_available = False
            print(f"пилот {pilot.name} добавлен в бригаду {self._crew_id}")
        else:
            print("в бригаде уже максимум пилотов (2)")

    def set_navigator(self, navigator: Navigator):
        self._navigator = navigator
        navigator.is_available = False
        print(f"штурман {navigator.name} добавлен в бригаду {self._crew_id}")

    def set_radio_operator(self, radio_operator: RadioOperator):
        self._radio_operator = radio_operator
        radio_operator.is_available = False
        print(f"радист {radio_operator.name} добавлен в бригаду {self._crew_id}")

    def add_flight_attendant(self, flight_attendant: FlightAttendant):
        self._flight_attendants.append(flight_attendant)
        flight_attendant.is_available = False
        print(f"бортпроводник {flight_attendant.name} добавлен в бригаду {self._crew_id}")

    def is_complete(self) -> bool:
        #проверка полноты бригады
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

    def __str__(self):
        members = []
        members.extend([str(p) for p in self._pilots])
        if self._navigator:
            members.append(str(self._navigator))
        if self._radio_operator:
            members.append(str(self._radio_operator))
        members.extend([str(fa) for fa in self._flight_attendants])
        return f"\nбригада {self._crew_id}:\n" + "\n".join(members)


class Flight:

    def __init__(self, flight_number: str, departure_airport: Airport,
                 destination_airport: Airport, scheduled_time: datetime,
                 aircraft: Aircraft):
        self._flight_number = flight_number
        self._departure_airport = departure_airport
        self._destination_airport = destination_airport
        self._scheduled_time = scheduled_time
        self._aircraft = aircraft
        self._crew: Optional[Crew] = None
        self._passengers: List[Passenger] = []
        self._status = "запланирован"
        self._emergency_airport: Optional[Airport] = None

    @property
    def flight_number(self) -> str:
        return self._flight_number

    @property
    def status(self) -> str:
        return self._status

    def assign_crew(self, crew: Crew):
        #назначение летной бригады на рейс
        if not crew.is_complete():
            print(f"бригада {crew._crew_id} неполная!")
            return False

        self._crew = crew
        print(f"бригада назначена на рейс {self._flight_number}")
        return True

    def add_passenger(self, passenger: Passenger):
        if len(self._passengers) < self._aircraft.capacity:
            self._passengers.append(passenger)
            print(f"пассажир {passenger.name} добавлен на рейс {self._flight_number}")
        else:
            print(f"рейс {self._flight_number} полностью забронирован!")

    def check_weather_conditions(self) -> bool:
        """проверка погодных условий в аэропортах"""
        departure_ok = self._departure_airport.is_flight_possible()
        destination_ok = self._destination_airport.is_flight_possible()

        if not departure_ok:
            print(f"рейс {self._flight_number} ОТМЕНЕН: плохая погода в {self._departure_airport.code}")
            self._status = "Отменен (погода в пункте отлета)"
            return False

        if not destination_ok:
            print(f"рейс {self._flight_number} ОТМЕНЕН: плохая погода в {self._destination_airport.code}")
            self._status = "отменен (погода в пункте назначения)"
            return False

        return True

    def handle_emergency(self, issue: str):
        #обработка аварийной ситуации в полете
        print(f"АВАРИЙНАЯ СИТУАЦИЯ на рейсе {self._flight_number}: {issue}")

        # Поиск ближайшего аэропорта для экстренной посадки
        emergency_airport = Airport("SVO", "Шереметьево", "Москва", "Россия", "Хорошая")
        print(f"рейс {self._flight_number} меняет маршрут!")
        print(f"было: {self._destination_airport.city}")
        self._destination_airport = emergency_airport
        print(f"стало: {self._destination_airport.city} (экстренная посадка)")
        self._status = "изменен (технические неисправности)"
        self._emergency_airport = emergency_airport

    def execute_flight(self):
        #выполнение рейса
        if self._status.startswith("Отменен"):
            print(f"рейс {self._flight_number} отменен и не может быть выполнен")
            return

        if not self._crew:
            print(f"нет назначенной бригады!")
            return

        print(f"\n{'=' * 60}")
        print(f"ВЫПОЛНЕНИЕ РЕЙСА {self._flight_number}")
        print(f"{'=' * 60}")
        print(f"Маршрут: {self._departure_airport.city} -> {self._destination_airport.city}")
        print(f"Самолет: {self._aircraft}")
        print(f"Пассажиров: {len(self._passengers)}")
        print(f"Экипаж: {len(self._crew._pilots)} пилотов, "
              f"{len(self._crew._flight_attendants)} бортпроводников")

        self._aircraft.take_off()
        print(f"рейс {self._flight_number} в полете...")

        # симуляция возможной технической неисправности
        self._aircraft.land()
        self._status = "Выполнен"
        print(f"рейс {self._flight_number} успешно завершен")

    def __str__(self):
        return (f"рейс {self._flight_number}: {self._departure_airport.city} -> "
                f"{self._destination_airport.city}, статус: {self._status}")


class Administrator:

    def __init__(self, name: str, admin_id: str):
        self._name = name
        self._admin_id = admin_id
        self._flights: List[Flight] = []
        self._crews: List[Crew] = []

    def create_flight(self, flight_number: str, departure: Airport,
                      destination: Airport, time: datetime, aircraft: Aircraft) -> Flight:
        #создание нового рейса
        flight = Flight(flight_number, departure, destination, time, aircraft)
        self._flights.append(flight)
        print(f"администратор {self._name} создал рейс {flight_number}")
        return flight

    def form_crew(self, crew_id: str) -> Crew:
        #формирование летной бригады
        crew = Crew(crew_id)
        self._crews.append(crew)
        print(f"администратор {self._name} начал формирование бригады {crew_id}")
        return crew

    def assign_crew_to_flight(self, crew: Crew, flight: Flight):
        #назначение бригады на рейс"""
        if flight.assign_crew(crew):
            print(f"администратор назначил бригаду на рейс {flight.flight_number}")

    def cancel_flight(self, flight: Flight, reason: str):
        #отмена рейса"""
        flight._status = f"отменен ({reason})"
        print(f"администратор отменил рейс {flight.flight_number}. причина: {reason}")

    def get_flight_status(self, flight: Flight):
        print(f"статус рейса {flight.flight_number}: {flight.status}")


print("СИСТЕМА УПРАВЛЕНИЯ АЭРОФЛОТ")
print("демонстрация ООП отношений: Обобщение, Агрегация, Ассоциация, Реализация")
print("~" * 70)

# 1. Создание аэропортов (Агрегация)
print("\n1. СОЗДАНИЕ АЭРОПОРТОВ (Агрегация)")
print("-" * 50)
airport_svo = Airport("SVO", "Шереметьево", "Москва", "Россия", "Хорошая")
airport_led = Airport("LED", "Пулково", "Санкт-Петербург", "Россия", "Хорошая")
airport_sochi = Airport("AER", "Адлер", "Сочи", "Россия", "Шторм")

print(f"Аэропорт 1: {airport_svo}")
print(f"Аэропорт 2: {airport_led}")
print(f"Аэропорт 3: {airport_sochi} (погода: {airport_sochi.weather_condition})")

# 2. Создание самолетов (Реализация интерфейса Flyable)
print("\n2. СОЗДАНИЕ САМОЛЕТОВ (Реализация интерфейса Flyable)")
print("-" * 50)
aircraft1 = Aircraft("RA-89001", "Sukhoi Superjet 100", 98, 4578, "Sukhoi")
aircraft2 = Aircraft("RA-89002", "Boeing 737-800", 189, 5765, "Boeing")
print(aircraft1)
print(aircraft2)

# 3. Создание сотрудников (Обобщение/Наследование)
print("\n3. СОЗДАНИЕ СОТРУДНИКОВ (Обобщение - наследование от Person и Employee)")
print("-" * 50)

# Пилоты
commander = Pilot("Иванов Иван Иванович", "123456", 45, "P001", 20,
                  "ATPL-RUS-001", is_commander=True)
copilot = Pilot("Петров Петр Петрович", "654321", 35, "P002", 10,
                "ATPL-RUS-002", is_commander=False)

# Другие члены экипажа
navigator = Navigator("Сидоров Сидор Сидорович", "111222", 40, "N001", 15, "NAV-001")
radio_operator = RadioOperator("Козлов Козьма Козьмич", "333444", 38, "R001", 12, "RAD-001")
stewardess1 = FlightAttendant("Смирнова Анна Сергеевна", "555666", 28, "F001", 5,
                              ["Русский", "Английский", "Французский"])
stewardess2 = FlightAttendant("Кузнецова Мария Ивановна", "777888", 26, "F002", 3,
                              ["Русский", "Английский"])

print(commander)
print(copilot)
print(navigator)
print(radio_operator)
print(stewardess1)
print(stewardess2)

# 4. Создание администратора
print("\n4. СОЗДАНИЕ АДМИНИСТРАТОРА")
print("-" * 50)
admin = Administrator("Алексеев Алексей Алексеевич", "A001")
print(f"Администратор: {admin._name} (ID: {admin._admin_id})")

# 5. Формирование летной бригады (Композиция)
print("\n5. ФОРМИРОВАНИЕ ЛЕТНОЙ БРИГАДЫ (Композиция)")
print("-" * 50)
crew = admin.form_crew("CREW-001")
crew.add_pilot(commander)
crew.add_pilot(copilot)
crew.set_navigator(navigator)
crew.set_radio_operator(radio_operator)
crew.add_flight_attendant(stewardess1)
crew.add_flight_attendant(stewardess2)

print(f"\nБригада сформирована: {crew.is_complete()}")
print(crew)

# 6. Создание рейса (Ассоциация)
print("\n6. СОЗДАНИЕ РЕЙСА (Ассоциация с Airport, Aircraft, Crew)")
print("-" * 50)
flight_time = datetime(2024, 12, 25, 14, 30)
flight1 = admin.create_flight("SU-100", airport_svo, airport_led, flight_time, aircraft1)
admin.assign_crew_to_flight(crew, flight1)

# Добавление пассажиров
passenger1 = Passenger("Васильев Василий", "444555", 30, "MP123456", "TKT001")
passenger2 = Passenger("Николаева Елена", "666777", 25, "MP789012", "TKT002")
flight1.add_passenger(passenger1)
flight1.add_passenger(passenger2)

# 7. Проверка погоды и выполнение рейса
print("\n7. ПРОВЕРКА ПОГОДНЫХ УСЛОВИЙ")
print("-" * 50)
if flight1.check_weather_conditions():
    flight1.execute_flight()

# 8. Демонстрация отмены рейса из-за погоды
print("\n8. ДЕМОНСТРАЦИЯ ОТМЕНЫ РЕЙСА ИЗ-ЗА ПОГОДЫ")
print("-" * 50)
flight2 = admin.create_flight("SU-200", airport_svo, airport_sochi, flight_time, aircraft2)
# Проверка автоматически отменит рейс из-за шторма в Сочи
flight2.check_weather_conditions()

# 9. Демонстрация изменения маршрута из-за технических неисправностей
print("\n9. ДЕМОНСТРАЦИЯ ИЗМЕНЕНИЯ МАРШРУТА В ПОЛЕТЕ")
print("-" * 50)
# Создадим новый рейс с хорошей погодой
airport_kzn = Airport("KZN", "Казань", "Казань", "Россия", "Хорошая")
flight3 = admin.create_flight("SU-300", airport_svo, airport_kzn, flight_time, aircraft1)

# Новая бригада для этого рейса
commander2 = Pilot("Федоров Федор", "999000", 50, "P003", 25, "ATPL-003", True)
crew2 = admin.form_crew("CREW-002")
crew2.add_pilot(commander2)
crew2.add_pilot(Pilot("Морозов Мороз", "112233", 32, "P004", 8, "ATPL-004", False))
crew2.set_navigator(Navigator("Волков Волк", "445566", 42, "N002", 18, "NAV-002"))
crew2.set_radio_operator(RadioOperator("Лисицын Лис", "778899", 36, "R002", 11, "RAD-002"))
crew2.add_flight_attendant(FlightAttendant("Медведева Медведь", "121212", 29, "F003", 6, ["Русский"]))

admin.assign_crew_to_flight(crew2, flight3)

# Выполняем рейс
if flight3.check_weather_conditions():
    print(f"\nРейс {flight3.flight_number} начал выполнение...")
    aircraft1.take_off()
    print("В полете...")

    # Командир сообщает о неисправности
    commander2.report_technical_issue("Отказ двигателя №2", flight3)

    # Рейс приземляется в альтернативном аэропорту
    aircraft1.land()

# 10. Итоговая сводка
print("\n" + "=" * 70)
print("ИТОГОВАЯ СВОДКА ПО РЕЙСАМ")
print("=" * 70)
for flight in admin._flights:
    print(f"• {flight}")

print("\n" + "=" * 70)
print("СИСТЕМА ЗАВЕРШИЛА РАБОТУ")
print("=" * 70)

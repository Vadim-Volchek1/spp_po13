from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class TransportType(Enum):
    """Типы транспорта для проезда"""

    ECONOMY = "Эконом (автобус)"
    STANDARD = "Стандарт (поезд)"
    BUSINESS = "Бизнес (самолет)"
    LUXURY = "Люкс (индивидуальный трансфер)"


class AccommodationType(Enum):
    """Типы проживания"""

    HOSTEL = "Хостел"
    HOTEL_3_STARS = "Отель 3 звезды"
    HOTEL_4_STARS = "Отель 4 звезды"
    HOTEL_5_STARS = "Отель 5 звезд"
    APARTMENTS = "Апартаменты"


class MealType(Enum):
    """Типы питания"""

    WITHOUT_MEALS = "Без питания"
    BREAKFAST_ONLY = "Только завтраки"
    HALF_BOARD = "Полупансион (завтрак + ужин)"
    FULL_BOARD = "Полный пансион (3-разовое)"
    ALL_INCLUSIVE = "Все включено"


class TourPackage:
    """
    Класс туристического пакета (продукт)
    """

    def __init__(self):
        self._transport = None
        self._accommodation = None
        self._meal = None
        self._excursions: List[str] = []
        self._museums: List[str] = []
        self._additional_services: List[str] = []

    def set_transport(self, transport: TransportType, price: float):
        self._transport = {"type": transport, "price": price}

    def set_accommodation(
        self, accommodation: AccommodationType, nights: int, price_per_night: float
    ):
        self._accommodation = {
            "type": accommodation,
            "nights": nights,
            "price_per_night": price_per_night,
        }

    def set_meal(self, meal: MealType, price: float):
        self._meal = {"type": meal, "price": price}

    def add_excursion(self, name: str, price: float):
        self._excursions.append({"name": name, "price": price})

    def add_museum(self, name: str, price: float):
        self._museums.append({"name": name, "price": price})

    def add_service(self, name: str, price: float):
        self._additional_services.append({"name": name, "price": price})

    def calculate_total_cost(self) -> float:
        """Расчет общей стоимости тура"""
        total = 0

        # Проезд
        if self._transport:
            total += self._transport["price"]

        # Проживание
        if self._accommodation:
            total += (
                self._accommodation["nights"] * self._accommodation["price_per_night"]
            )

        # Питание
        if self._meal:
            total += self._meal["price"]

        # Экскурсии
        for excursion in self._excursions:
            total += excursion["price"]

        # Музеи
        for museum in self._museums:
            total += museum["price"]

        # Доп. услуги
        for service in self._additional_services:
            total += service["price"]

        return total

    def __str__(self) -> str:
        """Строковое представление тура"""
        result = ["*" * 50, "ВАШ ТУРИСТИЧЕСКИЙ ПАКЕТ", "*" * 50]

        # Проезд
        if self._transport:
            result.append(f"\nПроезд: {self._transport['type'].value}")
            result.append(f"   Стоимость: {self._transport['price']} $")

        # Проживание
        if self._accommodation:
            result.append(f"\nПроживание: {self._accommodation['type'].value}")
            result.append(f"   Количество ночей: {self._accommodation['nights']}")
            result.append(
                f"   Стоимость за ночь: {self._accommodation['price_per_night']} $"
            )
            result.append(
                f"   Всего: {self._accommodation['nights'] * self._accommodation['price_per_night']} $"
            )

        # Питание
        if self._meal:
            result.append(f"\nПитание: {self._meal['type'].value}")
            result.append(f"   Стоимость: {self._meal['price']} $")

        # Экскурсии
        if self._excursions:
            result.append("\nЭкскурсии:")
            for e in self._excursions:
                result.append(f"   • {e['name']} - {e['price']} $")

        # Музеи
        if self._museums:
            result.append("\nПосещение музеев:")
            for m in self._museums:
                result.append(f"  {m['name']} - {m['price']} $")

        # Доп. услуги
        if self._additional_services:
            result.append("\nДополнительные услуги:")
            for s in self._additional_services:
                result.append(f"   • {s['name']} - {s['price']} $")

        result.append(f"\nИТОГОВАЯ СТОИМОСТЬ: {self.calculate_total_cost()} $")
        result.append("*" * 50)

        return "\n".join(result)


class TourBuilder(ABC):
    """
    Абстрактный строитель туров
    """

    def __init__(self):
        self._tour = None

    def create_new_tour(self):
        """Создание нового тура"""
        self._tour = TourPackage()

    @abstractmethod
    def build_transport(self):
        pass

    @abstractmethod
    def build_accommodation(self):
        pass

    @abstractmethod
    def build_meal(self):
        pass

    @abstractmethod
    def build_excursions(self):
        pass

    @abstractmethod
    def build_museums(self):
        pass

    @abstractmethod
    def build_additional_services(self):
        pass

    def get_tour(self) -> TourPackage:
        """Получение готового тура"""
        return self._tour


class EconomyTourBuilder(TourBuilder):
    """
    Строитель эконом-тура
    """

    def build_transport(self):
        self._tour.set_transport(TransportType.ECONOMY, 300)

    def build_accommodation(self):
        self._tour.set_accommodation(AccommodationType.HOSTEL, 5, 100)

    def build_meal(self):
        self._tour.set_meal(MealType.WITHOUT_MEALS, 0)

    def build_excursions(self):
        self._tour.add_excursion("Обзорная экскурсия по городу", 50)

    def build_museums(self):
        self._tour.add_museum("Краеведческий музей", 20)

    def build_additional_services(self):
        pass  # Нет доп. услуг в эконом-туре


class StandardTourBuilder(TourBuilder):
    """
    Строитель стандартного тура
    """

    def build_transport(self):
        self._tour.set_transport(TransportType.STANDARD, 1000)

    def build_accommodation(self):
        self._tour.set_accommodation(AccommodationType.HOTEL_3_STARS, 5, 250)

    def build_meal(self):
        self._tour.set_meal(MealType.BREAKFAST_ONLY, 200)

    def build_excursions(self):
        self._tour.add_excursion("Обзорная экскурсия по городу", 50)
        self._tour.add_excursion("Посещение центра с Эльфилевой башней", 80)

    def build_museums(self):
        self._tour.add_museum("Краеведческий музей", 20)
        self._tour.add_museum("Лувр (стандарт)", 30)

    def build_additional_services(self):
        self._tour.add_service("Встреча в аэропорту", 50)
        self._tour.add_service("Медицинская страховка", 50)


class LuxuryTourBuilder(TourBuilder):
    """
    Строитель люкс-тура
    """

    def build_transport(self):
        self._tour.set_transport(TransportType.LUXURY, 1500)

    def build_accommodation(self):
        self._tour.set_accommodation(AccommodationType.HOTEL_5_STARS, 7, 1000)

    def build_meal(self):
        self._tour.set_meal(MealType.ALL_INCLUSIVE, 1000)

    def build_excursions(self):
        self._tour.add_excursion("Индивидуальная экскурсия по городу", 500)
        self._tour.add_excursion("Винный тур с дегустацией", 300)
        self._tour.add_excursion("Морская прогулка на яхте", 1000)

    def build_museums(self):
        self._tour.add_museum("Лувр (VIP-билеты)", 300)
        self._tour.add_museum("Обзорная площадка на Эльфелевой башне", 200)

    def build_additional_services(self):
        self._tour.add_service("Индивидуальный гид", 800)
        self._tour.add_service("Спа-процедуры", 500)


class CustomTourBuilder(TourBuilder):
    """
    Строитель для кастомного тура (с возможностью выбора)
    """

    def __init__(self):
        super().__init__()
        self._transport_choice = None
        self._accommodation_choice = None
        self._meal_choice = None
        self._nights = 5
        self._selected_excursions = []
        self._selected_museums = []
        self._selected_services = []

    def set_transport_choice(self, transport: TransportType, price: float):
        self._transport_choice = (transport, price)

    def set_accommodation_choice(
        self, accommodation: AccommodationType, nights: int, price_per_night: float
    ):
        self._accommodation_choice = (accommodation, nights, price_per_night)

    def set_meal_choice(self, meal: MealType, price: float):
        self._meal_choice = (meal, price)

    def add_excursion_choice(self, name: str, price: float):
        self._selected_excursions.append((name, price))

    def add_museum_choice(self, name: str, price: float):
        self._selected_museums.append((name, price))

    def add_service_choice(self, name: str, price: float):
        self._selected_services.append((name, price))

    def build_transport(self):
        if self._transport_choice:
            transport, price = self._transport_choice
            self._tour.set_transport(transport, price)

    def build_accommodation(self):
        if self._accommodation_choice:
            accommodation, nights, price_per_night = self._accommodation_choice
            self._tour.set_accommodation(accommodation, nights, price_per_night)

    def build_meal(self):
        if self._meal_choice:
            meal, price = self._meal_choice
            self._tour.set_meal(meal, price)

    def build_excursions(self):
        for name, price in self._selected_excursions:
            self._tour.add_excursion(name, price)

    def build_museums(self):
        for name, price in self._selected_museums:
            self._tour.add_museum(name, price)

    def build_additional_services(self):
        for name, price in self._selected_services:
            self._tour.add_service(name, price)


class TourDirector:
    """
    Директор, управляющий процессом строительства
    """

    def __init__(self, builder: TourBuilder):
        self._builder = builder

    def construct_economy_tour(self):
        """Построение эконом-тура"""
        self._builder.create_new_tour()
        self._builder.build_transport()
        self._builder.build_accommodation()
        self._builder.build_meal()
        self._builder.build_excursions()
        self._builder.build_museums()
        self._builder.build_additional_services()
        return self._builder.get_tour()

    def construct_standard_tour(self):
        """Построение стандартного тура"""
        self._builder.create_new_tour()
        self._builder.build_transport()
        self._builder.build_accommodation()
        self._builder.build_meal()
        self._builder.build_excursions()
        self._builder.build_museums()
        self._builder.build_additional_services()
        return self._builder.get_tour()

    def construct_luxury_tour(self):
        """Построение люкс-тура"""
        self._builder.create_new_tour()
        self._builder.build_transport()
        self._builder.build_accommodation()
        self._builder.build_meal()
        self._builder.build_excursions()
        self._builder.build_museums()
        self._builder.build_additional_services()
        return self._builder.get_tour()

    def construct_custom_tour(self):
        """Построение кастомного тура"""
        self._builder.create_new_tour()
        self._builder.build_transport()
        self._builder.build_accommodation()
        self._builder.build_meal()
        self._builder.build_excursions()
        self._builder.build_museums()
        self._builder.build_additional_services()
        return self._builder.get_tour()


class TravelAgency:
    """
    Класс туристического агентства (клиент)
    """

    def __init__(self):
        self._available_excursions = [
            ("Обзорная экскурсия по городу", 50),
            ("Исторический центр", 80),
            ("Винный тур с дегустацией", 300),
            ("Морская прогулка", 1000),
            ("Ночная экскурсия", 100),
        ]

        self._available_museums = [
            ("Краеведческий музей", 20),
            ("Художественная галерея", 30),
            ("Лувр", 300),
            ("Обзорная площадка на Эльфелевой башне", 500),
        ]

        self._available_services = [
            ("Встреча в аэропорту", 100),
            ("Медицинская страховка", 50),
            ("Индивидуальный гид", 200),
            ("Спа-процедуры", 300),
            ("Фотосессия", 150),
        ]

    def show_menu(self):
        """Показать меню выбора тура"""
        print("\n" + "*" * 50)
        print("ДОБРО ПОЖАЛОВАТЬ В ТУРИСТИЧЕСКОЕ БЮРО")
        print("*" * 50)
        print("1. Готовый эконом-тур")
        print("2. Готовый стандартный тур")
        print("3. Готовый люкс-тур")
        print("4. Собрать свой тур")
        print("0. Выход")
        print("*" * 50)

    def create_custom_tour(self):
        """Создание кастомного тура"""
        builderFirst = CustomTourBuilder()
        director = TourDirector(builderFirst)

        print("\n--- СОЗДАНИЕ ИНДИВИДУАЛЬНОГО ТУРА ---")
        self.choice_mashinke(builderFirst)
        self.choice_hata(builderFirst)
        self.choice_pokushat(builderFirst)
        self.choice_excurs(builderFirst)
        self.choice_musei(builderFirst)
        self.choice_dop_uslugi(builderFirst)
        # Строим тур
        tour = director.construct_custom_tour()
        return tour

    # Выбор транспорта
    def choice_mashinke(self, builder):
        print("\nВыберите тип транспорта:")
        for i, transport in enumerate(TransportType, 1):
            price = {1: 150, 2: 300, 3: 800, 4: 1500}[i]
            print(f"{i}. {transport.value} - {price} $")

        transport_choice = int(input("Ваш выбор (1-4): "))
        transport = list(TransportType)[transport_choice - 1]
        transport_price = [150, 300, 800, 1500][transport_choice - 1]
        builder.set_transport_choice(transport, transport_price)

    # Выбор проживания
    def choice_hata(self, builder):
        print("\nВыберите тип проживания:")
        for i, accommodation in enumerate(AccommodationType, 1):
            price = {1: 80, 2: 150, 3: 250, 4: 500, 5: 300}[i]
            print(f"{i}. {accommodation.value} - {price} $/ночь")

        accommodation_choice = int(input("Ваш выбор (1-5): "))
        accommodation = list(AccommodationType)[accommodation_choice - 1]
        nights = int(input("Количество ночей: "))
        price_per_night = [80, 150, 250, 500, 300][accommodation_choice - 1]
        builder.set_accommodation_choice(accommodation, nights, price_per_night)

    # Выбор питания
    def choice_pokushat(self, builder):
        print("\nВыберите тип питания:")
        for i, meal in enumerate(MealType, 1):
            price = {1: 0, 2: 100, 3: 250, 4: 400, 5: 600}[i]
            print(f"{i}. {meal.value} - {price} $")

        meal_choice = int(input("Ваш выбор (1-5): "))
        meal = list(MealType)[meal_choice - 1]
        meal_price = [0, 100, 250, 400, 600][meal_choice - 1]
        builder.set_meal_choice(meal, meal_price)

    # Выбор экскурсий
    def choice_excurs(self, builder):
        print("\nДоступные экскурсии (введите номера через пробел, 0 - пропустить):")
        for i, (name, price) in enumerate(self._available_excursions, 1):
            print(f"{i}. {name} - {price} $")

        excursions_choice = input("Ваш выбор: ").strip()
        if excursions_choice != "0" and excursions_choice:
            for num in excursions_choice.split():
                idx = int(num) - 1
                if 0 <= idx < len(self._available_excursions):
                    name, price = self._available_excursions[idx]
                    builder.add_excursion_choice(name, price)

    # Выбор музеев
    def choice_musei(self, builder):
        print("\nДоступные музеи (введите номера через пробел, 0 - пропустить):")
        for i, (name, price) in enumerate(self._available_museums, 1):
            print(f"{i}. {name} - {price} $")

        museums_choice = input("Ваш выбор: ").strip()
        if museums_choice != "0" and museums_choice:
            for num in museums_choice.split():
                idx = int(num) - 1
                if 0 <= idx < len(self._available_museums):
                    name, price = self._available_museums[idx]
                    builder.add_museum_choice(name, price)

    # Выбор доп. услуг
    def choice_dop_uslugi(self, builder):
        print("\nДополнительные услуги (введите номера через пробел, 0 - пропустить):")
        for i, (name, price) in enumerate(self._available_services, 1):
            print(f"{i}. {name} - {price} $")

        services_choice = input("Ваш выбор: ").strip()
        if services_choice != "0" and services_choice:
            for num in services_choice.split():
                idx = int(num) - 1
                if 0 <= idx < len(self._available_services):
                    name, price = self._available_services[idx]
                    builder.add_service_choice(name, price)

    def run(self):
        """Запуск работы агентства"""
        while True:
            self.show_menu()
            choice = input("Выберите действие: ")

            if choice == "0":
                self._handle_exit()
                break

            self._process_tour_choice(choice)

    def _handle_exit(self):
        """Обработка выхода"""
        print("Спасибо за обращение! До свидания!")

    def _process_tour_choice(self, choice):
        """Обработка выбора тура"""
        tour = None

        if choice == "1":
            tour = self._create_economy_tour()
        elif choice == "2":
            tour = self._create_standard_tour()
        elif choice == "3":
            tour = self._create_luxury_tour()
        elif choice == "4":
            tour = self.create_custom_tour()

        if tour:
            self._handle_tour_result(tour)

    def _create_economy_tour(self):
        """Создание эконом тура"""
        builder = EconomyTourBuilder()
        director = TourDirector(builder)
        tour = director.construct_economy_tour()
        print("\nСформирован эконом-тур:")
        return tour

    def _create_standard_tour(self):
        """Создание стандартного тура"""
        builder = StandardTourBuilder()
        director = TourDirector(builder)
        tour = director.construct_standard_tour()
        print("\nСформирован стандартный тур:")
        return tour

    def _create_luxury_tour(self):
        """Создание люкс тура"""
        builder = LuxuryTourBuilder()
        director = TourDirector(builder)
        tour = director.construct_luxury_tour()
        print("\nСформирован люкс-тур:")
        return tour

    def _handle_tour_result(self, tour):
        """Обработка результата тура"""
        print(tour)

        confirm = input("\nЖелаете оформить тур? (да/нет): ")
        if confirm.lower() == "да":
            print("Тур успешно оформлен! Приятного отдыха!")
        else:
            print("Оформление отменено")


if __name__ == "__main__":
    agency = TravelAgency()
    agency.run()

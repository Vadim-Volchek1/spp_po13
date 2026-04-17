from abc import ABC, abstractmethod
from enum import Enum
import time
import threading
import random
from queue import Queue, Empty


class MusicGenre(Enum):
    ROCK = "Рок"
    POP = "Поп"
    JAZZ = "Джаз"
    CLASSICAL = "Классика"
    ELECTRONIC = "Электроника"


class Product(ABC):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @abstractmethod
    def get_info(self):
        pass


class RockProduct(Product):
    def get_info(self):
        return f"Рок: {self.name} - {self.price} руб."


class PopProduct(Product):
    def get_info(self):
        return f"Поп: {self.name} - {self.price} руб."


class JazzProduct(Product):
    def get_info(self):
        return f"Джаз: {self.name} - {self.price} руб."


class ClassicalProduct(Product):
    def get_info(self):
        return f"Классика: {self.name} - {self.price} руб."


class ElectronicProduct(Product):
    def get_info(self):
        return f"Электроника: {self.name} - {self.price} руб."


class ProductFactory(ABC):
    @abstractmethod
    def create_product(self, name, price):
        pass


class RockFactory(ProductFactory):
    def create_product(self, name, price):
        return RockProduct(name, price)


class PopFactory(ProductFactory):
    def create_product(self, name, price):
        return PopProduct(name, price)


class JazzFactory(ProductFactory):
    def create_product(self, name, price):
        return JazzProduct(name, price)


class ClassicalFactory(ProductFactory):
    def create_product(self, name, price):
        return ClassicalProduct(name, price)


class ElectronicFactory(ProductFactory):
    def create_product(self, name, price):
        return ElectronicProduct(name, price)


class Customer:
    def __init__(self, name, customer_id):
        self.name = name
        self.id = customer_id
        self.cart = []

    def add_to_cart(self, product):
        self.cart.append(product)
        print(f"  {self.name} добавил: {product.get_info()}")

    def __str__(self):
        return f"{self.name}"


class Cashier:
    def __init__(self, name):
        self.name = name
        self.customers_served = 0

    def serve_customer(self, customer):
        total = sum(p.price for p in customer.cart)
        time.sleep(random.uniform(1, 3))
        self.customers_served += 1
        msg = f"{self.name} обслужил {customer.name}. "
        msg += f"Сумма: {total} руб. (товаров: {len(customer.cart)})"
        return msg


class MusicStore:
    def __init__(self, name):
        self.name = name
        self.products = []
        self.factories = {
            MusicGenre.ROCK: RockFactory(),
            MusicGenre.POP: PopFactory(),
            MusicGenre.JAZZ: JazzFactory(),
            MusicGenre.CLASSICAL: ClassicalFactory(),
            MusicGenre.ELECTRONIC: ElectronicFactory(),
        }
        self.cashiers = []
        self.results = []

    def add_cashier(self, name):
        self.cashiers.append(Cashier(name))
        print(f"Добавлен кассир: {name}")

    def add_product(self, genre, name, price):
        factory = self.factories[genre]
        product = factory.create_product(name, price)
        self.products.append(product)
        print(f"Добавлен: {product.get_info()}")
        return product

    def serve_customers_parallel(self, customers_list):
        """Обслуживание покупателей в несколько потоков"""
        msg = "\n--- ОБСЛУЖИВАНИЕ ПОКУПАТЕЛЕЙ "
        msg += f"({len(customers_list)} чел, {len(self.cashiers)} кассира) ---"
        print(msg)

        queue = Queue()
        for customer in customers_list:
            queue.put(customer)

        threads = []
        start_time = time.time()
        self.results = []

        def cashier_work(cashier):
            while not queue.empty():
                try:
                    customer = queue.get_nowait()
                    result = cashier.serve_customer(customer)
                    self.results.append(result)
                    print(f"  ✓ {result}")
                except Empty:
                    break

        for cashier in self.cashiers:
            thread = threading.Thread(target=cashier_work, args=(cashier,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        total_time = time.time() - start_time
        print(f"\nВсе покупатели обслужены за {total_time:.1f} сек")
        print(f"Обслужено заказов: {len(self.results)}")
        for cashier in self.cashiers:
            print(f"  {cashier.name} обслужил {cashier.customers_served} чел.")

    def show_catalog(self):
        print(f"\n=== КАТАЛОГ МАГАЗИНА '{self.name}' ===")
        for p in self.products:
            print(f"  {p.get_info()}")


# ДЕМОНСТРАЦИЯ
if __name__ == "__main__":
    print("=" * 60)
    print("МУЗЫКАЛЬНЫЙ МАГАЗИН (Factory Method + Потоки)")
    print("=" * 60)

    # Создаем магазин
    store = MusicStore("Мелодия")

    # Добавляем кассиров
    print("\n--- ПЕРСОНАЛ ---")
    store.add_cashier("Анна")
    store.add_cashier("Иван")
    store.add_cashier("Елена")

    # Добавляем товары через фабрики
    print("\n--- ТОВАРЫ ---")
    rock_album = store.add_product(MusicGenre.ROCK, "Nirvana - Nevermind", 1500)
    pop_album = store.add_product(MusicGenre.POP, "Michael Jackson - Thriller", 1400)
    jazz_album = store.add_product(MusicGenre.JAZZ, "Miles Davis - Kind of Blue", 1700)
    classic_album = store.add_product(MusicGenre.CLASSICAL, "Beethoven - Symphony 9", 1200)
    electronic_album = store.add_product(MusicGenre.ELECTRONIC, "Daft Punk - RAM", 1600)
    rock_album2 = store.add_product(MusicGenre.ROCK, "Metallica - Black Album", 1550)
    pop_album2 = store.add_product(MusicGenre.POP, "Lady Gaga - The Fame", 1350)

    store.show_catalog()

    # Создаем покупателей
    print("\n--- ПОКУПАТЕЛИ ---")
    customers = []

    customer1 = Customer("Иван", 1)
    customer1.add_to_cart(rock_album)
    customer1.add_to_cart(pop_album)
    customers.append(customer1)

    customer2 = Customer("Мария", 2)
    customer2.add_to_cart(jazz_album)
    customer2.add_to_cart(classic_album)
    customers.append(customer2)

    customer3 = Customer("Алексей", 3)
    customer3.add_to_cart(electronic_album)
    customer3.add_to_cart(rock_album2)
    customers.append(customer3)

    customer4 = Customer("Елена", 4)
    customer4.add_to_cart(pop_album2)
    customers.append(customer4)

    customer5 = Customer("Дмитрий", 5)
    customer5.add_to_cart(rock_album)
    customer5.add_to_cart(rock_album2)
    customer5.add_to_cart(pop_album)
    customers.append(customer5)

    customer6 = Customer("Ольга", 6)
    customer6.add_to_cart(jazz_album)
    customers.append(customer6)

    # Обслуживание (параллельно)
    store.serve_customers_parallel(customers)

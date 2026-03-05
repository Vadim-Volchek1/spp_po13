from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


# ========== БАЗОВЫЕ КЛАССЫ ==========
class Bill(ABC):
    """Абстрактный счет"""

    def __init__(self, amount=0):
        self.amount = amount
        self.date = datetime.now()
        self.paid = False

    @abstractmethod
    def calculate(self):
        pass

    def pay(self):
        self.paid = True
        print(f"Счет оплачен: {self.calculate()} руб.")

    def __str__(self):
        return f"Счет от {self.date.strftime('%d.%m.%Y')}: {self.calculate()} руб."


class CallBill(Bill):
    """Счет за разговоры"""

    def __init__(self, minutes, rate):
        super().__init__()
        self.minutes = minutes
        self.rate = rate

    def calculate(self):
        return self.minutes * self.rate


class ServiceBill(Bill):
    """Счет за услуги"""

    def __init__(self, service_name, monthly_fee):
        super().__init__()
        self.service_name = service_name
        self.monthly_fee = monthly_fee

    def calculate(self):
        return self.monthly_fee


class Service:
    """Услуга"""

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.price} руб./мес)"


# ========== ОСНОВНЫЕ КЛАССЫ ==========
class Subscriber:
    """Абонент"""

    def __init__(self, sub_id, name, phone):
        self.id = sub_id
        self.name = name
        self.phone = phone
        self.balance = 0.0
        self.active = True
        self.services = []  # агрегация
        self.bills = []  # ассоциация

    def add_service(self, service):
        if service not in self.services:
            self.services.append(service)
            bill = ServiceBill(service.name, service.price)
            self.bills.append(bill)
            print(f"{self.name} подключил {service.name}")

    def remove_service(self, service_name):
        for s in self.services[:]:
            if s.name == service_name:
                self.services.remove(s)
                print(f"{self.name} отключил {service_name}")
                return

    def make_call(self, minutes, rate):
        if not self.active:
            print(f"{self.name} заблокирован. Звонок невозможен")
            return
        bill = CallBill(minutes, rate)
        self.bills.append(bill)
        print(f"{self.name} проговорил {minutes} мин")

    def pay_bill(self, index=-1):
        if not self.bills:
            print("Нет счетов")
            return
        bill = self.bills[index] if index != -1 else self.bills[-1]
        amount = bill.calculate()
        bill.pay()
        self.balance -= amount

    def get_debt(self):
        return sum(b.calculate() for b in self.bills if not b.paid)

    def request_new_phone(self, admin, new_phone):
        print(f"{self.name} просит сменить номер {self.phone} -> {new_phone}")
        return admin.change_phone(self, new_phone)

    def request_unsubscribe(self, admin, service_name):
        print(f"{self.name} просит отключить {service_name}")
        return admin.remove_service(self, service_name)

    def __str__(self):
        status = "активен" if self.active else "заблокирован"
        serv = ", ".join(s.name for s in self.services) or "нет"
        return f"{self.name} (тел:{self.phone}, {status}, услуги:{serv})"

    def __eq__(self, other):
        return isinstance(other, Subscriber) and self.id == other.id


class Administrator:
    """Администратор"""

    def __init__(self, name, station):
        self.name = name
        self.station = station  # ассоциация

    def change_phone(self, subscriber, new_phone):
        # Проверка, что номер не занят
        for sub in self.station.subscribers:
            if sub.phone == new_phone:
                print(f"Ошибка: номер {new_phone} занят")
                return False
        old = subscriber.phone
        subscriber.phone = new_phone
        print(f"Админ {self.name} сменил номер {old} -> {new_phone}")
        return True

    def add_service(self, subscriber, service_name):
        service = self.station.get_service(service_name)
        if service:
            subscriber.add_service(service)
            return True
        print(f"Услуга {service_name} не найдена")
        return False

    def remove_service(self, subscriber, service_name):
        subscriber.remove_service(service_name)
        return True

    def block_subscriber(self, subscriber):
        if subscriber.get_debt() > 0:
            subscriber.active = False
            print(f"Админ {self.name} заблокировал {subscriber.name} за долг {subscriber.get_debt()} руб.")
            return True
        print(f"У {subscriber.name} нет долгов")
        return False

    def unblock_subscriber(self, subscriber):
        if subscriber.get_debt() == 0:
            subscriber.active = True
            print(f"Админ {self.name} разблокировал {subscriber.name}")
            return True
        print(f"{subscriber.name} должен {subscriber.get_debt()} руб.")
        return False

    def __str__(self):
        return f"Админ {self.name}"


class PhoneStation:
    """Телефонная станция (агрегация)"""

    def __init__(self, name, call_rate=2.0):
        self.name = name
        self.call_rate = call_rate
        self.subscribers = []  # агрегация
        self.services = []  # агрегация

    def add_subscriber(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            print(f"{subscriber.name} добавлен на станцию")

    def remove_subscriber(self, sub_id):
        for s in self.subscribers[:]:
            if s.id == sub_id:
                self.subscribers.remove(s)
                print(f"{s.name} удален со станции")
                return

    def add_service(self, service):
        self.services.append(service)
        print(f"Услуга {service.name} добавлена")

    def get_service(self, name):
        for s in self.services:
            if s.name == name:
                return s
        return None

    def show_all(self):
        print(f"\n=== СТАНЦИЯ '{self.name}' ===")
        print("УСЛУГИ:")
        for s in self.services:
            print(f"  - {s}")
        print("АБОНЕНТЫ:")
        for s in self.subscribers:
            debt = s.get_debt()
            print(f"  - {s}" + (f" ДОЛГ: {debt} руб." if debt else ""))

    def __str__(self):
        return f"Станция '{self.name}' ({len(self.subscribers)} абонентов)"


# ========== ДЕМОНСТРАЦИЯ ==========
def demo():
    print("-" * 50)
    print("ТЕЛЕФОННАЯ СТАНЦИЯ")
    print("-" * 50)

    # 1. Создаем станцию
    station = PhoneStation("Мегафон", 1.5)
    admin = Administrator("Петров", station)
    print(f"Станция: {station}")
    print(f"Админ: {admin}")

    # 2. Добавляем услуги
    print("\n--- Добавление услуг ---")
    station.add_service(Service("Интернет", 300))
    station.add_service(Service("ТВ", 200))
    station.add_service(Service("SMS", 150))

    # 3. Создаем абонентов
    print("\n--- Регистрация абонентов ---")
    sub1 = Subscriber("001", "Иванов Иван", "111-111")
    sub2 = Subscriber("002", "Петров Петр", "222-222")
    sub3 = Subscriber("003", "Сидорова Анна", "333-333")

    station.add_subscriber(sub1)
    station.add_subscriber(sub2)
    station.add_subscriber(sub3)

    # 4. Подключаем услуги
    print("\n--- Подключение услуг ---")
    admin.add_service(sub1, "Интернет")
    admin.add_service(sub1, "ТВ")
    admin.add_service(sub2, "SMS")

    # 5. Совершаем звонки
    print("\n--- Звонки ---")
    sub1.make_call(10, station.call_rate)
    sub1.make_call(25, station.call_rate)
    sub2.make_call(5, station.call_rate)

    # 6. Смена номера
    print("\n--- Смена номера ---")
    sub1.request_new_phone(admin, "999-999")

    # 7. Проверка счетов
    print("\n--- Счета ---")
    for i, bill in enumerate(sub1.bills):
        print(f"  {i+1}. {bill}")

    # 8. Оплата
    print("\n--- Оплата ---")
    sub1.pay_bill(0)
    sub1.pay_bill()

    # 9. Блокировка за долги
    print("\n--- Блокировка ---")
    print(f"Долг {sub2.name}: {sub2.get_debt()} руб.")
    admin.block_subscriber(sub2)

    # Попытка звонка с заблокированного
    sub2.make_call(1, station.call_rate)

    # 10. Отказ от услуги
    print("\n--- Отказ от услуги ---")
    sub1.request_unsubscribe(admin, "ТВ")

    # 11. Показываем состояние
    station.show_all()

    # 12. Сравнение
    print("\n--- Сравнение ---")
    sub1_copy = Subscriber("001", "Иванов Иван", "999-999")
    print(f"sub1 == sub1_copy? {sub1 == sub1_copy}")


if __name__ == "__main__":
    demo()

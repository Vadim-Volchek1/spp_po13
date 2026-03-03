from abc import ABC, abstractmethod


# Интерфейс платежной системы
class PaymentSystem(ABC):
    @abstractmethod
    def pay_order(self, order):
        pass

    @abstractmethod
    def transfer(self, target_account, amount):
        pass


#  Базовый класс Person
class Person:
    def __init__(self, name):
        self.name = name


# Класс банковского счёта
class Account:
    def __init__(self, number, balance=0):
        self.number = number
        self.balance = balance
        self.active = True

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if not self.active:
            raise ValueError("Счёт аннулирован.")
        if amount > self.balance:
            raise ValueError("Недостаточно средств.")
        self.balance -= amount

    def close(self):
        self.active = False

    def __str__(self):
        return f"Счёт {self.number}: баланс={self.balance}, активен={self.active}"


# Кредитная карта, привязанная к счёту
class CreditCard:
    def __init__(self, number, credit_limit, account: Account):
        self.number = number
        self.credit_limit = credit_limit
        self.used = 0
        self.blocked = False
        self.account = account

    def spend(self, amount):

        if self.blocked:
            raise ValueError("Карта заблокирована.")

        if self.used + amount > self.credit_limit+self.account.balance:
            raise ValueError("Превышение кредитного лимита.")

        if self.account.balance >= amount:
            self.account.withdraw(amount)
        else:
            self.used += amount

    def block(self):
        self.blocked = True

    def __str__(self):
        return (f"КК {self.number}: использовано={self.used}/{self.credit_limit}, "
                f"заблокирована={self.blocked}, счёт={self.account.number}")

class Order:
    def __init__(self, order_id, amount):
        self.order_id = order_id
        self.amount = amount

    def __str__(self):
        return f"Заказ {self.order_id}: сумма={self.amount}"

class Client(Person, PaymentSystem):
    def __init__(self, name, account: Account, card: CreditCard):
        super().__init__(name)
        self.account = account
        self.card = card

    def pay_order(self, order: Order):
        print(f"{self.name} оплачивает заказ {order.order_id}")
        self.card.spend(order.amount)

    def transfer(self, target_account: Account, amount):
        print(f"{self.name} переводит {amount} на счёт {target_account.number}")
        self.account.withdraw(amount)
        target_account.deposit(amount)

    def block_card(self):
        print(f"{self.name} блокирует свою карту.")
        self.card.block()

    def close_account(self):
        print(f"{self.name} аннулирует свой счёт.")
        self.account.close()
        self.card.block()

#  Администратор
class Administrator(Person):
    def block_card_for_limit(self, card: CreditCard):
        print(f"Администратор {self.name} блокирует карту {card.number} за превышение лимита.")
        card.block()


acc1 = Account("A001", 1000)
acc2 = Account("A002", 500)


card1 = CreditCard("C001", 300, acc1)


client = Client("Иван", acc1, card1)
admin = Administrator("Мария")

def print_state():
    print("\n--- Текущее состояние ---")
    print(acc1)
    print(acc2)
    print(card1)
    print("-------------------------")

print_state()

while True:
    print("\nВыберите действие:")
    print("1. Оплатить заказ на 150")
    print("2. Перевести 200 со счёта A001 на A002")
    print("3. Заблокировать карту клиента")
    print("4. Аннулировать счёт клиента (и заблокировать карту)")
    print("5. Администратор блокирует карту за превышение лимита")
    print("6. Показать состояние")
    print("0. Выход")

    choice = input("Ваш выбор: ").strip()

    try:
        if choice == "1":
            order1 = Order("O100", 150)
            client.pay_order(order1)
            print("Заказ оплачен.")
        elif choice == "2":
            client.transfer(acc2, 200)
            print("Перевод выполнен.")
        elif choice == "3":
            client.block_card()
            print("Карта заблокирована.")
        elif choice == "4":
            client.close_account()
            print("Счёт аннулирован, карта заблокирована.")
        elif choice == "5":
            admin.block_card_for_limit(card1)
            print("Карта заблокирована администратором.")
        elif choice == "6":
            print_state()
            continue
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный пункт.")
            continue
    except ValueError as e:
        print(f"Ошибка: {e}")

    print_state()

"""
В2
2) Система Платежи. Клиент имеет Счет в банке и Кредитную Карту (КК).
Клиент может оплатить Заказ, сделать платеж на другой Счет, заблокировать
КК и аннулировать Счет. Администратор может заблокировать КК за
превышение кредита.
"""

class Client:
    def __init__(self, name, credit_card):
        self.name = name
        self.credit_card = credit_card

    def print(self):
        print(self.name)
        print(self.credit_card)

    def pay_for_order(self, order):
        self.credit_card.pay(order)

    def transfer_money(self, account, amount):
        self.credit_card.transfer(account, amount)

    def block_kk(self, credit_card):
        credit_card.block()

    def null_account(self):
        self.credit_card.null_account()


class Card:
    def __init__(self, account, number, status):
        self.account = account
        self.number = number
        self.status = status

    def get_balance(self):
        return self.account.get_balance()

    def pay(self, order):
        if order.cost <= self.get_balance() and order.status != "Paid" and self.status != "Blocked":
            self.account.pay(order.get_cost())
            order.set_status("Paid")
            print("Оплата прошла успешно")
        else:
            print("Операция не прошла!")

    def transfer(self, account, amount):
        if amount <= self.get_balance() and self.status != "Blocked":
            self.account.pay(amount)
            account.get_money(amount)
            print("Перевод выполнен успешно")
        else:
            print("Операция не прошла!")

    def block(self):
        self.status = "Blocked"
        print("Карта заблокирована")

    def null_account(self):
        self.account.null_account()

    def transfer_money(self, account, amount):
        if amount <= self.get_balance() and self.status != "Blocked":
            self.account.pay(amount)
            account.get_money(amount)
        else:
            print("Операция не прошла!")


class Order:
    def __init__(self, cost, status="Waiting"):
        self.cost = cost
        self.status = status

    def print(self):
        print(self.status)

    def set_status(self, status):
        self.status = status

    def get_cost(self):
        return self.cost

class BankAccount:
    def __init__(self, owner, credit_card, balance):
        self.owner = owner
        self.credit_card = credit_card
        self.balance = balance

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def pay(self, amount):
        self.set_balance(self.balance - amount)
        if self.balance < 0:
            self.credit_card.block()
            print("Карта заблокирована из-за отрицательного баланса")

    def get_money(self, amount):
        self.set_balance(self.balance + amount)

    def null_account(self):
        self.balance = 0
        print("Счет аннулирован")


class Administrator(Client):
    def __init__(self,name,credit_card=None):
        Client.__init__(self,name,credit_card)
    def block_kk(self, credit_card):
        credit_card.block()
        print(f"Администратор {self.name} заблокировал карту")


if __name__ == '__main__':
    bank_account = BankAccount("Иван Петров", None, 5000)
    var_credit_card = Card(bank_account, "4276-1234-5678-9012", "Active")
    bank_account.credit_card = var_credit_card

    client = Client("Иван Петров", var_credit_card)
    admin = Administrator("Петр Сидоров")

    print(f"Клиент: {client.name}")
    print(f"Номер карты: {var_credit_card.number}")
    print(f"Статус карты: {var_credit_card.status}")
    print(f"Баланс счета: {bank_account.get_balance()}")
    print(f"Баланс карты: {var_credit_card.get_balance()}")

    order1 = Order(2000, "Waiting")
    order2 = Order(4000, "Waiting")
    order3 = Order(1500, "Waiting")

    print(f"Заказ 1: сумма {order1.cost}, статус {order1.status}")
    print(f"Заказ 2: сумма {order2.cost}, статус {order2.status}")
    print(f"Заказ 3: сумма {order3.cost}, статус {order3.status}")

    client.pay_for_order(order1)
    print(f"Статус заказа: {order1.status}")
    print(f"Баланс после оплаты: {bank_account.get_balance()}")

    client.pay_for_order(order2)
    print(f"Статус заказа: {order2.status}")
    print(f"Баланс после оплаты: {bank_account.get_balance()}")
    print(f"Статус карты: {var_credit_card.status}")


    other_account = BankAccount("Петр Иванов", None, 1000)
    print(f"Баланс счета {other_account.owner} до перевода: {other_account.get_balance()}")

    client.transfer_money(other_account, 500)
    print(f"Баланс счета {client.name} после перевода: {bank_account.get_balance()}")
    print(f"Баланс счета {other_account.owner} после перевода: {other_account.get_balance()}")

    client.block_kk(var_credit_card)
    print(f"Статус карты: {var_credit_card.status}")

    client.pay_for_order(order3)
    print(f"Статус заказа: {order3.status}")
    print(f"Баланс не изменился: {bank_account.get_balance()}")

    new_account = BankAccount("Сергей", None, 3000)
    new_card = Card(new_account, "5555-6666", "Active")
    new_account.credit_card = new_card
    print("Новая карта, статус: ",new_card.status)

    admin.block_kk(new_card)
    print("Статус карты после блокировки: ",new_card.status)

    print(f"Баланс до аннулирования: {bank_account.get_balance()}")
    client.null_account()
    print(f"Баланс после аннулирования: {bank_account.get_balance()}")

class ATM:
    def __init__(self, atm_id, initial_money):
        self.atm_id = atm_id
        self.total_money = initial_money
        self.state = WaitingState(self)
        self.current_card = None
        self.failed_attempts = 0

    def __str__(self):
        return f"Банкомат {self.atm_id}: {self.total_money} руб., состояние: {self.state}"

    def set_state(self, state):
        self.state = state
        print(f"Банкомат {self.atm_id} перешел в режим: {self.state}")

    def insert_card(self, card):
        self.state.insert_card(card)

    def enter_pin(self, pin):
        self.state.enter_pin(pin)

    def withdraw_money(self, amount):
        self.state.withdraw_money(amount)

    def cancel(self):
        self.state.cancel()

    def has_enough_money(self, amount):
        return self.total_money >= amount

    def dispense_money(self, amount):
        if self.has_enough_money(amount):
            self.total_money -= amount
            print(f"Выдано {amount} руб.")
            return True
        return False


class ATMState:
    def __init__(self, atm):
        self.atm = atm

    def insert_card(self, card):  # pylint: disable=unused-argument
        print("Операция не поддерживается в текущем режиме")

    def enter_pin(self, pin):  # pylint: disable=unused-argument
        print("Операция не поддерживается в текущем режиме")

    def withdraw_money(self, amount):  # pylint: disable=unused-argument
        print("Операция не поддерживается в текущем режиме")

    def cancel(self):
        print("Операция не поддерживается в текущем режиме")


class WaitingState(ATMState):
    def __str__(self):
        return "Ожидание карты"

    def insert_card(self, card):
        print(f"Карта {card} вставлена")
        self.atm.current_card = card
        self.atm.set_state(PinEntryState(self.atm))


class PinEntryState(ATMState):
    def __str__(self):
        return "Ввод PIN-кода"

    def enter_pin(self, pin):
        correct_pin = "1234"
        if pin == correct_pin:
            print("PIN-код принят")
            self.atm.failed_attempts = 0
            self.atm.set_state(OperationState(self.atm))
        else:
            self.atm.failed_attempts += 1
            print(f"Неверный PIN-код. Попытка {self.atm.failed_attempts}/3")
            if self.atm.failed_attempts >= 3:
                print("Превышено количество попыток. Карта заблокирована")
                self.atm.set_state(BlockedState(self.atm))

    def cancel(self):
        print("Операция отменена")
        self.atm.current_card = None
        self.atm.set_state(WaitingState(self.atm))


class OperationState(ATMState):
    def __str__(self):
        return "Выполнение операции"

    def withdraw_money(self, amount):
        if amount <= 0:
            print("Некорректная сумма")
            return

        if not self.atm.has_enough_money(amount):
            print("Недостаточно средств в банкомате")
            self.atm.set_state(NoMoneyState(self.atm))
            return

        if amount > 10000:
            print("Превышен лимит на снятие (10000 руб.)")
            return

        if self.atm.dispense_money(amount):
            print(f"Снято {amount} руб. Остаток: {self.atm.total_money} руб.")
            print("Заберите карту")
            self.atm.current_card = None
            self.atm.set_state(WaitingState(self.atm))

    def cancel(self):
        print("Операция отменена")
        self.atm.current_card = None
        self.atm.set_state(WaitingState(self.atm))


class NoMoneyState(ATMState):
    def __str__(self):
        return "Блокировка (нет денег)"

    def insert_card(self, card):  # pylint: disable=unused-argument
        print("Банкомат временно не обслуживает. Нет денег")

    def cancel(self):
        print("Возврат к ожиданию...")
        self.atm.set_state(WaitingState(self.atm))


class BlockedState(ATMState):
    def __str__(self):
        return "Блокировка (неверный PIN)"

    def insert_card(self, card):  # pylint: disable=unused-argument
        print("Карта заблокирована. Обратитесь в банк")

    def cancel(self):
        print("Возврат к ожиданию...")
        self.atm.failed_attempts = 0
        self.atm.current_card = None
        self.atm.set_state(WaitingState(self.atm))


class Card:
    def __init__(self, card_number, owner):
        self.card_number = card_number
        self.owner = owner

    def __str__(self):
        return f"{self.card_number} ({self.owner})"


demo_atm = ATM("ATM-001", 50000)
print(demo_atm)

demo_card = Card("1234-5678-9012-3456", "Владелец 1")
print(demo_card)

print("СЦЕНАРИЙ 1: Успешное снятие денег")
demo_atm.insert_card(demo_card)
demo_atm.enter_pin("1234")
demo_atm.withdraw_money(5000)
print(f"\nИтог: {demo_atm}")

print("СЦЕНАРИЙ 2: Неверный PIN-код")
demo_atm.insert_card(demo_card)
demo_atm.enter_pin("0000")
demo_atm.enter_pin("1111")
demo_atm.enter_pin("2222")
print(f"\nИтог: {demo_atm}")

demo_atm.cancel()
print(f"После сброса: {demo_atm}")

print("СЦЕНАРИЙ 3: Недостаточно средств в банкомате")
atm2 = ATM("ATM-002", 1000)
print(atm2)

atm2.insert_card(demo_card)
atm2.enter_pin("1234")
atm2.withdraw_money(2000)
print(f"\nИтог: {atm2}")

atm2.cancel()
print(f"После сброса: {atm2}")

print("СЦЕНАРИЙ 4: Отмена операции")
demo_atm.insert_card(demo_card)
demo_atm.enter_pin("1234")
demo_atm.cancel()
demo_atm.insert_card(demo_card)
print(f"\nИтог: {demo_atm}")

print("ДЕМОНСТРАЦИЯ ВСЕХ СОСТОЯНИЙ")
states_demo = ATM("DEMO-001", 5000)
print("\n1. Ожидание карты:")
print(states_demo)
print("\n2. Ввод PIN-кода:")
states_demo.insert_card(demo_card)
print(states_demo)
print("\n3. Выполнение операции:")
states_demo.enter_pin("1234")
print(states_demo)
print("\n4. Блокировка (нет денег):")
states_demo.total_money = 0
states_demo.withdraw_money(1000)
print(states_demo)
print("\n5. Возврат в ожидание:")
states_demo.cancel()
print(states_demo)

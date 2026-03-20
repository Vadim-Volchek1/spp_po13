"""
В2
2)Проект «Универсальная электронная карта». В проекте
должна быть
реализована универсальная электронная карта, в
которой есть функции
паспорта, страхового полиса, банковской карты и т. д.
"""
#ФАСАД

class PassportSubsystem:
    def __init__(self):
        self.full_name = "Ибрагим Абдулович"
        self.birth_date = "25.11.2005"
        self.passport_number = "42"
        self.registration = "Улица Бабалабла"

    def verify_identity(self):
        print("Паспортная система: проверка личности... OK")
        return True

    def public_def_only_for_public_def_def_pylint_live_me_along(self):
        print("\npublic_def_only_for_public_def_def_pylint_live_me_along\n")

class InsuranceSubsystem:
    def __init__(self):
        self.policy_number = "2022345"

    def check_coverage(self, service):
        print(f"Страховая система: проверка покрытия для услуги '{service}'... Доступно")
        return True

    def public_def_only_for_public_def_def_pylint_live_me_along(self):
        print("\npublic_def_only_for_public_def_def_pylint_live_me_along\n")


class BankSubsystem:
    def __init__(self):
        self.card_number = "220023456789012"
        self.bank_name = "Мбанк"
        self.balance = 5000.0

    def pay(self, amount, merchant):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Банк: оплата {amount} руб. в '{merchant}' выполнена")
            return True
        print("Банк: недостаточно средств")
        return False

    def money_up(self, amount):
        self.balance += amount
        print(f"Банк: счет пополнен на {amount} руб.")
        return self.balance


#Фасад
class UniversalCardFacade:

    def __init__(self, person_id: str):
        self.person_id = person_id
        self.card_number = f"Кар-Точка ->{person_id}"
        self.passport = PassportSubsystem()
        self.insurance = InsuranceSubsystem()
        self.bank = BankSubsystem()
        print(f"\nИнициализация карты {self.card_number} ")
        print("Карта готова к использованию \n")

    def show_info(self):
        print("\n")
        print("УНИВЕРСАЛЬНАЯ ЭЛЕКТРОННАЯ КАР-ТОЧКА")
        print(f"Карта №: {self.card_number}")
        print(f"Владелец: {self.passport.full_name}")
        print(f"Паспорт: {self.passport.passport_number}")
        print(f"Прописка: {self.passport.registration}")
        print(f"Полис: {self.insurance.policy_number}")
        print(f"Банк: {self.bank.bank_name}")
        print(f"Баланс: {self.bank.balance} руб.")

    def pay(self, amount, merchant = "Покупка"):
        print(f"\nОперация: оплата {amount} руб. в '{merchant}'")
        if self.bank.pay(amount, merchant):
            print("оплата прошла успешно")
            return True

        return False


    def verify_document(self):
        print("\nОперация: подтверждение личности")
        if self.passport.verify_identity():
            print("Личность подтверждена")
            return True
        return False

    def money_up_balance(self, amount: float):
        print("\nОперация: пополнение баланса")
        new_balance = self.bank.money_up(amount)
        print(f"Новый баланс: {new_balance} руб.")
        return new_balance

if __name__ == "__main__":
    my_card = UniversalCardFacade("USER-001")
    my_card.show_info()

    my_card.pay(500, "Магазин")
    my_card.verify_document()
    my_card.money_up_balance(2000)

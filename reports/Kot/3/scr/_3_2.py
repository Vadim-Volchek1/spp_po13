from abc import ABC, abstractmethod


# Компонент
class Account(ABC):
    @abstractmethod
    def get_benefits(self):
        pass

    @abstractmethod
    def get_discount(self):
        pass


# Конкретный компонент (базовый уровень)
class BaseAccount(Account):
    def __init__(self, name: str):
        self.name = name
        print(f"[INIT] Base account created for: {name}")

    def get_benefits(self):
        return ["Standard catalog access"]

    def get_discount(self):
        return 0.0


# Абстрактный декоратор
class AccountDecorator(Account):
    def __init__(self, account: Account):
        self._account = account
        print(
            f"[DECORATE] Adding new features to: {account.name if hasattr(account, 'name') else 'Account'}"
        )

    def get_benefits(self):
        return self._account.get_benefits()

    def get_discount(self):
        return self._account.get_discount()


# Конкретные декораторы
class BronzeDecorator(AccountDecorator):
    def get_benefits(self):
        benefits = self._account.get_benefits()
        benefits.append("Free standard shipping")
        return benefits

    def get_discount(self):
        return 5.0


class SilverDecorator(AccountDecorator):
    def get_benefits(self):
        benefits = self._account.get_benefits()
        benefits.append("Priority customer support")
        benefits.append("Exclusive monthly e-book")
        return benefits

    def get_discount(self):
        return 10.0


class GoldDecorator(AccountDecorator):
    def get_benefits(self):
        benefits = self._account.get_benefits()
        benefits.append("VIP early access to new releases")
        benefits.append("Free express shipping")
        benefits.append("Personal book advisor")
        return benefits

    def get_discount(self):
        return 15.0


# Клиентский код
if __name__ == "__main__":
    print("--- Creating customer: John Doe ---")
    user = BaseAccount("John Doe")
    print("\n--- Upgrading to Bronze level ---")
    user = BronzeDecorator(user)
    print("\n--- Upgrading to Silver level ---")
    user = SilverDecorator(user)
    print("\n--- Upgrading to Gold level ---")
    user = GoldDecorator(user)
    print("\n=== Final Account Status ===")
    print(f"Benefits: {', '.join(user.get_benefits())}")
    print(f"Discount: {user.get_discount()}%")

from abc import ABC, abstractmethod

class Card(ABC):
    @abstractmethod
    def info(self) -> str:
        pass


class BaseCard(Card):
    def info(self) -> str:
        return "Универсальная электронная карта"


class CardDecorator(Card):
    def __init__(self, card: Card):
        self.card = card

    @abstractmethod
    def info(self) -> str:
        pass


class PassportDecorator(CardDecorator):
    def info(self) -> str:
        return self.card.info() + ", паспортные данные"


class InsuranceDecorator(CardDecorator):
    def info(self) -> str:
        return self.card.info() + ", страховой полис"


class BankCardDecorator(CardDecorator):
    def info(self) -> str:
        return self.card.info() + ", банковская карта"


class TransportDecorator(CardDecorator):
    def info(self) -> str:
        return self.card.info() + ", транспортная карта"


if __name__ == "__main__":
    card = BaseCard()
    card = PassportDecorator(card)
    card = InsuranceDecorator(card)
    card = BankCardDecorator(card)

    print(card.info())

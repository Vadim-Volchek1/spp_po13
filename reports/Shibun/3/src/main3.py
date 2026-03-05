from abc import ABC, abstractmethod

class PrintStrategy(ABC):
    @abstractmethod
    def print(self, text: str) -> str:
        pass


class ColorPrint(PrintStrategy):
    def print(self, text: str) -> str:
        return f"Цветная печать: {text}"


class BlackWhitePrint(PrintStrategy):
    def print(self, text: str) -> str:
        return f"Чёрно-белая печать: {text}"


class PhotoPrint(PrintStrategy):
    def print(self, text: str) -> str:
        return f"Фотопечать высокого качества: {text}"


class DraftPrint(PrintStrategy):
    def print(self, text: str) -> str:
        return f"Черновой режим: {text}"


class Printer:
    def __init__(self, model: str, strategy: PrintStrategy):
        self.model = model
        self.strategy = strategy

    def set_strategy(self, strategy: PrintStrategy):
        self.strategy = strategy

    def print(self, text: str):
        print(f"[{self.model}] {self.strategy.print(text)}")


if __name__ == "__main__":
    printer = Printer("HP LaserJet", BlackWhitePrint())
    printer.print("Документ 1")

    printer.set_strategy(ColorPrint())
    printer.print("Документ 2")

    printer.set_strategy(PhotoPrint())
    printer.print("Фото 3")

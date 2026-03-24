"""Реализация поведенческого паттерна Strategy для проекта 'Принтеры'."""

# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod

# ============================================================
# Стратегии печати
# ============================================================


class PrintStrategy(ABC):
    """Абстрактная стратегия печати."""

    @abstractmethod
    def print_document(self, content: str) -> str:
        """Выполняет печать документа."""


class TextPrintStrategy(PrintStrategy):
    """Стратегия текстовой печати."""

    def print_document(self, content: str) -> str:
        return f"[Текстовая печать] {content}"


class ColorPrintStrategy(PrintStrategy):
    """Стратегия цветной печати."""

    def print_document(self, content: str) -> str:
        return f"[Цветная печать] {content}"


class PhotoPrintStrategy(PrintStrategy):
    """Стратегия фотопечати."""

    def print_document(self, content: str) -> str:
        return f"[Фотопечать высокого качества] {content}"


# ============================================================
# Контекст — Принтер
# ============================================================


class Printer:
    """Принтер, который использует выбранную стратегию печати."""

    def __init__(self, strategy: PrintStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PrintStrategy):
        """Меняет стратегию печати."""
        self.strategy = strategy

    def print(self, content: str) -> str:
        """Печатает документ с использованием текущей стратегии."""
        return self.strategy.print_document(content)


# ============================================================
# Пример использования
# ============================================================

if __name__ == "__main__":
    printer = Printer(TextPrintStrategy())

    print(printer.print("Документ №1"))

    printer.set_strategy(ColorPrintStrategy())
    print(printer.print("Документ №2"))

    printer.set_strategy(PhotoPrintStrategy())
    print(printer.print("Фото №3"))

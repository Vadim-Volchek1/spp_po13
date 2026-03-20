from abc import ABC, abstractmethod
import random
import time


class PrinterState(ABC):
    """Базовый класс состояния принтера"""

    def __init__(self, printer):
        self.printer = printer

    @abstractmethod
    def print_document(self, pages):
        pass

    @abstractmethod
    def load_paper(self, sheets):
        pass

    @abstractmethod
    def remove_jam(self):
        pass

    @abstractmethod
    def refill_ink(self, percent):
        pass

    @abstractmethod
    def get_state_name(self):
        pass


class IdleState(PrinterState):
    """Состояние ожидания"""

    def print_document(self, pages):
        print(f"\nПопытка печати {pages} стр. в состоянии ОЖИДАНИЕ")

        # Проверка наличия бумаги
        if self.printer.paper_sheets < pages:
            print(f"  Недостаточно бумаги! (есть: {self.printer.paper_sheets}, нужно: {pages})")
            self.printer.set_state(OutOfPaperState(self.printer))
            return False

        # Проверка наличия краски
        ink_needed = pages * 2
        if self.printer.ink_level < ink_needed:
            print(f"  Недостаточно краски! (есть: {self.printer.ink_level}%, нужно: {ink_needed}%)")
            self.printer.set_state(OutOfInkState(self.printer))
            return False

        # Проверка вероятности зажатия (5%)
        if random.random() < self.printer.jam_probability:
            print("  ПРОИЗОШЛО ЗАЖАТИЕ БУМАГИ!")  # Убрал f-строку
            self.printer.set_state(JammedState(self.printer))
            return False

        # Начинаем печать
        self.printer.set_state(PrintingState(self.printer))
        return self.printer.current_state.print_document(pages)

    def load_paper(self, sheets):
        print(f"\nЗагрузка {sheets} листов")
        self.printer.paper_sheets += sheets
        print(f"  Теперь бумаги: {self.printer.paper_sheets} листов")
        return True

    def remove_jam(self):
        print("\nПопытка удалить зажатие")
        print("  Нет зажатия бумаги")
        return False

    def refill_ink(self, percent):
        print(f"\nЗаправка картриджа на {percent}%")
        self.printer.ink_level = min(100, self.printer.ink_level + percent)
        print(f"  Теперь уровень краски: {self.printer.ink_level}%")
        return True

    def get_state_name(self):
        return "ОЖИДАНИЕ"


class PrintingState(PrinterState):
    """Состояние печати"""

    def print_document(self, pages):
        print(f"\nПЕЧАТЬ {pages} стр.")

        for page in range(1, pages + 1):
            time.sleep(0.2)
            print(f"    Страница {page} напечатана")

            self.printer.paper_sheets -= 1
            self.printer.ink_level -= 2

            # Маленькая вероятность зажатия (2%)
            if random.random() < self.printer.jam_probability / 2:
                print(f"  ЗАЖАТИЕ БУМАГИ на странице {page}!")
                self.printer.set_state(JammedState(self.printer))
                return False

        print("  Печать завершена")  # Убрал f-строку
        self.printer.set_state(IdleState(self.printer))
        return True

    def load_paper(self, sheets):
        print("\nПопытка загрузить бумагу во время ПЕЧАТИ")
        print("  Невозможно, принтер работает")
        return False

    def remove_jam(self):
        print("\nПопытка удалить зажатие во время ПЕЧАТИ")
        print("  Нет зажатия")
        return False

    def refill_ink(self, percent):
        print("\nПопытка заправить картридж во время ПЕЧАТИ")
        print("  Невозможно, принтер работает")
        return False

    def get_state_name(self):
        return "ПЕЧАТЬ"


class JammedState(PrinterState):
    """Состояние зажатия бумаги"""

    def print_document(self, pages):
        print("\nПопытка печати при ЗАЖАТИИ")
        print("  Устраните зажатие!")
        return False

    def load_paper(self, sheets):
        print("\nПопытка загрузить бумагу при ЗАЖАТИИ")
        print("  Устраните зажатие!")
        return False

    def remove_jam(self):
        print("\nУДАЛЕНИЕ ЗАЖАТОЙ БУМАГИ")
        time.sleep(0.5)
        print("  Зажатие успешно устранено")
        self.printer.set_state(IdleState(self.printer))
        return True

    def refill_ink(self, percent):
        print("\nЗаправка картриджа при ЗАЖАТИИ")
        self.printer.ink_level = min(100, self.printer.ink_level + percent)
        print("  Картридж заправлен, зажатие осталось")  # Убрал f-строку
        return True

    def get_state_name(self):
        return "ЗАЖАТИЕ"


class OutOfPaperState(PrinterState):
    """Состояние отсутствия бумаги"""

    def print_document(self, pages):
        print("\nПопытка печати - НЕТ БУМАГИ")
        return False

    def load_paper(self, sheets):
        print(f"\nЗАГРУЗКА {sheets} листов")
        self.printer.paper_sheets += sheets
        print(f"  Теперь бумаги: {self.printer.paper_sheets} листов")
        self.printer.set_state(IdleState(self.printer))
        return True

    def remove_jam(self):
        print("\nПопытка удалить зажатие")
        print("  Нет зажатия")
        return False

    def refill_ink(self, percent):
        print("\nЗаправка картриджа")
        self.printer.ink_level = min(100, self.printer.ink_level + percent)
        print(f"  Уровень краски: {self.printer.ink_level}%")
        return True

    def get_state_name(self):
        return "НЕТ БУМАГИ"


class OutOfInkState(PrinterState):
    """Состояние отсутствия краски"""

    def print_document(self, pages):
        print("\nПопытка печати - НЕТ КРАСКИ")
        return False

    def load_paper(self, sheets):
        print(f"\nЗАГРУЗКА {sheets} листов")
        self.printer.paper_sheets += sheets
        print(f"  Теперь бумаги: {self.printer.paper_sheets} листов")
        return True

    def remove_jam(self):
        print("\nПопытка удалить зажатие")
        print("  Нет зажатия")
        return False

    def refill_ink(self, percent):
        print(f"\nЗАПРАВКА КАРТРИДЖА на {percent}%")
        self.printer.ink_level = min(100, self.printer.ink_level + percent)
        print(f"  Теперь краски: {self.printer.ink_level}%")
        self.printer.set_state(IdleState(self.printer))
        return True

    def get_state_name(self):
        return "НЕТ КРАСКИ"


class Printer:
    def __init__(self, model):
        self.model = model
        self.paper_sheets = 100  # Начинаем с 100 листов
        self.ink_level = 100  # Начинаем с 100% краски
        self.jam_probability = 0.03  # 3% вероятность зажатия
        self.current_state = IdleState(self)
        self.total_printed = 0
        self.jams_fixed = 0

        print(f"\nСОЗДАН ПРИНТЕР {model}")
        print(f"  Бумага: {self.paper_sheets} листов")
        print(f"  Краска: {self.ink_level}%")
        print(f"  Вероятность зажатия: {self.jam_probability*100:.0f}%")

    def set_state(self, state):
        print(f"\nСостояние: {self.current_state.get_state_name()} -> {state.get_state_name()}")
        self.current_state = state

    def print_document(self, pages):
        print("\n" + "=" * 50)
        print(f"КОМАНДА: ПЕЧАТЬ {pages} стр.")
        print("=" * 50)
        result = self.current_state.print_document(pages)
        if result:
            self.total_printed += pages
        self.show_status()
        return result

    def load_paper(self, sheets):
        print("\n" + "=" * 50)
        print(f"КОМАНДА: ЗАГРУЗИТЬ {sheets} ЛИСТОВ")
        print("=" * 50)
        result = self.current_state.load_paper(sheets)
        self.show_status()
        return result

    def remove_jam(self):
        print("\n" + "=" * 50)
        print("КОМАНДА: УСТРАНИТЬ ЗАЖАТИЕ")
        print("=" * 50)
        result = self.current_state.remove_jam()
        if result:
            self.jams_fixed += 1
        self.show_status()
        return result

    def refill_ink(self, percent):
        print("\n" + "=" * 50)
        print(f"КОМАНДА: ЗАПРАВИТЬ КАРТРИДЖ на {percent}%")
        print("=" * 50)
        result = self.current_state.refill_ink(percent)
        self.show_status()
        return result

    def show_status(self):
        print("\nСТАТУС ПРИНТЕРА:")
        print(f"  Модель: {self.model}")
        print(f"  Состояние: {self.current_state.get_state_name()}")
        print(f"  Бумага: {self.paper_sheets} листов")
        print(f"  Краска: {self.ink_level}%")
        print(f"  Напечатано: {self.total_printed} стр.")
        print("-" * 50)


def demo():
    print("=" * 60)
    print("ПРОЕКТ ПРИНТЕР (ПАТТЕРН: СОСТОЯНИЕ)")
    print("=" * 60)

    printer = Printer("HP LaserJet 1018")

    # 1. Успешная печать
    print("\n" + "*" * 40)
    print("1. ОБЫЧНАЯ ПЕЧАТЬ")
    print("*" * 40)
    printer.print_document(5)

    # 2. Еще печать
    print("\n" + "*" * 40)
    print("2. ВТОРОЙ ДОКУМЕНТ")
    print("*" * 40)
    printer.print_document(3)

    # 3. Печать пока не кончится бумага
    print("\n" + "*" * 40)
    print("3. ПЕЧАТЬ ДО КОНЦА БУМАГИ")
    print("*" * 40)
    printer.print_document(100)  # Бумаги 92 после первых двух печатей

    # 4. Загрузка бумаги
    print("\n" + "*" * 40)
    print("4. ЗАГРУЗКА БУМАГИ")
    print("*" * 40)
    printer.load_paper(50)

    # 5. Печать пока не кончится краска
    print("\n" + "*" * 40)
    print("5. ПЕЧАТЬ ДО КОНЦА КРАСКИ")
    print("*" * 40)
    for _ in range(5):  # Изменил i на _
        printer.print_document(10)

    # 6. Заправка картриджа
    print("\n" + "*" * 40)
    print("6. ЗАПРАВКА КАРТРИДЖА")
    print("*" * 40)
    printer.refill_ink(100)

    # 7. Финальная печать
    print("\n" + "*" * 40)
    print("7. ФИНАЛЬНАЯ ПЕЧАТЬ")
    print("*" * 40)
    printer.print_document(7)

    print("\n" + "=" * 60)
    print("ИТОГ")
    print("=" * 60)
    printer.show_status()


if __name__ == "__main__":
    demo()

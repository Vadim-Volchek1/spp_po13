from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Optional
import math


class Calculator:
    def __init__(self):
        self._display = "0"
        self._memory = 0.0
        self._current_value = 0.0
        self._operation: Optional[str] = None
        self._waiting_for_operand = False

        # Стратегии для кнопок (по умолчанию - стандартные)
        self._button_strategies: Dict[str, 'ButtonStrategy'] = {}
        self._setup_default_strategies()

    def _setup_default_strategies(self):
        # Настройка стратегий по умолчанию
        # Цифровые кнопки (0-9) - фиксированная функция
        for i in range(10):
            self._button_strategies[str(i)] = DigitButtonStrategy(str(i))

        # Арифметические операции (+, -, *, /) - фиксированная функция
        self._button_strategies["+"] = OperationButtonStrategy("+")
        self._button_strategies["-"] = OperationButtonStrategy("-")
        self._button_strategies["*"] = OperationButtonStrategy("*")
        self._button_strategies["/"] = OperationButtonStrategy("/")

        # Равно (=) - фиксированная функция
        self._button_strategies["="] = EqualsButtonStrategy()

        # Дополнительные кнопки с изменяемым назначением
        self._button_strategies["F1"] = ClearButtonStrategy()  # Очистка
        self._button_strategies["F2"] = MemoryButtonStrategy("M+")  # Память+
        self._button_strategies["F3"] = MemoryButtonStrategy("MR")  # Вызов памяти
        self._button_strategies["F4"] = ScientificButtonStrategy("sqrt")  # Корень

    @property
    def display(self) -> str:
        return self._display

    def press_button(self, button: str) -> str:
        # Нажатие кнопки - делегирование стратегии
        strategy = self._button_strategies.get(button)
        if not strategy:
            return f"Кнопка '{button}' не назначена"

        resultt = strategy.execute(self)
        return resultt

    def set_button_strategy(self, button: str, strategy: 'ButtonStrategy'):
        # Изменение назначения кнопки (смена стратегии)
        self._button_strategies[button] = strategy
        return f"Кнопка '{button}' переназначена: {strategy.get_description()}"

    def get_button_info(self, button: str) -> str:
        # Получение информации о назначении кнопки
        strategy = self._button_strategies.get(button)
        if strategy:
            return f"{button}: {strategy.get_description()}"
        return f"{button}: [не назначена]"

    def get_all_buttons(self) -> List[str]:
        # Получение списка всех кнопок
        return list(self._button_strategies.keys())

    # Методы для работы со стратегиями
    def update_display(self, value: str):
        self._display = value

    def append_to_display(self, digit: str):
        if self._waiting_for_operand:
            self._display = digit
            self._waiting_for_operand = False
        else:
            if self._display == "0":
                self._display = digit
            else:
                self._display += digit

    def get_display_value(self) -> float:
        try:
            return float(self._display)
        except ValueError:
            return 0.0

    def set_operation(self, op: str):
        self._current_value = self.get_display_value()
        self._operation = op
        self._waiting_for_operand = True

    def calculate(self) -> str:
        if not self._operation:
            return self._display

        second_operand = self.get_display_value()
        resultt = 0.0

        try:
            if self._operation == "+":
                resultt = self._current_value + second_operand
            elif self._operation == "-":
                resultt = self._current_value - second_operand
            elif self._operation == "*":
                resultt = self._current_value * second_operand
            elif self._operation == "/":
                if second_operand == 0:
                    return "Error: Division by zero"
                resultt = self._current_value / second_operand

            self._display = str(resultt)
            self._operation = None
            self._waiting_for_operand = True
            return self._display
        except ZeroDivisionError:
            return "Error: Division by zero"
        except ValueError:
            return "Error: Invalid value"
        except OverflowError:
            return "Error: Result too large"

    def clear(self):
        self._display = "0"
        self._current_value = 0.0
        self._operation = None
        self._waiting_for_operand = False

    def memory_add(self):
        self._memory += self.get_display_value()

    def memory_recall(self):
        self._display = str(self._memory)
        self._waiting_for_operand = True

    def memory_clear(self):
        self._memory = 0.0

    def scientific_operation(self, func: str) -> str:
        # Выполнение научной операции
        value = self.get_display_value()

        # Проверки на корректность
        if func in ["sqrt", "log", "ln"] and value <= 0:
            return f"Error: Invalid value for {func}"

        # Словарь операций вместо if-elif
        operations = {
            "sqrt": math.sqrt,
            "pow2": lambda v: v ** 2,
            "sin": math.radians,
            "cos": math.radians,
            "log": math.log10,
            "ln": math.log
        }

        operation = operations.get(func)
        if not operation:
            return f"Error: Unknown function {func}"

        try:
            if func in ["sin", "cos"]:
                rad_value = math.radians(value)
                if func == "sin":
                    rresult = math.sin(rad_value)
                else:
                    rresult = math.cos(rad_value)
            else:
                rresult = operation(value)

            self._display = str(rresult)
            self._waiting_for_operand = True
            return self._display
        except ValueError as ve:
            return f"Error: Invalid value for {func} - {str(ve)}"
        except OverflowError:
            return f"Error: Result too large for {func}"


# Стратегии кнопок (Strategy Interface + Concrete Strategies)

class ButtonStrategy(ABC):
    @abstractmethod
    def execute(self, calculator: Calculator) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class DigitButtonStrategy(ButtonStrategy):
    def __init__(self, digit: str):
        self._digit = digit

    def execute(self, calculator: Calculator) -> str:
        calculator.append_to_display(self._digit)
        return calculator.display

    def get_description(self) -> str:
        return f"Цифра {self._digit}"


class OperationButtonStrategy(ButtonStrategy):

    def __init__(self, operation: str):
        self._operation = operation

    def execute(self, calculator: Calculator) -> str:
        calculator.set_operation(self._operation)
        return calculator.display

    def get_description(self) -> str:
        ops = {"+": "Сложение", "-": "Вычитание", "*": "Умножение", "/": "Деление"}
        return f"Операция: {ops.get(self._operation, self._operation)}"


class EqualsButtonStrategy(ButtonStrategy):

    def execute(self, calculator: Calculator) -> str:
        return calculator.calculate()

    def get_description(self) -> str:
        return "Вычислить результат"


class ClearButtonStrategy(ButtonStrategy):
    def execute(self, calculator: Calculator) -> str:
        calculator.clear()
        return calculator.display

    def get_description(self) -> str:
        return "Очистить дисплей"


class MemoryButtonStrategy(ButtonStrategy):

    def __init__(self, mem_op: str):
        self._mem_op = mem_op

    def execute(self, calculator: Calculator) -> str:
        if self._mem_op == "M+":
            calculator.memory_add()
            return f"M+ ({calculator.display})"
        if self._mem_op == "MR":
            calculator.memory_recall()
            return calculator.display
        if self._mem_op == "MC":
            calculator.memory_clear()
            return "Memory cleared"
        return "Unknown memory op"

    def get_description(self) -> str:
        ops = {"M+": "Добавить в память", "MR": "Вызвать из памяти",
               "MC": "Очистить память"}
        return ops.get(self._mem_op, self._mem_op)


class ScientificButtonStrategy(ButtonStrategy):

    def __init__(self, func: str):
        self._func = func

    def execute(self, calculator: Calculator) -> str:
        return calculator.scientific_operation(self._func)

    def get_description(self) -> str:
        funcs = {
            "sqrt": "Квадратный корень",
            "pow2": "Возведение в квадрат",
            "sin": "Синус",
            "cos": "Косинус",
            "log": "Десятичный логарифм",
            "ln": "Натуральный логарифм"
        }
        return f"Научная функция: {funcs.get(self._func, self._func)}"


class CustomButtonStrategy(ButtonStrategy):

    def __init__(self, name: str, action: Callable[[Calculator], str],
                 description: str = "Пользовательская функция"):
        self._name = name
        self._action = action
        self._description = description

    def execute(self, calculator: Calculator) -> str:
        return self._action(calculator)

    def get_description(self) -> str:
        return f"[{self._name}] {self._description}"


# Демонстрация работы
if __name__ == "__main__":
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНА 'СТРАТЕГИЯ'")
    print("Настраиваемый калькулятор с изменяемыми функциями кнопок")

    # Создание калькулятора
    calc = Calculator()

    print("\n1. БАЗОВЫЕ ОПЕРАЦИИ (фиксированные кнопки)")
    print("Начальное состояние:", calc.display)

    # Пример: 12 + 7 =
    sequence = ["1", "2", "+", "7", "="]
    print(f"\nПоследовательность: {' '.join(sequence)}")

    for btn in sequence:
        result = calc.press_button(btn)
        print(f"  Нажата '{btn}' -> {result}")

    # 2. Демонстрация изменяемых кнопок
    print("\n2. НАСТРОЙКА ИЗМЕНЯЕМЫХ КНОПОК (F1-F4)")

    print("\nИсходные назначения:")
    for btn in ["F1", "F2", "F3", "F4"]:
        print(f"  {calc.get_button_info(btn)}")

    # Переназначение кнопок
    print("\nПереназначение кнопок...")

    # F1 - теперь квадрат числа
    print(calc.set_button_strategy("F1", ScientificButtonStrategy("pow2")))

    # F2 - теперь синус
    print(calc.set_button_strategy("F2", ScientificButtonStrategy("sin")))


    # F3 - пользовательская функция (умножение на 2)
    def multiply_by_two(c: Calculator) -> str:
        val = c.get_display_value()
        c.update_display(str(val * 2))
        return c.display


    print(calc.set_button_strategy("F3",
                                   CustomButtonStrategy("×2", multiply_by_two, "Умножение на 2")))

    # F4 - очистка памяти
    print(calc.set_button_strategy("F4", MemoryButtonStrategy("MC")))

    print("\nНовые назначения:")
    for btn in ["F1", "F2", "F3", "F4"]:
        print(f"  {calc.get_button_info(btn)}")

    # 3. Использование переназначенных кнопок
    print("\n3. ИСПОЛЬЗОВАНИЕ ПЕРЕНАЗНАЧЕННЫХ КНОПОК")

    # Вводим число 5
    calc.press_button("C")  # Очистка (если есть)
    calc.clear()
    calc.press_button("5")
    print(f"\nВведено число: {calc.display}")

    print(f"Нажимаем F1 (квадрат): {calc.press_button('F1')}")

    calc.press_button("3")
    calc.press_button("0")
    print(f"Вводим 30, нажимаем F2 (синус): {calc.press_button('F2')}")

    calc.press_button("1")
    calc.press_button("0")
    print(f"Вводим 10, нажимаем F3 (×2): {calc.press_button('F3')}")

    # 4. Сравнение стратегий
    print("\n4. СРАВНЕНИЕ РАЗЛИЧНЫХ СТРАТЕГИЙ")

    # Создадим второй калькулятор с другими настройками
    calc2 = Calculator()

    # Настроим F1-F4 по-другому
    calc2.set_button_strategy("F1", ScientificButtonStrategy("cos"))
    calc2.set_button_strategy("F2", ScientificButtonStrategy("log"))
    calc2.set_button_strategy("F3", ScientificButtonStrategy("ln"))
    calc2.set_button_strategy("F4", ScientificButtonStrategy("sqrt"))

    print("\nКалькулятор 1 (F1-F4):")
    for btn in ["F1", "F2", "F3", "F4"]:
        print(f"  {calc.get_button_info(btn)}")

    print("\nКалькулятор 2 (F1-F4):")
    for btn in ["F1", "F2", "F3", "F4"]:
        print(f"  {calc2.get_button_info(btn)}")

    # 5. Демонстрация гибкости
    print("\n5. ГИБКОСТЬ СИСТЕМЫ (смена стратегии на лету)")


    calc2.press_button("9")
    calc2.press_button("0")
    print(f"\nВведено 90 в Калькуляторе 2")

    print(f"F1 (cos): {calc2.press_button('F1')}")

    # Меняем F1 на синус и снова вычисляем
    calc2.set_button_strategy("F1", ScientificButtonStrategy("sin"))
    calc2.press_button("9")
    calc2.press_button("0")
    print("Меняем F1 на sin, вводим 90")
    print(f"F1 (sin): {calc2.press_button('F1')}")

    print("Демонстрация завершена!")
    print("Паттерн Стратегия позволил:")
    print("- Иметь фиксированные кнопки (цифры, операции)")
    print("- Изменять назначение функциональных кнопок")
    print("- Создавать пользовательские функции")
    print("- Менять поведение кнопок во время работы")

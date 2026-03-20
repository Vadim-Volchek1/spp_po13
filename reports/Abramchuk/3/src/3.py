# Strategy (Стратегия)

from abc import ABC, abstractmethod

# Абстрактный класс стратегии
class Strategy(ABC):
    @abstractmethod
    def execute(self):
        pass

# Конкретные стратегии
class NumberStrategy(Strategy):
    def __init__(self, value):
        self.value = value

    def execute(self):
        return self.value

class AddStrategy(Strategy):
    def execute(self):
        return "Выполняю сложение"

class SubStrategy(Strategy):
    def execute(self):
        return "Выполняю вычитание"

class SinStrategy(Strategy):
    def execute(self):
        return "Вычисляю синус"

class CleanHistoryStrategy(Strategy):
    def execute(self):
        return "Очищаю историю операций"

# Кнопки
class Button(ABC):
    def __init__(self, label: str, strategy: Strategy):
        self._label = label
        self._strategy = strategy

    def click(self):
        if self._strategy:
            print(f"Кнопка {self._label}: {self._strategy.execute()}")
        else:
            print(f"Кнопка {self._label} не имеет функции")

class CustomButton(Button):
    def __init__(self, _label: str, strategy: Strategy = None):
        super().__init__(_label, strategy)

    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy
        print(f"Кнопка {self._label}: Назначение изменилось")


btn_plus = Button("+", AddStrategy())
btn_one = Button("1", NumberStrategy(1))
btn_two = Button("2", NumberStrategy(2))

btn_custom = CustomButton("F1", CleanHistoryStrategy())

btn_plus.click()
btn_one.click()
btn_custom.click()

print()

btn_custom.set_strategy(SinStrategy())
btn_custom.click()

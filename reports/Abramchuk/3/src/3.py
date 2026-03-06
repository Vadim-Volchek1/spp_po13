# Command (Команда)

from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class OneCommand(Command):
    def execute(self):
        return 1

class TwoCommand(Command):
    def execute(self):
        return 2

class AddCommand(Command):
    def execute(self):
        return "Выполняю сложение"

class SubCommand(Command):
    def execute(self):
        return "Выполняю вычитание"

class SinCommand(Command):
    def execute(self):
        return "Вычисляю синус"

class CleanHistoryCommand(Command):
    def execute(self):
        return "Очищаю историю операций"

class Button:
    def __init__(self, label):
        self.label = label
        self.command = None

    def set_command(self, command: Command):
        self.command = command

    def click(self):
        if self.command:
            print(f"Кнопка {self.label}: {self.command.execute()}")
        else:
            print(f"Кнопка {self.label} пока не настроена.")


btn_plus = Button("+")
btn_one = Button("1")
btn_custom = Button("F1")

btn_plus.set_command(AddCommand())
btn_one.set_command(OneCommand())
btn_custom.set_command(CleanHistoryCommand())

btn_plus.click()
btn_one.click()
btn_custom.click()

btn_custom.set_command(SinCommand())
btn_custom.click()

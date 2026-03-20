"""
В2
Третья группа заданий (поведенческий паттерн)
2) Проект «Принтеры». В проекте должны быть реализованы
разные модели
принтеров, которые выполняют разные виды печати.
"""
from abc import ABC, abstractmethod

#Стратегии
class PrintStrategy(ABC):
    @abstractmethod
    def print(self, document_content):
        pass

    def public_def_only_for_public_def_def_pylint_live_me_along(self):
        print("\npublic_def_only_for_public_def_def_pylint_live_me_along\n")


class BWPrint(PrintStrategy):

    def print(self, document_content):
        print("Черно-белая печать ")
        print(f"Текст документа: {document_content}")

class ColorPrint(PrintStrategy):
    def print(self, document_content) :
        print("Цветная печать ")
        print(f"Текст документа (цветной): {document_content}")


class ThreeDPrint(PrintStrategy):
    def print(self, document_content):
        # В данном контексте document_content может быть именем 3D-модели
        print("3D печать ")
        print(f"Печать модели: {document_content}")


#Принтеры
class Printer:
    def __init__(self, model, strategy):
        self.model = model
        self._strategy = strategy

    def set_strategy(self, strategy):
        print(f"\nПринтер {self.model} переключен на {strategy.__class__.__name__}")
        self._strategy = strategy

    def execute(self, document):
        print(f"\nПринтер {self.model} выполняет задание...")
        self._strategy.print(document)

if __name__ == "__main__":
    bw_strategy = BWPrint()
    color_strategy = ColorPrint()
    three_d_strategy = ThreeDPrint()

    office_printer = Printer("Крепыш", bw_strategy)

    office_printer.execute("Важный текст ткст")

    office_printer.set_strategy(color_strategy)
    office_printer.execute("Цветик севицветик")

    three_d_printer = Printer("СуперБамбукЛабик", three_d_strategy)
    three_d_printer.execute("моделька")

    three_d_printer.set_strategy(bw_strategy)
    three_d_printer.execute("Чтото там.txt")

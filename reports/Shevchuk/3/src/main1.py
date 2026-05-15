"""Lab 3, task 1, variant 7.

Порождающий паттерн: Factory Method.
Преподаватель работает с несколькими студентами,
которые создаются через фабрики.
"""

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Student(ABC):
    """Абстрактный студент."""

    def __init__(self, name: str) -> None:
        if not name.strip():
            raise ValueError("Имя студента не может быть пустым.")
        self.name = name

    @abstractmethod
    def info(self) -> str:
        """Вернуть описание студента."""


# pylint: disable=too-few-public-methods
class BachelorStudent(Student):
    """Студент-бакалавр."""

    def info(self) -> str:
        return f"Студент-бакалавр: {self.name}"


# pylint: disable=too-few-public-methods
class MasterStudent(Student):
    """Студент-магистр."""

    def info(self) -> str:
        return f"Студент-магистр: {self.name}"


# pylint: disable=too-few-public-methods
class StudentFactory(ABC):
    """Абстрактная фабрика студентов."""

    @abstractmethod
    def create_student(self, name: str) -> Student:
        """Создать студента."""


# pylint: disable=too-few-public-methods
class BachelorFactory(StudentFactory):
    """Фабрика бакалавров."""

    def create_student(self, name: str) -> Student:
        return BachelorStudent(name)


# pylint: disable=too-few-public-methods
class MasterFactory(StudentFactory):
    """Фабрика магистров."""

    def create_student(self, name: str) -> Student:
        return MasterStudent(name)


class Teacher:
    """Преподаватель, работающий с несколькими студентами."""

    def __init__(self, name: str) -> None:
        if not name.strip():
            raise ValueError("Имя преподавателя не может быть пустым.")
        self.name = name
        self.students: list[Student] = []

    def add_student(self, student: Student) -> None:
        """Добавить студента."""
        self.students.append(student)

    def conduct_lecture(self) -> None:
        """Провести лекцию."""
        print(f"{self.name} проводит лекцию.")
        for student in self.students:
            print(student.info())

    def conduct_consultation(self) -> None:
        """Провести консультацию."""
        print(f"{self.name} проводит консультацию.")

    def check_laboratory_work(self) -> None:
        """Проверить лабораторную работу."""
        print(f"{self.name} проверяет лабораторную работу.")

    def accept_exam(self) -> None:
        """Принять экзамен."""
        print(f"{self.name} принимает экзамен.")

    def assign_grade(self) -> None:
        """Выставить отметки."""
        print(f"{self.name} выставляет отметки.")


def main() -> None:
    """Демонстрация работы паттерна."""
    bachelor_factory = BachelorFactory()
    master_factory = MasterFactory()

    teacher = Teacher("Крощенко А.А.")
    teacher.add_student(bachelor_factory.create_student("Иван"))
    teacher.add_student(bachelor_factory.create_student("Алина"))
    teacher.add_student(master_factory.create_student("Дмитрий"))

    teacher.conduct_lecture()
    teacher.conduct_consultation()
    teacher.check_laboratory_work()
    teacher.accept_exam()
    teacher.assign_grade()


if __name__ == "__main__":
    main()

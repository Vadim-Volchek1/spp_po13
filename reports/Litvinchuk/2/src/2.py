from abc import ABC, abstractmethod

# Обобщение


class Person:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"


class Student(Person):
    def __init__(self, name: str):
        super().__init__(name)
        self.courses = []

    def enroll(self, course):
        course.add_student(self)
        self.courses.append(course)

    def __str__(self):
        return f"Student: {self.name}"


class Teacher(Person):
    def assign_grade(self, student, course, grade, archive_obj):
        archive_obj.save_grade(student, course, grade)


# Реализация (интерфейс)


class Graded(ABC):
    @abstractmethod
    def save_grade(self, student, course, grade):
        pass


# Агрегация


class Archive(Graded):
    def __init__(self):
        self.records = []

    def save_grade(self, student, course, grade):
        self.records.append((student.name, course.title, grade))

    def show_records(self):
        for record in self.records:
            print(f"Студент: {record[0]}, " f"Курс: {record[1]}, " f"Оценка: {record[2]}")


class Course:
    def __init__(self, title: str, teacher: Teacher):
        self.title = title
        self.teacher = teacher
        self.students = []

    def add_student(self, student: Student):
        self.students.append(student)

    def __str__(self):
        return f"Курс: {self.title}, Преподаватель: {self.teacher.name}"


# Демонстрация


if __name__ == "__main__":
    archive_storage = Archive()

    teacher1 = Teacher("Иванов")
    teacher2 = Teacher("Петров")

    course1 = Course("Python", teacher1)
    course2 = Course("Databases", teacher2)

    student1 = Student("Алексей")
    student2 = Student("Мария")

    student1.enroll(course1)
    student2.enroll(course1)
    student2.enroll(course2)

    teacher1.assign_grade(student1, course1, 5, archive_storage)
    teacher1.assign_grade(student2, course1, 4, archive_storage)
    teacher2.assign_grade(student2, course2, 5, archive_storage)

    archive_storage.show_records()

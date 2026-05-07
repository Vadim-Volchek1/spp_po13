"""Lab 3, task 1, variant 7.

Creational pattern example: Factory Method.
The teacher works with several students created by factories.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Student:
    """Represent a student."""

    def __init__(self, name: str, group: str, level: str, diligence: int) -> None:
        """Initialize a student."""
        if not name.strip():
            raise ValueError("Student name cannot be empty.")
        if not group.strip():
            raise ValueError("Group cannot be empty.")
        if diligence < 1 or diligence > 10:
            raise ValueError("Diligence must be between 1 and 10.")

        self.name = name
        self.group = group
        self.level = level
        self.diligence = diligence
        self.grades: list[int] = []

    def attend_lecture(self, topic: str) -> str:
        """Attend a lecture."""
        return f"{self.level} student {self.name} attended lecture: {topic}"

    def attend_consultation(self, topic: str) -> str:
        """Attend a consultation."""
        return f"{self.level} student {self.name} attended consultation: {topic}"

    def submit_laboratory_work(self, lab_name: str) -> int:
        """Submit a laboratory work and get a mark."""
        grade = min(10, self.diligence + 1)
        self.grades.append(grade)
        print(f"{self.name} submitted '{lab_name}' and got {grade}")
        return grade

    def pass_exam(self, subject: str) -> int:
        """Pass an exam and get a mark."""
        grade = min(10, self.diligence + 2)
        self.grades.append(grade)
        print(f"{self.name} passed exam in '{subject}' and got {grade}")
        return grade

    def receive_grade(self, subject: str, grade: int) -> None:
        """Receive a final grade."""
        if grade < 0 or grade > 10:
            raise ValueError("Grade must be between 0 and 10.")

        self.grades.append(grade)
        print(f"{self.name} received final grade {grade} in '{subject}'")

    def average_grade(self) -> float:
        """Return the average grade."""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def __str__(self) -> str:
        """Return string representation."""
        return f"Student(name='{self.name}', group='{self.group}', level='{self.level}')"


class BachelorStudent(Student):
    """Represent a bachelor student."""

    def __init__(self, name: str, group: str) -> None:
        """Initialize a bachelor student."""
        super().__init__(name, group, "Bachelor", 7)


class MasterStudent(Student):
    """Represent a master student."""

    def __init__(self, name: str, group: str) -> None:
        """Initialize a master student."""
        super().__init__(name, group, "Master", 9)


class StudentCreator(ABC):
    """Abstract creator for students."""

    @abstractmethod
    def create_student(self, name: str, group: str) -> Student:
        """Create a student."""


# pylint: disable=too-few-public-methods
class BachelorCreator(StudentCreator):
    """Create bachelor students."""

    def create_student(self, name: str, group: str) -> Student:
        """Create a bachelor student."""
        return BachelorStudent(name, group)


# pylint: disable=too-few-public-methods
class MasterCreator(StudentCreator):
    """Create master students."""

    def create_student(self, name: str, group: str) -> Student:
        """Create a master student."""
        return MasterStudent(name, group)


class Teacher:
    """Represent a teacher working with several students."""

    def __init__(self, name: str, subject: str) -> None:
        """Initialize a teacher."""
        if not name.strip():
            raise ValueError("Teacher name cannot be empty.")
        if not subject.strip():
            raise ValueError("Subject cannot be empty.")

        self.name = name
        self.subject = subject
        self.students: list[Student] = []

    def add_student(self, student: Student) -> None:
        """Add a student to the teacher's list."""
        self.students.append(student)

    def show_students(self) -> None:
        """Show all students."""
        print(f"\nStudents of teacher {self.name}:")
        for student in self.students:
            print(student)

    def conduct_lecture(self, topic: str) -> None:
        """Conduct a lecture for all students."""
        print(f"\nTeacher {self.name} conducts lecture on '{topic}'")
        for student in self.students:
            print(student.attend_lecture(topic))

    def conduct_consultation(self, topic: str) -> None:
        """Conduct a consultation for all students."""
        print(f"\nTeacher {self.name} conducts consultation on '{topic}'")
        for student in self.students:
            print(student.attend_consultation(topic))

    def check_laboratory_work(self, lab_name: str) -> None:
        """Check laboratory work of all students."""
        print(f"\nTeacher {self.name} checks laboratory work '{lab_name}'")
        for student in self.students:
            student.submit_laboratory_work(lab_name)

    def accept_exam(self) -> None:
        """Accept exam from all students."""
        print(f"\nTeacher {self.name} accepts exam in '{self.subject}'")
        for student in self.students:
            student.pass_exam(self.subject)

    def assign_final_grade(self) -> None:
        """Assign final grades to all students."""
        print(f"\nTeacher {self.name} assigns final grades")
        for student in self.students:
            final_grade = round(student.average_grade())
            student.receive_grade(self.subject, final_grade)


def main() -> None:
    """Demonstrate the factory method example."""
    bachelor_factory = BachelorCreator()
    master_factory = MasterCreator()

    student_1 = bachelor_factory.create_student("Ivan Petrov", "PO-13")
    student_2 = bachelor_factory.create_student("Alina Sokolova", "PO-13")
    student_3 = master_factory.create_student("Dmitry Kovalev", "POM-21")

    teacher = Teacher("Kroshchenko A.A.", "Design Patterns")
    teacher.add_student(student_1)
    teacher.add_student(student_2)
    teacher.add_student(student_3)

    teacher.show_students()
    teacher.conduct_lecture("Factory Method")
    teacher.conduct_consultation("Creational patterns")
    teacher.check_laboratory_work("Lab 3")
    teacher.accept_exam()
    teacher.assign_final_grade()


if __name__ == "__main__":
    main()

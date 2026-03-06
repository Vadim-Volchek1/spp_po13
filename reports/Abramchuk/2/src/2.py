class Person:
    def __init__(self, name):
        self.name = name

class Elective:
    def __init__(self, title, teacher):
        self.title = title
        self.teacher = teacher
        self.students = []
        self.is_active = True

    def add_student(self, student):
        if self.is_active:
            self.students.append(student)
            print(f"Студент {student.name} зачислен на курс '{self.title}'")

    def finish(self, archive_obj):
        if self.is_active:
            self.is_active = False
            for student in self.students:
                self.teacher.evaluate_student(student, self.title, 10, archive_obj)

class Archive:
    def __init__(self):
        self._records = []

    def add_record(self, data, student_name, elective_name, grade):
        record = {
            "date": data,
            "student": student_name,
            "elective": elective_name,
            "grade": grade
        }
        self._records.append(record)

    def show_all(self):
        for record in self._records:
            print(f"{record['date']} | {record['student']} | {record['elective']} | Оценка: {record['grade']}")

class Student(Person):
    def sing_up(self, elective):
        elective.add_student(self)

class Teacher(Person):
    def create_elective(self, title):
        print(f"Преподаватель {self.name} открыл запись на курс '{title}'")
        return Elective(title, self)

    def evaluate_student(self, student, elective_title, grade, archive_obj):
        print(f"Преподаватель {self.name} выставил оценку {grade} студенту {student.name}")
        archive_obj.add_record("22.01.2026", student.name, elective_title, grade)


archive = Archive()
nikolay = Teacher("Николай Николаевич")
lieonid = Teacher("Леонид Леонидович")

python_elective = nikolay.create_elective("Python")
java_elective = lieonid.create_elective("Java")

sacha = Student("Саша")
pacha = Student("Паша")

sacha.sing_up(python_elective)
pacha.sing_up(python_elective)
sacha.sing_up(java_elective)

python_elective.finish(archive)
java_elective.finish(archive)

archive.show_all()

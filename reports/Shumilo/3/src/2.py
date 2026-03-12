class Employee:
    def __init__(self, name, department, position, salary):
        self.name = name
        self.department = department
        self.position = position
        self.salary = salary
        self.subordinates = []
        self.boss = None

    def add_subordinate(self, employee):
        self.subordinates.append(employee)
        employee.boss = self

    def remove_subordinate(self, employee):
        if employee in self.subordinates:
            self.subordinates.remove(employee)
            employee.boss = None

    def info(self, indent=0):
        print(" " * indent + f"{self.position}: {self.name} | Отдел: {self.department} | Зарплата: {self.salary}")
        for sub in self.subordinates:
            sub.info(indent + 4)

    def get_boss(self):
        return self.boss

    def get_subordinates(self):
        return self.subordinates

class EmployeeIterator:
    def __init__(self, root):
        self.stack = [(root, 0)]

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration

        current, level = self.stack.pop()


        for sub in reversed(current.subordinates):
            self.stack.append((sub, level + 1))

        return current, level

def generate_salary_report(root_employee):
    iterator = EmployeeIterator(root_employee)

    printed_departments = set()
    total_salary = 0

    print("\nОТЧЁТ ПО ЗАРПЛАТАМ")

    for emp, level in iterator:

        if emp.department not in printed_departments:
            print(f"\nОтдел: {emp.department}")
            printed_departments.add(emp.department)

        indent = "    " * (level + 1)

        print(f"{indent}{emp.position}: {emp.name} — {emp.salary} руб.")

        total_salary += emp.salary

    print("\nИТОГО ЗАТРАТ НА ЗАРПЛАТЫ:", total_salary, "руб.")



def find_employee_by_name(root, name):
    for emp in EmployeeIterator(root):
        if emp.name.lower() == name.lower():
            return emp
    return None
def add(root):
    print("\nДобавление сотрудника")
    name = input("ФИО: ")
    dept = input("Отдел: ")
    pos = input("Должность: ")
    salary = float(input("Зарплата: "))
    boss_name = input("Кому подчиняется (ФИО): ")
    boss = find_employee_by_name(root, boss_name)
    if not boss:
        print("Ошибка: начальник не найден.")
        return
    new_emp = Employee(name, dept, pos, salary)
    boss.add_subordinate(new_emp)
    print(f"Сотрудник {name} добавлен под руководителя {boss.name}.")

def interactive_menu(root):
    while True:
        print("\nМЕНЮ УПРАВЛЕНИЯ КОМПАНИЕЙ")
        print("1 — Показать структуру компании\n2 — Добавить сотрудника\n")
        print("\n3 — Удалить сотрудника\n4 — Показать отчёт по зарплатам\n0 — Выход")
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            print("\nСТРУКТУРА КОМПАНИИ:")
            root.info()
        elif choice == "2":
            add(root)
        elif choice == "3":
            print("\nУдаление сотрудника")
            name = input("Введите ФИО сотрудника: ")
            emp = find_employee_by_name(root, name)
            if not emp:
                print("Сотрудник не найден.")
                continue
            if emp is root:
                print("Нельзя удалить директора!")
                continue
            boss = emp.get_boss()
            boss.remove_subordinate(emp)
            print(f"Сотрудник {name} удалён.")
        elif choice == "4":
            generate_salary_report(root)
        elif choice == "0":
            print("Выход из программы.")
            break

if __name__ == "__main__":

    director = Employee("Иванов И.И.", "Управление", "Директор", 200000)
    head_dev = Employee("Петров П.П.", "Разработка", "Руководитель отдела", 150000)
    dev1 = Employee("Сидоров С.С.", "Разработчик", "Разработчик", 100000)
    dev2 = Employee("Кузнецов К.К.", "Разработчик", "Разработчик", 95000)
    hr = Employee("Смирнова А.А.", "HR", "HR-менеджер", 80000)


    director.add_subordinate(head_dev)
    director.add_subordinate(hr)
    head_dev.add_subordinate(dev1)
    head_dev.add_subordinate(dev2)

    interactive_menu(director)

from __future__ import annotations

from typing import Optional

from burger_shop import (
    BurgerCafe,
    BurgerType,
    DrinkType,
    PackagingType,
    format_menu,
)
from it_company import Employee, ITCompany
from payroll import SimpleSalaryCalculator, generate_salary_report


def _read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid integer. Try again.")


def _read_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Invalid number. Try again.")


def run_burger_shop() -> None:
    print("=== Project: Burger cafe (Builder pattern) ===")
    print(format_menu())

    burger_choice = _read_int("Choose burger (1..): ")
    drink_choice = _read_int("Choose drink (1..): ")
    packaging_choice = _read_int("Choose packaging (1..): ")

    burger_types = list(BurgerType)
    drink_types = list(DrinkType)
    packaging_types = list(PackagingType)

    try:
        btype = burger_types[burger_choice - 1]
        dtype = drink_types[drink_choice - 1]
        ptype = packaging_types[packaging_choice - 1]
    except IndexError:
        print("Invalid choices. Returning to menu.")
        return

    order = BurgerCafe.create_order(btype=btype, dtype=dtype, ptype=ptype)
    print("\nOrder created.")
    print(f"Burger: {order.burger.btype.value} ({order.burger.cost:.2f})")
    print(f"Drink: {order.drink.dtype.value} ({order.drink.cost:.2f})")
    print(f"Packaging: {order.packaging.ptype.value} ({order.packaging.cost:.2f})")
    print(f"Total cost: {order.total_cost():.2f}")


def _build_employee_interactively(employee_id: int) -> Employee:
    print(f"--- Creating employee id={employee_id} ---")
    full_name = input("Full name: ").strip()
    department = input("Department: ").strip()
    position = input("Position: ").strip()
    base_salary = _read_float("Base salary: ")
    seniority_years = _read_int("Seniority (years): ")
    return Employee(
        employee_id=employee_id,
        full_name=full_name,
        department=department,
        position=position,
        base_salary=base_salary,
        seniority_years=seniority_years,
    )


def _read_manager_id(company: ITCompany) -> int | None:
    existing_ids = sorted(emp.employee_id for emp in company.get_all_employees())
    if existing_ids:
        print(f"Existing employee ids (can be manager): {existing_ids}")
    else:
        print("No managers yet. First employee must be a root (empty manager id).")

    while True:
        raw = input("Manager id (empty for root): ").strip()
        if not raw:
            return None
        try:
            manager_id = int(raw)
        except ValueError:
            print("Manager id must be an integer or empty.")
            continue

        if manager_id not in existing_ids:
            print("Manager id not found among existing employees. Choose from the list above or leave empty.")
            continue
        return manager_id


def run_it_company() -> Optional[ITCompany]:
    print("=== Project: IT company (Composite pattern) ===")
    company = ITCompany(company_name="IT Company")

    n = _read_int("How many employees to add initially? ")
    for _ in range(n):
        emp_id = _read_int("Employee id (unique): ")
        manager_id = _read_manager_id(company)
        emp = _build_employee_interactively(emp_id)
        try:
            company.add_employee(emp, manager_id=manager_id)
        except ValueError as exc:
            print(f"Input error: {exc}")
            print("Employee was not added. Try this employee again.")

    company.print_org()

    print("\nAdd one more employee? (y/n)")
    if input().strip().lower() == "y":
        emp_id = _read_int("Employee id (unique): ")
        manager_id = _read_manager_id(company)
        emp = _build_employee_interactively(emp_id)
        try:
            company.add_employee(emp, manager_id=manager_id)
        except ValueError as exc:
            print(f"Input error: {exc}")
            print("Employee was not added.")

    print("\nRemove one employee by id? (y/n)")
    if input().strip().lower() == "y":
        rem_id = _read_int("Employee id to remove: ")
        try:
            company.remove_employee(rem_id)
        except ValueError as exc:
            print(f"Input error: {exc}")

    print("\nUpdated org chart:")
    company.print_org()
    return company


def run_payroll(company: Optional[ITCompany]) -> None:
    print("=== Project: Payroll calculation (Visitor pattern) ===")
    if company is None:
        # Demo company for direct payroll run.
        company = ITCompany(company_name="Demo IT Company")
        ceo = Employee(1, "Ivan Petrov", "Backend", "Team Lead", 2000.0, 6)
        dev1 = Employee(2, "Anna Smirnova", "Backend", "Developer", 1200.0, 3)
        dev2 = Employee(3, "Max Korolev", "Frontend", "Developer", 1100.0, 2)
        company.add_employee(ceo, manager_id=None)
        company.add_employee(dev1, manager_id=1)
        company.add_employee(dev2, manager_id=None)

    # Department bonuses (optional business data).
    calculator = SimpleSalaryCalculator(
        department_bonus={
            "Backend": 150.0,
            "Frontend": 100.0,
            "QA": 80.0,
        }
    )

    report = generate_salary_report(company=company, calculator=calculator)
    print(report)


def main() -> None:
    company: Optional[ITCompany] = None

    while True:
        print("\n=== Lab 3 Menu ===")
        print("1) Burger cafe")
        print("2) IT company")
        print("3) Payroll report (uses last IT company)")
        print("0) Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            run_burger_shop()
        elif choice == "2":
            company = run_it_company()
        elif choice == "3":
            run_payroll(company=company)
        elif choice == "0":
            break
        else:
            print("Unknown option. Try again.")


if __name__ == "__main__":
    main()

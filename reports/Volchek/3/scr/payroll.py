from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from it_company import Employee, EmployeeVisitor, ITCompany


class SalaryCalculator(Protocol):
    def compute_salary(self, emp: Employee) -> float: ...


@dataclass
class SimpleSalaryCalculator:
    """
    Salary formula (used by the visitor).
    This keeps the behavioral pattern logic separate from business formula.
    """

    department_bonus: dict[str, float]
    subordinate_bonus_rate: float = 0.03

    def compute_salary(self, emp: Employee) -> float:
        bonus_dept = self.department_bonus.get(emp.department, 0.0)
        bonus_subs = emp.base_salary * self.subordinate_bonus_rate * len(emp.subordinates)
        # Seniority bonus grows with years.
        seniority_bonus = emp.base_salary * 0.01 * max(emp.seniority_years, 0)
        return emp.base_salary + bonus_dept + bonus_subs + seniority_bonus


class SalaryReportVisitor(EmployeeVisitor):
    """Visitor that traverses a hierarchy and creates report lines."""

    def __init__(self, calculator: SalaryCalculator) -> None:
        self._calculator = calculator
        self._lines: list[str] = []
        self._employees: list[Employee] = []

    def visit(self, emp: Employee) -> None:
        self._employees.append(emp)
        salary = self._calculator.compute_salary(emp)
        self._lines.append(
            f"{emp.department:>10} | {emp.seniority_years:>3} yrs | "
            f"{emp.full_name:<20} | {emp.position:<15} | {salary:>10.2f}"
        )

    @property
    def employees(self) -> list[Employee]:
        return list(self._employees)

    def build_report(self, company: ITCompany) -> str:
        # Behavioral requirement: employees are ordered by seniority for each department.
        employees_sorted = sorted(self._employees, key=lambda e: (e.department, -e.seniority_years))

        # Rebuild lines in the required order (lines list is based on traversal order).
        calculator = self._calculator
        lines: list[str] = []
        for emp in employees_sorted:
            salary = calculator.compute_salary(emp)
            lines.append(
                f"{emp.department:>10} | {emp.seniority_years:>3} yrs | "
                f"{emp.full_name:<20} | {emp.position:<15} | {salary:>10.2f}"
            )

        header = (
            f"=== Salary Report for {company.company_name} ===\n"
            f"{'Department':>10} | {'Seniority':>10} | {'Full name':<20} | {'Position':<15} | {'Salary':>10}\n"
            + "-" * 86
        )
        return header + "\n" + "\n".join(lines)


def generate_salary_report(company: ITCompany, calculator: SalaryCalculator) -> str:
    visitor = SalaryReportVisitor(calculator=calculator)
    for root in company.roots:
        root.accept(visitor)
    return visitor.build_report(company=company)

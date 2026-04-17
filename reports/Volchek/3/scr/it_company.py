from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Employee:
    """
    Composite (structural pattern):
    an employee may have subordinates and forms a hierarchy (tree).
    """

    employee_id: int
    full_name: str
    department: str
    position: str
    base_salary: float
    seniority_years: int
    subordinates: list[Employee] = field(default_factory=list)

    def add_subordinate(self, emp: Employee) -> None:
        if emp not in self.subordinates:
            self.subordinates.append(emp)

    def remove_subordinate(self, emp: Employee) -> None:
        if emp in self.subordinates:
            self.subordinates.remove(emp)

    def accept(self, visitor: "EmployeeVisitor") -> None:
        visitor.visit(self)
        for child in self.subordinates:
            child.accept(visitor)


class EmployeeVisitor:
    """Marker base class for visitor (behavioral pattern support)."""

    def visit(self, emp: Employee) -> None:  # pragma: no cover
        raise NotImplementedError


class ITCompany:
    """
    Manages employees hierarchy.
    Provides add/remove operations required by the assignment.
    """

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name
        self._employees_by_id: dict[int, Employee] = {}
        self._roots: list[Employee] = []

    @property
    def roots(self) -> list[Employee]:
        return list(self._roots)

    def add_employee(self, emp: Employee, manager_id: int | None = None) -> None:
        if emp.employee_id in self._employees_by_id:
            raise ValueError(f"Employee id {emp.employee_id} already exists.")

        if manager_id is None:
            self._employees_by_id[emp.employee_id] = emp
            self._roots.append(emp)
            return

        manager = self._employees_by_id.get(manager_id)
        if manager is None:
            raise ValueError(f"Manager id {manager_id} not found.")

        self._employees_by_id[emp.employee_id] = emp
        manager.add_subordinate(emp)

    def remove_employee(self, employee_id: int) -> None:
        emp = self._employees_by_id.get(employee_id)
        if emp is None:
            raise ValueError(f"Employee id {employee_id} not found.")

        # Remove from roots or from its manager's subordinates.
        if emp in self._roots:
            self._roots.remove(emp)
        else:
            for candidate in self._employees_by_id.values():
                if emp in candidate.subordinates:
                    candidate.remove_subordinate(emp)
                    break

        # Also remove the entire subtree from the index.
        to_delete: list[Employee] = []

        def collect_subtree(node: Employee) -> None:
            to_delete.append(node)
            for ch in node.subordinates:
                collect_subtree(ch)

        collect_subtree(emp)
        for node in to_delete:
            self._employees_by_id.pop(node.employee_id, None)

    def get_employee(self, employee_id: int) -> Employee:
        return self._employees_by_id[employee_id]

    def get_all_employees(self) -> list[Employee]:
        return list(self._employees_by_id.values())

    def print_org(self) -> None:
        print(f"=== {self.company_name} org chart ===")

        def dfs(node: Employee, depth: int) -> None:
            prefix = "  " * depth + "- "
            print(
                f"{prefix}[{node.employee_id}] {node.full_name} | {node.department} | {node.position} | "
                f"seniority={node.seniority_years} | salary={node.base_salary:.2f}"
            )
            for ch in node.subordinates:
                dfs(ch, depth + 1)

        if not self._roots:
            print("(no employees)")
            return
        for root in self._roots:
            dfs(root, 0)

from typing import List
from models.employee import Employee
from collections import defaultdict


def generate_payout_report(employees: List[Employee]) -> str:
    output_lines = []
    departments = defaultdict(list)

    # Группируем сотрудников по отделам
    for emp in employees:
        departments[emp.department].append(emp)

    # Формируем отчёт по каждому отделу
    for dept, emps in departments.items():
        output_lines.append(dept)
        total_hours = 0
        total_payout = 0

        for emp in emps:
            payout = emp.payout
            total_hours += emp.hours_worked
            total_payout += payout
            output_lines.append(
                f"-------------- {emp.name:<22} {emp.hours_worked:<7} {int(emp.hourly_rate):<5} ${int(payout)}"
            )

        output_lines.append(f"{'':>38}{total_hours:<13} ${int(total_payout)}")

    return "\n".join(output_lines)

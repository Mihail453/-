from typing import List
from models.employee import Employee

POSSIBLE_RATE_FIELDS = {"hourly_rate", "rate", "salary"}


def parse_csv_line(header: List[str], line: str) -> Employee:
    values = line.strip().split(',')
    data = dict(zip(header, values))

    # Нормализуем названия полей
    rate_key = next((key for key in POSSIBLE_RATE_FIELDS if key in data), None)
    if rate_key is None:
        raise ValueError("CSV is missing a rate column")

    return Employee(
        name=data["name"],
        email=data["email"],
        department=data["department"],
        hours_worked=int(data["hours_worked"]),
        hourly_rate=float(data[rate_key])
    )


def read_employees(filenames: List[str]) -> List[Employee]:
    employees = []
    for filename in filenames:
        with open(filename, encoding='utf-8') as f:
            lines = f.readlines()
            header = lines[0].strip().split(',')
            for line in lines[1:]:
                if line.strip():
                    employees.append(parse_csv_line(header, line))
    return employees
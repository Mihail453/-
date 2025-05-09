import pytest
from reader.csv_reader import read_employees
from models.employee import Employee
from reports.payout import generate_payout_report
import tempfile
import os


def create_temp_csv(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".csv", text=True)
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(content)
    return path


def test_read_employees_with_different_rate_fields():
    csv1 = """id,email,name,department,hours_worked,rate
1,test1@example.com,Test One,Sales,100,20
"""
    csv2 = """id,email,name,department,hours_worked,salary
2,test2@example.com,Test Two,Engineering,120,30
"""
    csv3 = """id,email,name,department,hours_worked,hourly_rate
3,test3@example.com,Test Three,Marketing,90,25
"""

    files = [create_temp_csv(csv) for csv in (csv1, csv2, csv3)]

    employees = read_employees(files)

    assert len(employees) == 3

    assert employees[0] == Employee(
        name="Test One",
        email="test1@example.com",
        department="Sales",
        hours_worked=100,
        hourly_rate=20.0
    )
    assert employees[1] == Employee(
        name="Test Two",
        email="test2@example.com",
        department="Engineering",
        hours_worked=120,
        hourly_rate=30.0
    )
    assert employees[2] == Employee(
        name="Test Three",
        email="test3@example.com",
        department="Marketing",
        hours_worked=90,
        hourly_rate=25.0
    )

    for f in files:
        os.remove(f)

def test_read_employees_with_missing_hourly_column():
    broken_csv = """id,email,name,department,hours_worked,rate_wrong
4,test4@example.com,Test Four,Support,80,18
"""
    file_path = create_temp_csv(broken_csv)

    with pytest.raises(ValueError):
        read_employees([file_path])

    os.remove(file_path)


def test_read_employees_with_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        read_employees(["not_a_real_file.csv"])


def test_generate_payout_report_format():
    employees = [
        Employee(name="Alice", email="alice@example.com", department="Marketing", hours_worked=160, hourly_rate=50),
        Employee(name="Bob", email="bob@example.com", department="Design", hours_worked=150, hourly_rate=40),
        Employee(name="Carol", email="carol@example.com", department="Design", hours_worked=170, hourly_rate=60)
    ]

    report = generate_payout_report(employees)

    assert "Marketing" in report
    assert "Design" in report
    assert "Alice" in report
    assert "$8000" in report  # Alice: 160*50
    assert "$6000" in report  # Bob: 150*40
    assert "$10200" in report  # Carol: 170*60
    assert "$16200" in report  # Total for Design
    assert "$8000" in report  # Total for Marketing
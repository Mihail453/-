import argparse
from reader.csv_reader import read_employees
from reports import get_report


def main():
    parser = argparse.ArgumentParser(description="Salary report generator")
    parser.add_argument("files", nargs='+', help="CSV files with employee data")
    parser.add_argument("--report", required=True, help="Report type (e.g., payout)")
    args = parser.parse_args()

    try:
        employees = read_employees(args.files)
        report_func = get_report(args.report)
        report_text = report_func(employees)
        print(report_text)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

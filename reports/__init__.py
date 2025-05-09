from typing import Callable, Dict
from models.employee import Employee
from reports.payout import generate_payout_report


ReportFunction = Callable[[list[Employee]], str]

# Здесь регистрируются все доступные отчеты
REPORTS: Dict[str, ReportFunction] = {
    "payout": generate_payout_report,
}


def get_report(name: str) -> ReportFunction:
    if name not in REPORTS:
        raise ValueError(f"Unknown report type: {name}")
    return REPORTS[name]

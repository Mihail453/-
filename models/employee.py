from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    email: str
    department: str
    hours_worked: int
    hourly_rate: float

    @property
    def payout(self) -> float:
        return self.hours_worked * self.hourly_rate

"""
Expense model definition.
Defines the structure of an expense record for the system.
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Expense:
    id: Optional[int]
    user_id: int
    amount: float
    category: str
    description: str
    date: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat()
        }

    @staticmethod
    def from_dict(data: dict) -> "Expense":
        return Expense(
            id=data.get("id"),
            user_id=data["user_id"],
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=datetime.fromisoformat(data["date"])
        )

    def is_valid(self) -> bool:
        """Check if the expense contains valid data."""
        return self.amount > 0 and bool(self.category.strip()) and bool(self.description.strip())

    def update(self, **kwargs) -> None:
        """Update expense fields dynamically."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def summary(self) -> str:
        """Generate a brief summary string of the expense."""
        return f"{self.date.date()} - {self.category}: ${self.amount:.2f} ({self.description})"

    def matches_category(self, target_category: str) -> bool:
        """Check if the expense belongs to a given category (case insensitive)."""
        return self.category.lower() == target_category.lower()

    def is_within_date_range(self, start_date: datetime, end_date: datetime) -> bool:
        """Check if the expense falls within a specific date range."""
        return start_date <= self.date <= end_date

    def formatted(self, currency_symbol: str = "$") -> str:
        """Return a formatted string of the expense for display."""
        return f"{self.date.strftime('%Y-%m-%d')} | {self.category:<15} | {currency_symbol}{self.amount:>8.2f} | {self.description}"

    def clone(self, new_id: Optional[int] = None) -> "Expense":
        """Create a copy of the expense, optionally with a new ID."""
        return Expense(
            id=new_id,
            user_id=self.user_id,
            amount=self.amount,
            category=self.category,
            description=self.description,
            date=self.date
        )

    def apply_discount(self, percent: float) -> None:
        """Apply a percentage discount to the expense amount."""
        if 0 < percent < 100:
            self.amount -= self.amount * (percent / 100)

    def categorize(self, category_mapping: dict) -> None:
        """Reassign the category based on a mapping if matched."""
        key = self.category.lower()
        if key in category_mapping:
            self.category = category_mapping[key]

    def __eq__(self, other: object) -> bool:
        """Check if two expenses are equal (excluding ID)."""
        if not isinstance(other, Expense):
            return NotImplemented
        return (
            self.user_id == other.user_id and
            self.amount == other.amount and
            self.category == other.category and
            self.description == other.description and
            self.date == other.date
        )

    def contains_keyword(self, keyword: str) -> bool:
        """Check if a keyword exists in the description (case insensitive)."""
        return keyword.lower() in self.description.lower()

    @staticmethod
    def filter_by_category(expenses: List["Expense"], category: str) -> List["Expense"]:
        return [e for e in expenses if e.matches_category(category)]

    @staticmethod
    def filter_by_date_range(expenses: List["Expense"], start: datetime, end: datetime) -> List["Expense"]:
        return [e for e in expenses if e.is_within_date_range(start, end)]

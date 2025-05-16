"""
Expense service layer.
Provides business logic for managing expenses.
"""

from typing import List, Optional, Dict
from datetime import datetime
from collections import defaultdict
import csv
import json
from app.models.expense import Expense

class ExpenseService:
    def __init__(self):
        self.expenses: List[Expense] = []

    def add_expense(self, expense: Expense) -> None:
        if not expense.is_valid():
            raise ValueError("Invalid expense data")
        self.expenses.append(expense)

    def get_all_expenses(self) -> List[Expense]:
        return self.expenses

    def get_expense_by_id(self, expense_id: int) -> Optional[Expense]:
        return next((e for e in self.expenses if e.id == expense_id), None)

    def delete_expense(self, expense_id: int) -> bool:
        expense = self.get_expense_by_id(expense_id)
        if expense:
            self.expenses.remove(expense)
            return True
        return False

    def update_expense(self, expense_id: int, **updates) -> bool:
        expense = self.get_expense_by_id(expense_id)
        if expense:
            expense.update(**updates)
            return True
        return False

    def filter_expenses_by_category(self, category: str) -> List[Expense]:
        return Expense.filter_by_category(self.expenses, category)

    def filter_expenses_by_date_range(self, start: datetime, end: datetime) -> List[Expense]:
        return Expense.filter_by_date_range(self.expenses, start, end)

    def total_amount(self) -> float:
        return sum(e.amount for e in self.expenses)

    def average_amount(self) -> float:
        return self.total_amount() / len(self.expenses) if self.expenses else 0.0

    def total_amount_by_category(self) -> Dict[str, float]:
        category_totals: Dict[str, float] = defaultdict(float)
        for expense in self.expenses:
            category_totals[expense.category] += expense.amount
        return dict(category_totals)

    def find_duplicates(self) -> List[Expense]:
        seen = set()
        duplicates = []
        for expense in self.expenses:
            key = (expense.user_id, expense.amount, expense.category, expense.description, expense.date)
            if key in seen:
                duplicates.append(expense)
            else:
                seen.add(key)
        return duplicates

    def get_expenses_containing_keyword(self, keyword: str) -> List[Expense]:
        return [e for e in self.expenses if e.contains_keyword(keyword)]

    def get_recent_expenses(self, limit: int = 5) -> List[Expense]:
        return sorted(self.expenses, key=lambda e: e.date, reverse=True)[:limit]

    def categorize_all(self, category_mapping: Dict[str, str]) -> None:
        for expense in self.expenses:
            expense.categorize(category_mapping)

    def apply_discount_to_category(self, category: str, percent: float) -> None:
        for expense in self.expenses:
            if expense.matches_category(category):
                expense.apply_discount(percent)

    def export_to_csv(self, file_path: str) -> None:
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.expenses[0].to_dict().keys())
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense.to_dict())

    def export_to_json(self, file_path: str) -> None:
        with open(file_path, mode='w', encoding='utf-8') as jsonfile:
            json.dump([e.to_dict() for e in self.expenses], jsonfile, indent=4)

    def import_from_json(self, file_path: str) -> None:
        with open(file_path, mode='r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            for item in data:
                self.add_expense(Expense.from_dict(item))

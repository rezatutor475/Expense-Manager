"""
Schemas for expense request and response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date

class ExpenseCreate(BaseModel):
    title: str = Field(..., example="Grocery shopping")
    amount: float = Field(..., gt=0, example=75.50)
    category: str = Field(..., example="Food")
    date: date = Field(..., example="2024-05-01")
    notes: Optional[str] = Field(None, example="Weekly groceries")

class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Grocery shopping")
    amount: Optional[float] = Field(None, gt=0, example=75.50)
    category: Optional[str] = Field(None, example="Food")
    date: Optional[date] = Field(None, example="2024-05-01")
    notes: Optional[str] = Field(None, example="Weekly groceries")

class ExpenseResponse(ExpenseCreate):
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True

class ExpenseSummaryByCategory(BaseModel):
    category: str
    total_amount: float

class TotalExpenseStat(BaseModel):
    total_expense: float

class DailyAverageExpense(BaseModel):
    average: float
    start_date: Optional[date]
    end_date: Optional[date]

class PeakExpenseDay(BaseModel):
    date: date
    total_amount: float

class SearchResult(BaseModel):
    results: List[ExpenseResponse]
    count: int

class ExpenseFilter(BaseModel):
    category: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ExportSummary(BaseModel):
    format: str = Field(..., example="csv")
    filters: Optional[ExpenseFilter] = None

class CategoryStat(BaseModel):
    category: str
    count: int
    average_amount: float

"""
Expense API routes.
Defines endpoints for managing expenses.
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import date
from ..schemas.expense_schema import ExpenseCreate, ExpenseResponse
from ...app.services.expense_service import ExpenseService

router = APIRouter()
service = ExpenseService()

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate):
    try:
        return service.create_expense(expense)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ExpenseResponse])
def get_all_expenses():
    try:
        return service.get_all_expenses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    try:
        return service.get_expense_by_id(expense_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    try:
        service.delete_expense(expense_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseCreate):
    try:
        return service.update_expense(expense_id, expense)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/filter/by-category/", response_model=List[ExpenseResponse])
def filter_expenses_by_category(category: str):
    try:
        return service.get_expenses_by_category(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter/by-date/", response_model=List[ExpenseResponse])
def filter_expenses_by_date_range(start_date: date = Query(...), end_date: date = Query(...)):
    try:
        return service.get_expenses_by_date_range(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary/monthly/", response_model=dict)
def get_monthly_summary(year: int, month: int):
    try:
        return service.get_monthly_summary(year, month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary/by-category/", response_model=dict)
def get_summary_by_category():
    try:
        return service.get_expense_summary_by_category()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/top-categories/", response_model=List[dict])
def get_top_expense_categories(limit: int = 5):
    try:
        return service.get_top_expense_categories(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/total/", response_model=dict)
def get_total_expense():
    try:
        return service.get_total_expense()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/", response_model=List[ExpenseResponse])
def search_expenses(keyword: str):
    try:
        return service.search_expenses(keyword)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/daily-average/", response_model=dict)
def get_daily_average(start_date: Optional[date] = None, end_date: Optional[date] = None):
    try:
        return service.get_daily_average(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/peak-day/", response_model=dict)
def get_peak_expense_day():
    try:
        return service.get_peak_expense_day()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

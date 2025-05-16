"""
Helper utilities for the Expense Management System.
Includes common functions like date parsing, currency formatting, input validation, time utilities, and more.
"""

from datetime import datetime, timedelta, date
import locale
import logging
import re
import uuid
import random
import calendar

# تنظیم فرمت محلی برای نمایش اعداد و تاریخ‌ها (در صورت نیاز)
locale.setlocale(locale.LC_ALL, '')

def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> datetime:
    """تبدیل رشته تاریخ به شیء datetime."""
    try:
        return datetime.strptime(date_str, fmt)
    except ValueError as e:
        logging.error(f"Invalid date format: {e}")
        raise

def format_currency(amount: float, symbol: str = "$", sep: str = ",") -> str:
    """فرمت‌دهی مبلغ با جداکننده و نماد پولی."""
    return f"{symbol}{amount:,.2f}".replace(",", sep)

def is_valid_email(email: str) -> bool:
    """بررسی اعتبار ایمیل با استفاده از قواعد ساده."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def log_exception(message: str, exception: Exception):
    """ثبت خطا با پیام سفارشی."""
    logging.error(f"{message}: {str(exception)}")

def get_current_timestamp() -> str:
    """دریافت timestamp فعلی به‌صورت رشته."""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def generate_transaction_id(prefix: str = "TX") -> str:
    """تولید یک شناسه یکتا برای تراکنش‌ها."""
    return f"{prefix}-{uuid.uuid4()}"

def get_random_color() -> str:
    """تولید رنگ تصادفی در قالب hex برای نمایش گرافیکی."""
    return "#%06x" % random.randint(0, 0xFFFFFF)

def calculate_days_between(start: str, end: str, fmt: str = "%Y-%m-%d") -> int:
    """محاسبه تعداد روز بین دو تاریخ."""
    try:
        start_date = parse_date(start, fmt)
        end_date = parse_date(end, fmt)
        return (end_date - start_date).days
    except Exception as e:
        log_exception("Failed to calculate days between", e)
        raise

def normalize_text(text: str) -> str:
    """نرمال‌سازی رشته‌ها برای ذخیره‌سازی یا مقایسه (حذف فاصله‌ها، حروف کوچک)."""
    return re.sub(r"\s+", " ", text.strip()).lower()

def get_first_day_of_month(target_date: date = date.today()) -> date:
    """دریافت اولین روز ماه از یک تاریخ مشخص."""
    return target_date.replace(day=1)

def get_last_day_of_month(target_date: date = date.today()) -> date:
    """دریافت آخرین روز ماه از یک تاریخ مشخص."""
    last_day = calendar.monthrange(target_date.year, target_date.month)[1]
    return target_date.replace(day=last_day)

def get_week_range(target_date: date = date.today()) -> tuple:
    """دریافت بازه زمانی یک هفته (از دوشنبه تا یکشنبه) برای یک تاریخ."""
    start = target_date - timedelta(days=target_date.weekday())
    end = start + timedelta(days=6)
    return start, end

def is_weekend(target_date: date) -> bool:
    """بررسی اینکه آیا تاریخ داده شده آخر هفته است یا خیر."""
    return target_date.weekday() >= 5

def format_percentage(value: float, precision: int = 2) -> str:
    """فرمت‌دهی عدد به صورت درصد."""
    return f"{value * 100:.{precision}f}%"

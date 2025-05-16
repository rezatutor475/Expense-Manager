"""
Database connection and session management using MySQL Connector and SQLAlchemy.
Includes utility functions for database initialization, teardown, and session handling.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import os
import logging

# تنظیمات اتصال پایگاه‌داده از محیط
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "expense_db")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ساخت Engine و Session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# پایه مدل‌ها
Base = declarative_base()

def init_db():
    """ایجاد جداول در پایگاه‌داده در صورت عدم وجود."""
    import app.models.expense  # بارگذاری مدل‌ها
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database initialized successfully.")
    except SQLAlchemyError as e:
        logging.error(f"Database initialization failed: {e}")


def drop_db():
    """حذف تمام جداول پایگاه‌داده (با احتیاط استفاده شود)."""
    import app.models.expense
    try:
        Base.metadata.drop_all(bind=engine)
        logging.warning("Database dropped successfully.")
    except SQLAlchemyError as e:
        logging.error(f"Database drop failed: {e}")


def get_db():
    """دریافت یک سشن از پایگاه‌داده برای استفاده در توابع.
    استفاده همراه با dependency injection یا context manager توصیه می‌شود.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# استفاده نمونه:
# from app.database.db import get_db
# for db in get_db():
#     result = db.query(...)

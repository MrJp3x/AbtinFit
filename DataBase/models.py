import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 📌 مسیر دیتابیس (مطلق)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}"

# 📌 اتصال به دیتابیس
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    """مدل کاربر با فیلدهای رمزنگاری‌شده"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(String, nullable=False)  # سن به‌شکل متن رمزنگاری‌شده ذخیره می‌شود
    gender = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)

# 📌 ایجاد جداول در دیتابیس
Base.metadata.create_all(engine)

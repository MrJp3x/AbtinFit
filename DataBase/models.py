from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

# تعریف بیس مدل برای استفاده در تمام جداول
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # شناسه‌ی یکتا
    first_name = Column(String, nullable=False)  # نام
    last_name = Column(String, nullable=False)  # نام خانوادگی
    age = Column(Integer, nullable=False)  # سن
    gender = Column(String, nullable=False)  # جنسیت (مثلاً 'مرد' یا 'زن')
    birth_date = Column(Date, nullable=False)  # تاریخ تولد

# ایجاد ارتباط با دیتابیس SQLite
engine = create_engine("sqlite:///database.db", echo=True)

# ایجاد جداول در دیتابیس
Base.metadata.create_all(engine)

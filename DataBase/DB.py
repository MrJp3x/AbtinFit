from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base

# تنظیمات دیتابیس
Base = declarative_base()
engine = create_engine("sqlite:///users.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# مدل User
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)  # نوع صحیح

Base.metadata.create_all(engine)

class UserManager:
    @staticmethod
    def add_user(first_name: str, last_name: str, age: int, gender: str, birth_date: str):
        """افزودن کاربر جدید"""
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()  # تبدیل تاریخ
        user = User(first_name=first_name, last_name=last_name, age=age, gender=gender, birth_date=birth_date_obj)
        session.add(user)
        session.commit()
        print(f"✅ کاربر {first_name} {last_name} با موفقیت اضافه شد.")

    @staticmethod
    def update_user(user_id: int, data: dict):
        """به‌روزرسانی اطلاعات کاربر"""
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            for key, value in data.items():
                if key == "birth_date" and isinstance(value, str):  # تبدیل تاریخ در صورت نیاز
                    value = datetime.strptime(value, "%Y-%m-%d").date()
                setattr(user, key, value)
            session.commit()
            print(f"🔄 اطلاعات کاربر {user.first_name} {user.last_name} به‌روزرسانی شد.")
        else:
            print(f"❌ کاربری با ID {user_id} یافت نشد.")

    @staticmethod
    def delete_user(user_id: int):
        """حذف کاربر"""
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"🗑️ کاربر {user.first_name} {user.last_name} حذف شد.")
        else:
            print(f"❌ کاربری با ID {user_id} یافت نشد.")

    @staticmethod
    def get_users():
        """دریافت لیست کاربران"""
        users = session.query(User).all()
        for user in users:
            print(f"{user.id}: {user.first_name} {user.last_name}, {user.age} ساله، {user.gender}, تاریخ تولد: {user.birth_date}")

# تست عملیات CRUD
if __name__ == "__main__":
    UserManager.add_user("علی", "احمدی", 25, "مرد", "1999-05-21")
    UserManager.get_users()

    UserManager.update_user(1, {"age": 26, "last_name": "رضایی", "birth_date": "1998-04-15"})
    UserManager.get_users()

    UserManager.delete_user(1)
    UserManager.get_users()

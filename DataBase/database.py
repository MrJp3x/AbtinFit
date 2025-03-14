from sqlalchemy.orm import sessionmaker
from .models import engine, User
from .crypto_manager import CryptoManager

class DatabaseManager:
    """مدیریت دیتابیس با SQLAlchemy و رمزنگاری داده‌ها"""

    def __init__(self):
        self.crypto = CryptoManager()
        self.SessionLocal = sessionmaker(bind=engine)

    def add_user(self, first_name: str, last_name: str, age: int, gender: str, birth_date: str):
        """افزودن کاربر جدید به دیتابیس (رمزنگاری‌شده)"""
        encrypted_user = User(
            first_name=self.crypto.encrypt(first_name),
            last_name=self.crypto.encrypt(last_name),
            age=self.crypto.encrypt(str(age)),  # عدد را به متن تبدیل می‌کنیم
            gender=self.crypto.encrypt(gender),
            birth_date=self.crypto.encrypt(birth_date)
        )
        with self.SessionLocal() as session:
            session.add(encrypted_user)
            session.commit()
        print(f"✅ کاربر {first_name} {last_name} ذخیره شد.")

    def get_users(self):
        """دریافت لیست کاربران (رمزگشایی‌شده)"""
        with self.SessionLocal() as session:
            users = session.query(User).all()

        return [
            {
                "id": user.id,
                "first_name": self.crypto.decrypt(user.first_name),
                "last_name": self.crypto.decrypt(user.last_name),
                "age": int(self.crypto.decrypt(user.age)),
                "gender": self.crypto.decrypt(user.gender),
                "birth_date": self.crypto.decrypt(user.birth_date)
            }
            for user in users
        ]

    def delete_user(self, user_id: int):
        """حذف کاربر از دیتابیس"""
        with self.SessionLocal() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                print(f"🗑️ کاربر با ID {user_id} حذف شد.")
            else:
                print(f"❌ کاربری با ID {user_id} یافت نشد.")

    def update_user(self, user_id: int, **kwargs):
        """بروزرسانی اطلاعات کاربر"""
        with self.SessionLocal() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                print(f"❌ کاربری با ID {user_id} یافت نشد.")
                return

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, self.crypto.encrypt(str(value)))

            session.commit()
            print(f"✏️ اطلاعات کاربر {user_id} بروزرسانی شد.")

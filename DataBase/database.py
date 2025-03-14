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
        session = self.SessionLocal()
        encrypted_user = User(
            first_name=self.crypto.encrypt(first_name),
            last_name=self.crypto.encrypt(last_name),
            age=self.crypto.encrypt(str(age)),  # عدد را به متن تبدیل می‌کنیم
            gender=self.crypto.encrypt(gender),
            birth_date=self.crypto.encrypt(birth_date)
        )
        session.add(encrypted_user)
        session.commit()
        session.close()
        print(f"✅ کاربر {first_name} {last_name} ذخیره شد.")

    def get_users(self):
        """دریافت لیست کاربران (رمزگشایی‌شده)"""
        session = self.SessionLocal()
        users = session.query(User).all()
        session.close()

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
        session = self.SessionLocal()
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"🗑️ کاربر با ID {user_id} حذف شد.")
        else:
            print(f"❌ کاربری با ID {user_id} یافت نشد.")
        session.close()

# --- تست CRUD ---
if __name__ == "__main__":
    db = DatabaseManager()
    db.add_user("علی", "احمدی", 25, "مرد", "1999-05-21")

    users = db.get_users()
    print("\n✅ لیست کاربران:")
    for user in users:
        print(user)

    db.delete_user(1)

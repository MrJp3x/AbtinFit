from sqlalchemy.orm import sessionmaker
from .models import engine, User
from .crypto_manager import CryptoManager

class DatabaseManager:
    def __init__(self):
        self.crypto = CryptoManager()
        self.SessionLocal = sessionmaker(bind=engine)

    def add_user(self, first_name: str, last_name: str, phone: str, age: int, gender: str, birth_date: str):
        try:
            encrypted_user = User(
                first_name=self.crypto.encrypt(first_name),
                last_name=self.crypto.encrypt(last_name),
                phone=self.crypto.encrypt(phone),
                age=self.crypto.encrypt(str(age)),
                gender=self.crypto.encrypt(gender),
                birth_date=self.crypto.encrypt(birth_date)
            )
            with self.SessionLocal() as session:
                session.add(encrypted_user)
                session.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {str(e)}")
            return False

    def get_users(self):
        with self.SessionLocal() as session:
            users = session.query(User).all()

        return [
            {
                "id": user.id,
                "first_name": self.crypto.decrypt(user.first_name),
                "last_name": self.crypto.decrypt(user.last_name),
                "phone": self.crypto.decrypt(user.phone),
                "age": int(self.crypto.decrypt(user.age)),
                "gender": self.crypto.decrypt(user.gender),
                "birth_date": self.crypto.decrypt(user.birth_date)
            }
            for user in users
        ]

    def delete_user(self, user_id: int):
        with self.SessionLocal() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()

    def update_user(self, user_id: int, **kwargs):
        with self.SessionLocal() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, self.crypto.encrypt(str(value)))
            session.commit()
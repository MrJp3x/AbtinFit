from cryptography.fernet import Fernet
import os

class CryptoManager:
    """Handles encryption and decryption of data"""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Database directory path
    KEY_PATH = os.path.join(BASE_DIR, "key.key")  # Encryption key file path

    def __init__(self):
        """Initialize encryption key and cipher"""
        self._key = self._load_or_generate_key()
        self._cipher = Fernet(self._key)

    def _load_or_generate_key(self):
        """Load encryption key from file, or generate and save it if not exists"""
        if not os.path.exists(self.KEY_PATH):
            key = Fernet.generate_key()
            with open(self.KEY_PATH, "wb") as key_file:
                key_file.write(key)
        else:
            with open(self.KEY_PATH, "rb") as key_file:
                key = key_file.read()
        return key

    def encrypt(self, data: str) -> str:
        """Encrypt data and return as a string"""
        return self._cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt encrypted data and return as a string"""
        return self._cipher.decrypt(encrypted_data.encode()).decode()

    def safe_decrypt(self, value: str) -> str:
        """Safely decrypt data, return 'Unknown' if value is None"""
        return self.decrypt(value) if value else "Unknown"

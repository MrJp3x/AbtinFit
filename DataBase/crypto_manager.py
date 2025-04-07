from cryptography.fernet import Fernet
import os
import base64


class CryptoManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    KEY_PATH = os.path.join(BASE_DIR, "key.key")
    API_KEY_PATH = os.path.join(BASE_DIR, "api_key.enc")

    def __init__(self):
        self._key = self._load_or_generate_key()
        self._cipher = Fernet(self._key)

    def _load_or_generate_key(self):
        if not os.path.exists(self.KEY_PATH):
            key = Fernet.generate_key()
            with open(self.KEY_PATH, "wb") as key_file:
                key_file.write(key)
        else:
            with open(self.KEY_PATH, "rb") as key_file:
                key = key_file.read()
        return key

    def encrypt(self, data: str) -> str:
        """Encrypts data with proper padding"""
        # Ensure data is bytes and properly padded
        data_bytes = data.encode()
        return self._cipher.encrypt(data_bytes).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypts data with padding validation"""
        try:
            # Add padding if necessary
            pad_len = len(encrypted_data) % 4
            if pad_len:
                encrypted_data += "=" * (4 - pad_len)
            return self._cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def safe_decrypt(self, value: str) -> str:
        return self.decrypt(value) if value else "Unknown"

    def initialize_api_key(self, api_key: str):
        """Store encrypted API key"""
        encrypted = self.encrypt(api_key)
        with open(self.API_KEY_PATH, "w") as f:
            f.write(encrypted)

    def get_api_key(self) -> str:
        """Retrieve decrypted API key"""
        if not os.path.exists(self.API_KEY_PATH):
            raise FileNotFoundError("API key not initialized")

        with open(self.API_KEY_PATH, "r") as f:
            encrypted = f.read().strip()
        return self.decrypt(encrypted)
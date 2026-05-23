from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY

cipher = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    if not data:
        return None
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    if not encrypted_data:
        return None
    try:
        return cipher.decrypt(encrypted_data.encode()).decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

def hash_password(password):
    return generate_password_hash(password)

def validate_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)

def encrypt_text(text):
    cipher_suite = Fernet(current_app.config.get("FERNET_KEY"))
    encrypted_email = cipher_suite.encrypt(text.encode())
    return encrypted_email.decode()

def decrypt_text(encrypted_text):
    cipher_suite = Fernet(current_app.config.get("FERNET_KEY"))
    decrypted_email = cipher_suite.decrypt(encrypted_text.encode())
    return decrypted_email.decode()

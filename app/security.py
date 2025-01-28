from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import jwt
from datetime import datetime

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

def generate_token(data):
    try:
        payload = {
            "data": data,
            "iat": datetime.now(),
            "exp": 9999999999999
        }

        token_key = current_app.config.get("TOKEN_KEY")
        return jwt.encode(payload, token_key, algorithm="HS256")

    except Exception as e:
        raise Exception(f"Erro ao gerar o token JWT: {e}")

def decode_jwt(token):
    try:
        token_key = current_app.config.get("TOKEN_KEY")
        payload = jwt.decode(token, token_key, algorithms=["HS256"])
        return payload.get('data')
    except Exception as e:
        raise e
    except jwt.InvalidSignatureError:
        raise Exception("Token inválido. Faça login novamente.")
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado. Faça login novamente.")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido. Faça login novamente.")

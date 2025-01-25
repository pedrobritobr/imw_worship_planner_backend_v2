from functools import wraps
from flask import request, jsonify, current_app
import re

def phrase_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_keyword = request.headers.get('keyword')
        PLANNER_PHRASE = current_app.config.get("PLANNER_PHRASE")
        if not user_keyword or user_keyword != PLANNER_PHRASE:
            return jsonify({"message": "Unauthorized"}), 401

        return func(*args, **kwargs)
    return wrapper

def is_valid_email(email):
    email_regex = r"^((?!\.)[\w\-_.]*[\d\w\-_.]{2,})(@\w{2,})(\.\w+(\.\w+)?[^.\W])$"
    return re.match(email_regex, email)

def is_valid_password(password):
    return len(password) >= 8
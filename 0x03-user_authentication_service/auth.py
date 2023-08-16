#!/usr/bin/env python3
"""Auth module
"""
from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Method hashes the password
    """
    pass_hash = hashpw(password=password.encode('utf-8'), salt=gensalt())
    return pass_hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user
        """
        try:
            user_check = self._db.find_user_by(email=email)
        except NoResultFound:
            hash_pass = _hash_password(password)
            user_obj = self._db.add_user(email, hash_pass)
            return user_obj
        raise ValueError(f"User {user_check.email} already exists")

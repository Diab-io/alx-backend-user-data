#!/usr/bin/env python3
"""Auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Method hashes the password
    """
    pass_hash = hashpw(password=password.encode('utf-8'), salt=gensalt())
    return pass_hash


def _generate_uuid() -> str:
    """Generates a uuid string
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validats the user
        """
        try:
            user_check = self._db.find_user_by(email=email)
            is_valid = checkpw(password.encode('utf-8'),
                               user_check.hashed_password)
            return is_valid
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        """
        try:
            session_id = _generate_uuid()
            user_check = self._db.find_user_by(email=email)
            user_check.session_id = session_id
            self._db._session.commit()

            return session_id
        except Exception:
            return

#!/usr/bin/env python3
"""Auth module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
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
        """Validates the user
        """
        try:
            user_check = self._db.find_user_by(email=email)
            is_valid = checkpw(password.encode('utf-8'),
                               user_check.hashed_password)
            return is_valid
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session for the user
        """
        try:
            session_id = _generate_uuid()
            user_check = self._db.find_user_by(email=email)
            self._db.update_user(user_check.id, session_id=session_id)
            return session_id
        except Exception:
            return

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Gets a user from the provided session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session of the specified user
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Method used for updating the users password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        new_hash_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=new_hash_password)
        self._db.update_user(user.id, reset_token=None)

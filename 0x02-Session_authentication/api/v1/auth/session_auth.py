#!/usr/bin/env python3
"""
session auth module
"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    Handles the session auth mechanisms
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a session id and stores it
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a user id based on the session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
         returns a User instance based on a cookie value
        """
        cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(cookie)
        user = User()
        return user.get(user_id)

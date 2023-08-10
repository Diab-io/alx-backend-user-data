#!/usr/bin/env python3
"""
session auth module
"""
from .auth import Auth
import uuid


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

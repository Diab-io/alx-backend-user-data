#!/usr/bin/env python3
""" Module for authentication
"""
from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """ Class that manages the Api authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a view requires authentication
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if path and path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                base_path = re.escape(excluded_path[:-1])
                if re.match(f"{base_path}.*", path):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method that returns the val of the authorization header
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that gets current user if authenticated
        """
        return None

    def session_cookie(self, request=None):
        """ Method that returns a cookie value from the request
        """
        if request is None:
            return None
        session_name = os.environ.get('SESSION_NAME')
        return request.cookies.get(session_name)

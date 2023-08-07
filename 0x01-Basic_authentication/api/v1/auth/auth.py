#!/usr/bin/env python3
""" Module for authentication
"""
from flask import request
from typing import List, TypeVar


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
        if path in excluded_paths:
            return False
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Method that handles processes in the authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that gets current user if authenticated
        """
        return None

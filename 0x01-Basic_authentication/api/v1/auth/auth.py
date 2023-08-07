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
        return False

    def authorization_header(self, request=None) -> str:
        """ Method that handles processes in the authorization header
        """
        return None
    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that gets current user if authenticated
        """
        return None

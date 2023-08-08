#!/usr/bin/env python3
"""
Basic Authentication module
"""
from .auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Contains all methods for Basic authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Method used to extract the value of the authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        auth_header_content = authorization_header.split(' ')[-1]
        return auth_header_content

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            msg = base64.b64decode(base64_authorization_header, validate=True)
            return msg.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Method used to get the credentials of the user
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if not decoded_base64_authorization_header.__contains__(':'):
            return (None, None)
        name, email = decoded_base64_authorization_header.split(':')
        return (name, email)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a user based on the user's credential
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if len(users) < 1:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]

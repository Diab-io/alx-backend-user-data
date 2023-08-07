#!/usr/bin/env python3
"""
Basic Authentication module
"""
from .auth import Auth
import base64


class BasicAuth(Auth):
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

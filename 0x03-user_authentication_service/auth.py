#!/usr/bin/env python3
"""Auth module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """Method hashes the password
    """
    pass_hash = hashpw(password=password.encode('utf-8'), salt=gensalt())
    return pass_hash

#!/usr/bin/env python3
"""
encrypt_password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    This function is used for hasing passwords
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    checks if the hashed password and password
    are the same
    """
    if bcrypt.checkpw(password.encode('utf8'), hashed_password):
        return True
    return False

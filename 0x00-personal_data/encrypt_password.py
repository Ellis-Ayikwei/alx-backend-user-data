#!/usr/bin/env python3
"""Defines a function the retunr an obfuscated msg"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Returns True if the password is valid."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

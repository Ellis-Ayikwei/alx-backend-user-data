#!/usr/bin/env python3
"""Auth module"""

import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound

from db import DB
import uuid


def _hash_password(password: str) -> bytes:
    """Hash a password for storing."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

        from sqlalchemy.orm.exc import NoResultFound

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email (str): The email address of the user to register.
            password (str): The password for the user to register.

        Returns:
            User: The newly registered user.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        new_user = self._db.add_user(email, _hash_password(password))

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user's login credentials."""
        try:
            user_by_email = self._db.find_user_by(email=email)
            if user_by_email is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"), user_by_email.hashed_password
                )
            else:
                return False
        except Exception:
            return False

    def _generate_uuid() -> str:
        """Return a string of the UUID"""
        return str(uuid.uuid4())

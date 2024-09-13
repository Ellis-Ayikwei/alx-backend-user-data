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


def _generate_uuid() -> str:
    """Return a string of the UUID"""
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """Create a new session for a user."""
        try:
            user_by_email = self._db.find_user_by(email=email)
            if user_by_email is not None:
                session_id = _generate_uuid()
                self._db.update_user(user_by_email.id, session_id=session_id)
                return session_id
        except Exception:
            return None

    @staticmethod
    def _generate_uuid() -> str:
        """Return a string of the UUID"""
        return str(uuid.uuid4())

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get a user from a session ID."""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session for a user."""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """retuns a token"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = str(uuid.uuid4())
                self._db.update_user(user.id, reset_token=reset_token)
            raise ValueError
        except NoResultFound:
            raise ValueError

#!/usr/bin/env python3
"""This module contains the BasicAauth class.
The BasicAauth class handles Basic Auth for the AirBnB clone.
It provides the following methods:
- extract_base64_authorization_header: Returns the
Base64 part of the Authorization
    header for a BasicAuth
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth that inherits from Auth.
    For the moment this class will be empty.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization
        header for a BasicAuth
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Returns the decoded value of a Base64
        string
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            return base64.standard_b64decode(base64_authorization_header).decode(
                "utf-8"
            )
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the user email and password from the decoded Base64
        string
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        user_email = decoded_base64_authorization_header.split(":")[0]
        user_name = decoded_base64_authorization_header.split(":")[1]
        return user_email, user_name

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """
        Returns the User object based on the email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if len(users) == 0:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

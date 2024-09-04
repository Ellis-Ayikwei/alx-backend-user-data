#!/usr/bin/env python3
"""This module contains the BasicAauth class.
The BasicAauth class handles Basic Auth for the AirBnB clone.
It provides the following methods:
- extract_base64_authorization_header: Returns the
Base64 part of the Authorization
    header for a BasicAuth
"""
import re
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth that inherits from Auth.
    For the moment this class will be empty.
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
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
            return base64.standard_b64decode(
                base64_authorization_header).decode(
                "utf-8"
            )
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str):
        """
        Extracts user credentials from the Base64 decoded authorization header.
        Allows passwords to contain ':'.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split at the first occurrence of ':'
        user_email, user_pwd = decoded_base64_authorization_header.split(':', 1)
        return user_email, user_pwd

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """Extracts user credentials from a base64-decoded authorization
        header that uses the Basic authentication flow.
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Retrieves the current user
        """
        auth_header = self.authorization_header(request)
        base64_auth = self.extract_base64_authorization_header(auth_header)
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        user_credentials = self.extract_user_credentials(decoded_auth)
        return self.user_object_from_credentials(*user_credentials)

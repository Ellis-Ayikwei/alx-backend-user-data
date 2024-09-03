#!/usr/bin/env python3
"""
This module contains the Auth class.
The Auth class handles authentication for the AirBnB clone.
It provides the following methods:
- require_auth: Returns True if the path requires
authentication, False otherwise.
"""
from flask import request
from typing import List,TypeVar
import flask


class Auth:
    """
    Auth class handles authentication for the AirBnB clone.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if the path requires authentication, False otherwise.
        """
        if path is None or not excluded_paths:
            return True

        normalized_path = path.rstrip("/")
        normalized_excluded_paths = [p.rstrip("/") for p in excluded_paths]
        print("normalized_excluded_paths")
        return normalized_path not in normalized_excluded_paths

    def authorization_header(self, request: flask.Request = None) -> str:
        """
        Retrieves the value of the Authorization header from the request.

        Args:
            request (flask.Request): The request object.

        Returns:
            str: The value of the Authorization header, or None if the header
                is not found.
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user.
        """
        return None

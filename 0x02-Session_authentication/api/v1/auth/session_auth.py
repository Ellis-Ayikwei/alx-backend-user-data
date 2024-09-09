#!/usr/bin/env python3
"""Define a module for the session auth class"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User

from flask import Flask, jsonify, request
from api.v1.views import app_views


class SessionAuth(Auth):
    """The Session Auth class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for the user id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """that returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """that returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)


    @app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
    def session_login():
        """Handles the login route"""
        from api.v1.app import auth

        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return jsonify({"error": "email missing"}), 400
        if not password:
            return jsonify({"error": "password missing"}), 400

        user = User.search({'email': email})
        if not user:
            return jsonify({"error": "no user found for this email"}), 404

        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(auth.session_name, session_id)

        return response

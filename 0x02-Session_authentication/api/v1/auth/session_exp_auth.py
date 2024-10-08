#!/usr/bin/env python3
"""Module of SessionExpAuth class"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Define the class for the session exp auth"""
    def __init__(self):
        self.session_duration = int(os.getenv('SESSION_DURATION')) \
            if os.getenv('SESSION_DURATION') else 0

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for the user id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
       
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def get_user_id_from_session_id(self, session_id: str) -> str:
        """
        Returns the user ID associated with a given session ID.
        """
        if session_id is None:
            return None

        session_info = self.user_id_by_session_id.get(session_id)

        if session_info is None:
            return None

        if self.session_duration <= 0:
            return session_info["user_id"]

        if "created_at" not in session_info:
            return None

        created_at = session_info["created_at"]
        session_expiration = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > session_expiration:
            return None

        return session_info["user_id"]

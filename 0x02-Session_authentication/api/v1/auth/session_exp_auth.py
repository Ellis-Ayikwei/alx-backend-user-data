from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta

sa = SessionAuth()


class SessionExpAuth(sa):
    def __init__(self):
        self.session_duration = int(os.getenv('SESSION_DURATION')) \
            if os.getenv('SESSION_DURATION') else 0
        self.session_cookie_duration = self.session_duration

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for the user id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        expiration_date = datetime.now()\
            + timedelta(seconds=self.session_duration)
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def get_user_id_from_session_id(self, session_id: str) -> str:
        """
        Returns the user ID associated with a given session ID.
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        session_info = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_info["user_id"]

        if "created_at" not in session_info:
            return None
        if int(session_info["created_at"])\
                + self.session_duration < datetime.now():
            return None

        return session_info["user_id"]

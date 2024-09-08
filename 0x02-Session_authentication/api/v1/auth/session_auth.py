#!/usr/bin/env python3
"""Define a module for the session auth class"""

from api.v1.auth.auth import Auth
import uuid

class SessionAuth(Auth):
    """The Session Auth class"""
    user_id_by_session_id = {}
    
    
    def create_session(self, user_id: str = None) -> str:
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4)
        user_id_by_session_id['user_id'] = user_id
    pass

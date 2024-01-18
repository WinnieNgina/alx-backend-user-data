#!/usr/bin/env python3
"""Module creates a new authentication mechanism"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session for a user"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Return a User instance based on a cookie value """
        if request is None:
            return None

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None

        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Implement log out method"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        else:
            del self.user_id_by_session_id[session_id]
            return True

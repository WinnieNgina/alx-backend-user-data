#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header"""
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None

        # Check if the header starts with 'Basic ' (with a space at the end)
        if not authorization_header.startswith('Basic '):
            return None

        # Extract and return the Base64 part after 'Basic '
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the Base64 part of authorization header"""
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Encode user credentials"""
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns user object"""
        if (user_email is None or not isinstance(user_email, str)):
            return None
        if (user_pwd is None or not isinstance(user_pwd, str)):
            return None
        users = User.search({'email': user_email})
        if not users:
            """No user found with the given email"""
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        # No valid user password is found
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request."""
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_value = self.decode_base64_authorization_header(base64_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_value)
        user_instance = self.user_object_from_credentials(user_email, user_pwd)
        return user_instance

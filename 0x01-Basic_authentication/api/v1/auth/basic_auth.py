#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth
import base64


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

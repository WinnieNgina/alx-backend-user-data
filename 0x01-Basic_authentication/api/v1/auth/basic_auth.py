#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth


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

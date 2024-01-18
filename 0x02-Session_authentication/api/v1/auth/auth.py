#!/usr/bin/env python3
"""This module defines class Auth"""
from typing import List, TypeVar
from flask import request
import fnmatch
import os


class Auth:
    """Class responsible for handling Authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for the given path.
        :path: The requested path.
        :excluded_paths: List of paths that are excluded from authentication.
        :return: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        normalized_path = path.rstrip('/') + '/'
        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(normalized_path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets the authorization header from the Flask request object.
        :param request: Flask request object.
        :return: Authorization header value.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user from the Flask request object.
        :param request: Flask request object.
        :return: Current user.
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = os.environ.get("SESSION_NAME")
        return request.cookies.get(session_name)

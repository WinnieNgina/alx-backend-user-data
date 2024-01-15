#!/usr/bin/env python3
"""This module defines class Auth"""
from typing import List, TypeVar
from flask import request


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
            if normalized_path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets the authorization header from the Flask request object.
        :param request: Flask request object.
        :return: Authorization header value.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user from the Flask request object.
        :param request: Flask request object.
        :return: Current user.
        """
        return None

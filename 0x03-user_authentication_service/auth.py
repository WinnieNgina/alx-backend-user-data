#!/usr/bin/env python3
"""Hash password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Password hashing function"""
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed

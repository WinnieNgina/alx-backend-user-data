#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Password hashing function"""
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password"""
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)

#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password):
    """Password hashing function"""
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password

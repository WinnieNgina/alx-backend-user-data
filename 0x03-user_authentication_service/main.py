#!/usr/bin/env python3
"""Integration tests"""
import requests


BASE_URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """
    Register a user with the given email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    response = requests.post(f'{BASE_URL}/users',
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    print("User registered successfully.")


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Logs in with a wrong password and
    verifies that the response status code is 401.
    Args:
        email (str): The email for logging in.
        password (str): The wrong password for logging in.
    Returns:
        None
    """
    response = requests.post(f'{BASE_URL}/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 401
    print("Login with wrong password failed as expected.")


def log_in(email: str, password: str) -> str:
    """
    Logs in with the given email and password
    and returns the session ID cookie.
    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID cookie.
    """
    response = requests.post(f'{BASE_URL}/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    print("Login successful.")
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """
    Function to perform an unlogged user profile access
    and verify the expected failure.
    No parameters are taken, and the function returns None.
    """
    response = requests.get(f'{BASE_URL}/profile')
    assert response.status_code == 403
    print("Profile access without login failed as expected.")


def profile_logged(session_id: str) -> None:
    """
    Function to log the profile access after a successful login.

    Args:
        session_id (str): The session ID for the user.

    Returns:
        None
    """
    response = requests.get(f'{BASE_URL}/profile',
                            cookies={'session_id': session_id})
    assert response.status_code == 200
    print("Profile access after login successful.")


def log_out(session_id: str) -> None:
    """
    Logs out the user by deleting the
    session identified by the given session_id.

    Args:
        session_id (str): The unique identifier of the session to be deleted.

    Returns:
        None
    """
    response = requests.delete(f'{BASE_URL}/sessions',
                               cookies={'session_id': session_id})
    assert response.status_code == 200  # Redirect status code
    print("Logout successful.")


def reset_password_token(email: str) -> str:
    """
    Function to reset the password token for a given email.

    Args:
        email (str): The email for which the password reset token is requested.

    Returns:
        str: The reset password token.
    """
    response = requests.post(f'{BASE_URL}/reset_password',
                             data={'email': email})
    assert response.status_code == 200
    reset_token = response.json()['reset_token']
    print("Reset password token obtained.")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update a user's password using the provided email,
    reset token, and new password.

    Args:
        email (str): The user's email address.
        reset_token (str): The token used to reset the user's password.
        new_password (str): The new password to be set for the user.

    Returns:
        None
    """
    response = requests.put(f'{BASE_URL}/reset_password',
                            data={'email': email, 'reset_token': reset_token,
                                  'new_password': new_password})
    assert response.status_code == 200
    print("Password updated successfully.")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

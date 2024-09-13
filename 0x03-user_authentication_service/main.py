#!/usr/bin/env python3
"""Defines the main file."""
import requests


def register_user(email: str, password: str) -> None:
    """
    Register a new user via a POST request to /users

    Args:
        email (str): The email address of the user to register.
        password (str): The password for the user to register.

    Returns:
        None

    Raises:
        AssertionError: If the POST request failed.
    """
    # Create the payload for the POST request
    payload = {"email": email, "password": password}

    # Send the POST request
    r = requests.post("http://127.0.0.1:5000/users", payload)

    # Check that the response was successful
    response_code = r.status_code
    assert response_code == 200

    # Check that the response was as expected
    assert r.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Tests logging in with an incorrect password.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        None

    Raises:
        AssertionError: If the POST request failed.
    """
    # Create the payload for the POST request
    payload = {"email": email, "password": password}

    # Send the POST request
    r = requests.post("http://127.0.0.1:5000/sessions", payload)

    # Check that the response was unsuccessful
    response_code = r.status_code
    assert response_code == 401


def profile_unlogged() -> None:
    """
    Tests accessing the profile without logging in first.

    The expected response is a 403 status code.

    Returns:
        None

    Raises:
        AssertionError: If the GET request failed.
    """
    # Perform a GET request to the profile route
    r = requests.get("http://127.0.0.1:5000/profile")

    # Check that the response was a 403
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Tests accessing the profile after logging in.

    The expected response is a 200 status code and a JSON object with the
    user's email address.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        None

    Raises:
        AssertionError: If the GET request failed.
    """
    # Perform a GET request to the profile route with the session ID
    payload = {"session_id": session_id}
    r = requests.get("http://127.0.0.1:5000/profile", params=payload)

    # Check that the response was successful
    assert r.status_code == 200

    # Check that the response was as expected
    assert r.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """
    Tests logging out a user.

    The expected response is a 200 status code.

    Args:
        session_id (str): The session ID of the user.

    Returns:
        None

    Raises:
        AssertionError: If the DELETE request failed.
    """
    # Perform a DELETE request to the sessions route with the session ID
    payload = {"session_id": session_id}
    r = requests.delete("http://127.0.0.1:5000/sessions", data=payload)

    # Check that the response was successful
    assert r.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Get the reset password token.

    The expected response is a 200 status code and a JSON object with the
    reset token.

    Args:
        email (str): The email address of the user.

    Returns:
        str: The reset token.

    Raises:
        AssertionError: If the POST request failed.
    """
    payload = {"email": email}
    r = requests.post("http://127.0.0.1:5000/reset_password", payload)

    # Check that the response was successful
    assert r.status_code == 200

    # Return the reset token
    return r.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the user's password.

    The expected response is a 200 status code and a JSON object with the
    message "Password updated".

    Args:
        email (str): The email address of the user.
        reset_token (str): The user's reset token.
        new_password (str): The user's new password.

    Returns:
        None

    Raises:
        AssertionError: If the PUT request failed.
    """
    payload = {"email": email, "reset_token": reset_token, "new_password": new_password}
    r = requests.put("http://127.0.0.1:5000/reset_password", payload)

    # Check that the response was successful
    assert r.status_code == 200

    # Check that the response was as expected
    assert r.json() == {"email": email, "message": "Password updated"}


def log_in(email: str, password: str) -> str:
    """
    Logs in a user.

    The expected response is a 200 status code and a JSON object with the
    user's email address and a message indicating that the user is logged in.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID of the user.

    Raises:
        AssertionError: If the POST request failed.
    """
    payload = {"email": email, "password": password}
    r = requests.post("http://127.0.0.1:5000/sessions", payload)

    # Check that the response was successful
    assert r.status_code == 200

    # Check that the response was as expected
    assert r.json() == {"email": email, "message": "logged in"}

    # Return the session ID
    return r.cookies.get("session_id")


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

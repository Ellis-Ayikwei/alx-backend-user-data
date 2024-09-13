#!/usr/bin/env python3

import requests

def register_user(email: str, password: str) -> None:
    payload={"email":email, "password":password}
    r = requests.post("http://127.0.0.1:5000/users", payload)
    response_code = r.status_code
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}
    
def log_in_wrong_password(email: str, password: str) -> None:
    payload={"email":email, "password":password}
    r = requests.post("http://127.0.0.1:5000/sessions", payload)
    response_code = r.status_code
    assert response_code == 401

def profile_unlogged() -> None:
    r = requests.get("http://127.0.0.1:5000/profile")
    assert r.status_code == 403
    
def profile_logged(session_id: str) -> None:
    payload = {"session_id": session_id}
    r = requests.get("http://127.0.0.1:5000/profile", payload)
    assert r.status_code == 200
    assert r.json() == {"email": "guillaume@holberton.io"}
    
def log_out(session_id: str) -> None:
    payload = {"session_id":session_id}
    r = requests.delete("http://127.0.0.1:5000/sessions", payload)
    assert r.status == 200

def reset_password_token(email: str) -> str:
    payload = {"email": email}
    r = requests.post("http://127.0.0.1:5000/reset_password", payload)
    assert r.status_code == 200
    return r.json()["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    payload = {"email": email, "reset_token": reset_token,
               "new_password": new_password}
    r = requests.put("http://127.0.0.1:5000/reset_password", payload)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message":
                        "Password updated"}
     
def log_in(email: str, password: str) -> str:
    payload={"email":email, "password":password}
    r = requests.post("http://127.0.0.1:5000/sessions", payload)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
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
    
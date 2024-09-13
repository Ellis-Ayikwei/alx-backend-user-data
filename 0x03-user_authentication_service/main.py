import requests
def register_user(email: str, password: str) -> None:
    payload={"email":email, "password":password}
    r=requests.post("http://127.0.0.1:5000/users", payload)
    response_code = r.status_code
    assert response_code == 200
    assert r == {"email": email, "message": "user created"}
    




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
    
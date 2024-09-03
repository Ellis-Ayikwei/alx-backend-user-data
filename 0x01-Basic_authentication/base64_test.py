#!/usr/bin/env python3
import base64

file = {"username": "Jason", "password": "idontknowjason"}


def basic_auth_str(file: dict) -> bytes:
    cred = f"{file['username']}:{file['password']}".encode("utf-8")
    encoded_cred = base64.urlsafe_b64encode(cred)
    return encoded_cred


the_basic_auth = basic_auth_str(file)


def decodess(the_basic_auth: bytes, file) -> bool:
    if base64.urlsafe_b64decode(
        the_basic_auth
    ) == f"{file['username']}:{file['password']}".encode("utf-8"):
        print("the initial suth ahs been authorised")
        return True


if __name__ == "__main__":
    print(decodess(the_basic_auth, file))

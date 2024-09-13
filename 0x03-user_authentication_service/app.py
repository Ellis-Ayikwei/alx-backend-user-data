#!/usr/bin/env python3
""" Defines A"""
from flask import Flask, jsonify, request, make_response, redirect, url_for
from auth import Auth
from flask import abort
from auth import _generate_uuid

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    email = request.form["email"]
    password = request.form["password"]
    try:
        user = AUTH.register_user(email, password)
        if user:
            return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "user already exists"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """End-point for user login."""

    email = request.form["email"]
    password = request.form["password"]
    if email and password:
        try:
            user = AUTH.valid_login(email, password)
            if user:
                session_id = _generate_uuid()
                AUTH.create_session(session_id)
                response = jsonify({"email": email, "message": "logged in"})
                response.set_cookie("session_id", session_id)
                return response
        except Exception:
            abort(401)
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    try:
        session_id = request.cookies.get("session_id")
        if session_id:
            user = AUTH.get_user_from_session_id(session_id)
            if user:
                AUTH.destroy_session(user.id)
            else:
                return redirect("/")
        abort(403)
    except Exception:
        return abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return:
        - The user's profile information.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})



@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """get the rest password token"""
    email = request.form['email']
    try:
        token = AUTH.get_reset_password_token(email)
        if token:
            return jsonify({"email": "<user email>",
                            "reset_token": "<reset token>"}), 200
    except Exception:
      abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

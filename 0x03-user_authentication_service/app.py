#!/usr/bin/env python3
""" Defines A"""
from flask import Flask, jsonify, request
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
    user = AUTH.register_user(email, password)
    if user:
        return jsonify({"email": email, "message": "user created"})
    return jsonify({"message": "user already exists"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    if not request.form['email'] and not request.form['password']:
        abort(401)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

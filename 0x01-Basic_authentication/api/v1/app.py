#!/usr/bin/env python3
"""
This module sets up the Flask application, including routes,
authentication, and error handling for the API.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, url_for, Response
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views.index import get_forbidden
from typing import Dict, Tuple, Literal

app = Flask(__name__)
app.register_blueprint(app_views)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv("AUTH_TYPE"):
    if getenv("AUTH_TYPE") == "basic_auth":
        auth = BasicAuth()
    else:
        auth = Auth()


@app.before_request
def check_auth() -> None:
    """Check if authentication is required for the current request"""
    if auth is None:
        return

    path = request.path
    excluded_paths = [
        "/api/v1/status/",
        "/api/v1/unauthorized/",
        "/api/v1/forbidden/",
    ]

    if not auth.require_auth(path, excluded_paths):
        return

    auth_header = auth.get_auth_header(request)
    if auth_header is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> Tuple[str, Literal[401]]:
    """Unauthorized handler.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

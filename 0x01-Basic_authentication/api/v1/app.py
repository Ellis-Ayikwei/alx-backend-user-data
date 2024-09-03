#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Route module for the API
"""

import os
import sys

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth import auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views.index import get_forbidden

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

if os.getenv("AUTH_TYPE") == "basic_auth":
    app.before_request(auth.BasicAuth().check_auth)
elif os.getenv("AUTH_TYPE"):
    app.before_request(auth.Auth().check_auth)


@app.errorhandler(404)
def not_found(_error):
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorised(_error):
    """Unauthorised handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(_error):
    """Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    try:
        port = int(port)
    except ValueError:
        print("API_PORT must be an integer", file=sys.stderr)
        sys.exit(1)
    app.run(host=host, port=port)


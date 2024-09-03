#!/usr/bin/env python3
"""Module of Index views
This module defines the index views for the API, including routes for checking
the status, retrieving statistics, and handling unauthorized and
forbidden requests.
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """GET /api/v1/status
    Return:
      - the status of the API as a JSON object.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats/", strict_slashes=False)
def stats():
    """GET /api/v1/stats
    Return:
      - the number of each object type in the system as a JSON object.
    """
    stats = {"users": User.count()}
    return jsonify(stats)


@app_views.route("/unauthorized", strict_slashes=False)
def unauthorized() -> None:
     """GET /api/v1/unauthorized
    Return:
      - Unauthorized error.
    """
    abort(401)


@app_views.route("/forbidden", methods=["GET"], strict_slashes=False)
def get_forbidden():
    """GET /forbidden
    Return:
        - Triggers a 403 Forbidden error.
    """
    abort(403)

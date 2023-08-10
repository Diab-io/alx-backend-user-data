#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.environ.get('AUTH_TYPE')

if auth_type == 'auth':
    auth = Auth()
if auth_type == 'basic_auth':
    auth = BasicAuth()
if auth_type == 'session_auth':
    auth = SessionAuth()


@app.before_request
def authenticate_user():
    """
    This authenticates a user before the
    request is processed
    """
    if auth is None:
        return
    excluded_path = ['/api/v1/status/',
                     '/api/v1/unauthorized/',
                     '/api/v1/forbidden/']
    path = request.path
    requires_auth = auth.require_auth(path, excluded_path)
    print(requires_auth)
    if requires_auth:
        if auth.authorization_header(request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)
        request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized access handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

#!/usr/bin/env python3
""" Module of session auth views
"""
from api.v1.views import app_views
from flask import request, jsonify, session, abort
from models.user import User
import os

SESSION_NAME = os.getenv('SESSION_NAME')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    POST /api/v1/auth_session/login
    This route returns user object in json format
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    valid_password = users[0].is_valid_password(password)
    if not valid_password:
        print(valid_password)
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(getattr(users[0], 'id'))
    user_obj = jsonify(users[0].to_json())
    user_obj.set_cookie(SESSION_NAME, session_id)

    return user_obj


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout():
    """
    DELETE /api/v1/auth_session/login
    This route deletes the session and simulates
    logging out the user
    """
    from api.v1.app import auth

    del_session = auth.destroy_session(request)
    if not del_session:
        abort(404)
    return jsonify({}), 200

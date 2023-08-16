#!/usr/bin/env python3
""" A simple flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index_page():
    """Returns a simple payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Returns a simple payload
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return
    try:
        user_obj = AUTH.register_user(email, password)
        return jsonify({"email": user_obj.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Implementation of login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return
    valid = AUTH.valid_login(email, password)
    if not valid:
        abort(401)
    user_session_id = AUTH.create_session(email)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', user_session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Implements the logout
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    Auth.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

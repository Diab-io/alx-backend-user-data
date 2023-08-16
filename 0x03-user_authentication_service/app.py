#!/usr/bin/env python3
""" A simple flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
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
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)  # Unauthorized
    AUTH.destroy_session(user.id)

    return redirect("/")  # Redirect after successful logout


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Gets the user profile
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password_token():
    """Resets password
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": "<user email>", "reset_token": reset_token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """This route updates the user's password
    """
    email = request.form.get("email")
    password = request.form.get("password")
    reset_token = request.form.get("reset_token")
    is_password_changed = False

    try:
        Auth.update_password(reset_token, password)
        is_password_changed = True
    except ValueError:
        is_password_changed = False
    if not is_password_changed:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

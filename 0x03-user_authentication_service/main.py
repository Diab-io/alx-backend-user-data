#!/usr/bin/env python3
"""
An End-to-end integration test for app.py
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Test registering a user
    """
    url = f"{BASE_URL}/users"
    data = {
        'email': email,
        'password': password,
    }
    resp = requests.post(url=url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "user created"}
    resp = requests.post(url=url, data=data)
    assert resp.status_code == 400
    assert resp.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests logging in with a wrong password
    """
    url = f"{BASE_URL}/sessions"
    data = {
        'email': email,
        'password': password
    }
    resp = requests.post(url=url, data=data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test logging in with the right password
    """
    url = f"{BASE_URL}/sessions"
    data = {
        'email': email,
        'password': password
    }
    resp = requests.post(url=url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    return resp.cookies.get('session_id')


def profile_unlogged():
    """Tests getting a profile info when logged out
    """
    url = f"{BASE_URL}/profile"
    resp = requests.get(url)
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests getting a profile info while logged in
    """
    url = f"{BASE_URL}/profile"
    set_cookies = {
        'session_id': session_id
    }
    resp = requests.get(url, cookies=set_cookies)
    assert resp.status_code == 200
    assert 'email' in resp.json()


def log_out(session_id: str) -> None:
    """Test the logging out
    """
    url = f"{BASE_URL}/sessions"
    cookie = {
        'session_id': session_id
    }
    resp = requests.delete(url=url, cookies=cookie)
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """Tests password reset request
    """
    url = f"{BASE_URL}/reset_password"
    data = {
        'email': email
    }
    resp = requests.post(url=url, data=data)
    assert resp.status_code == 200
    res_json = resp.json()
    assert 'email' in res_json
    assert res_json['email'] == email
    assert 'reset_token' in res_json
    return res_json.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests password updating
    """
    url = f"{BASE_URL}/reset_password"
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    resp = requests.put(url=url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

#!/usr/bin/env python3
"""App module"""
from flask import Flask, jsonify, request, redirect, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def message():
    """Returns message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """End point to register user"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user = AUTH.register_user(email, password)
        response = {"email": user.email, "message": "user created"}
        return jsonify(response), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """login endpoint"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout():
    """implement a logout function"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            abort(403)
    else:
        abort(403)


@app.route("/profile", methods=['GET'])
def profile():
    """Returns user profile"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            return jsonify({"email": user.email}), 200
        else:
            abort(403)
    else:
        abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """Get reset password token"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        response = {"email": email, "reset_token": reset_token}
        return jsonify(response), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """Update password end-point"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        response = {"email": email, "message": "Password updated"}
        return jsonify(response), 200
    except ValueError:
        abort(403)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

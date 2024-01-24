#!/usr/bin/env python3
"""App module"""
from flask import Flask, jsonify, request, abort
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


@app.route(" /sessions", methods=['POST'])
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

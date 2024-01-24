#!/usr/bin/env python3
"""App module"""
from flask import Flask, jsonify


app = Flask()


@app.route('/')
def message():
    """Returns message"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

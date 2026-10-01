import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000/auth")

def register(email, password):
    response = requests.post(f"{API_URL}/register", json={"email": email, "password": password})
    return response


def login(email, password):
    response = requests.post(
        f"{API_URL}/login",
        data={"username": email, "password": password},  # 👈 use 'username' key
        headers={"Content-Type": "application/x-www-form-urlencoded"}  # 👈 important
    )
    return response

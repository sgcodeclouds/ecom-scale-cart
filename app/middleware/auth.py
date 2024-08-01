import os
import requests
from flask import request, jsonify
from app.util.app_util import generate_response

def authenticate_token():
    def auth_wrapper(func):
        def auth_decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                # return jsonify({"message": "Unauthorized: No token provided"}), 403
                return generate_response(success=False, message="Unauthorized: No token provided"), 403
            data = {
                "token": auth_header
            }

            try:
                response = requests.post(
                    url=os.getenv('API_URL') + "auth/validate-token",
                    json=data,
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                request.user = response.json().get('user')
                return func(*args, **kwargs)
            except requests.RequestException:
                # return jsonify({"message": "Unauthorized: Invalid token"}), 403
                return generate_response(success=False, message="Unauthorized: Invalid token"), 403

        return auth_decorated_function
    return auth_wrapper



from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
MOCK_API_TOKEN = os.getenv("MOCK_API_TOKEN")  # Token clients use to access YOUR mock
REAL_API_URL = os.getenv("REAL_API_URL")      # e.g., "https://real-api.example.com/endpoint"
REAL_API_TOKEN = os.getenv("REAL_API_TOKEN")  # Token to access the real API

@app.route('/platform-asset-1.0.0/latest/filter/access', methods=['POST'])
def get_assets():
    # 1. Authenticate the client
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {MOCK_API_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Forward request to real API
    try:
        headers = {
            'Authorization': f'Bearer {REAL_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Forward all original data (payload + query params)
        response = requests.post(
            REAL_API_URL,
            headers=headers,
            json=request.get_json(),
            params=request.args,
            timeout=10  # Important for production
        )
        
        # 3. Return real API's response exactly
        return jsonify(response.json()), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "Real API timeout"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Real API error: {str(e)}"}), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
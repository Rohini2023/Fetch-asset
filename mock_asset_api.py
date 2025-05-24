from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Sample asset data
sample_assets = [
    {
        "id": "78a99023-eaba-43f6-aa90-453dd079ee0c",
        "displayName": "Fan Coil Unit A",
        "thingCode": "0565251",
        "type": "FanCoilUnit",
        "make": "ACME Corp",
        "model": "FCU-3000",
        "operationStatus": "ACTIVE",
        "communicationStatus": "ONLINE",
        "criticality": "MEDIUM",
        "location": {
            "latitude": 24.3511166,
            "longitude": 54.5205116
        },
        "lastCommunication": (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat(),
        "underMaintenance": False
    },
    {
        "id": "24600149-9a47-454e-af16-4ec05cf0ab1",
        "displayName": "Fan Coil Unit B",
        "thingCode": "0565252",
        "type": "FanCoilUnit",
        "make": "ACME Corp",
        "model": "FCU-3000",
        "operationStatus": "ACTIVE",
        "communicationStatus": "ONLINE",
        "criticality": "LOW",
        "location": {
            "latitude": 24.3531166,
            "longitude": 54.5225116
        },
        "lastCommunication": (datetime.datetime.now() - datetime.timedelta(minutes=30)).isoformat(),
        "underMaintenance": False
    },
    # Add more sample assets as needed
]

@app.route('/platform-asset-1.0.0/latest/filter/access', methods=['POST'])
def get_assets():
    # Verify authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401
    
    
    # Get request payload
    payload = request.get_json()
    
    # Validate required fields
    if not payload or 'domain' not in payload:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Get pagination parameters
    offset = int(payload.get('offset', 1))
    page_size = int(payload.get('pageSize', 10))
    
    # Apply pagination
    start_idx = (offset - 1) * page_size
    end_idx = start_idx + page_size
    paginated_assets = sample_assets[start_idx:end_idx]
    
    # Prepare response
    response = {
        "success": True,
        "data": {
            "total": len(sample_assets),
            "assets": paginated_assets,
            "page": offset,
            "pageSize": page_size
        }
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
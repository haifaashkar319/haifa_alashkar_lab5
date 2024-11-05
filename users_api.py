# users_api.py

#!/usr/bin/python
from flask import Flask, jsonify
from flask_cors import CORS
from database import get_users  # Import the function from database.py

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Define API endpoint for getting all users
@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())  # Use the get_users function

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)  # Ensure it listens on all interfaces



#!/usr/bin/python
import sqlite3

# Function to connect to the database
def connect_to_db():
    conn = sqlite3.connect('database.db')  # Connect to SQLite database
    return conn

# Function to create the users table
def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        );
        ''')
        conn.commit()
        print("User table created successfully")
    except Exception as e:
        print(f"User table creation failed - {e}")
    finally:
        conn.close()

# Function to insert a new user
def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)", 
                    (user['name'], user['email'], user['phone'], user['address'], user['country']))
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        print(f"Insert user failed - {e}")
        conn.rollback()
    finally:
        conn.close()
    return inserted_user

# Function to retrieve all users
def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for i in rows:
            user = {
                "user_id": i["user_id"],
                "name": i["name"],
                "email": i["email"],
                "phone": i["phone"],
                "address": i["address"],
                "country": i["country"]
            }
            users.append(user)
    except Exception as e:
        print(f"Get users failed - {e}")
    finally:
        conn.close()
    return users

# Function to get user by ID
def get_user_by_id(user_id):
    user = None  # Change to None to signify no user found
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:  # Check if row exists
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"]
            }
    except Exception as e:
        print(f"Get user by ID failed - {e}")
    finally:
        conn.close()
    return user  # Return None if user not found

# Function to update a user
def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?", 
                    (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"]))
        conn.commit()
        updated_user = get_user_by_id(user["user_id"])
    except Exception as e:
        print(f"Update user failed - {e}")
        conn.rollback()
    finally:
        conn.close()
    return updated_user

# Function to delete a user
def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE from users WHERE user_id = ?", (user_id,))
        if cur.rowcount == 0:  # Check if any rows were deleted
            message["status"] = "User not found"
        else:
            message["status"] = "User deleted successfully"
        conn.commit()
    except Exception as e:
        print(f"Delete user failed - {e}")
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message




from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Define API endpoints

@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())

@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    user = get_user_by_id(user_id)  # Retrieve user from database
    if user is None:  # Check if user was found
        return jsonify({"error": "User not found"}), 404  # Return 404 if user doesn't exist
    return jsonify(user), 200  # Return user data with 200 OK

@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))

if __name__ == "__main__":
    create_db_table()
    app.run()
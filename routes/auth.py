from flask import Blueprint, request, jsonify
from db import get_db_connection
import pymysql
import logging

logging.basicConfig(level=logging.DEBUG)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    connection = None
    cursor = None
    try:
        # Get JSON data from the request
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone', None)  # Optional field
        role = data.get('role', 'user')  # Default role is 'user'

        # Validate required fields
        if not all([username, email, password]):
            return jsonify({"error": "Missing required fields"}), 400

        # Log received data for debugging
        logging.debug(f"Registering user: {username}, {email}, {phone}, {role}")

        # Insert data into the database
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO users (username, email, password, phone, role)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, email, password, phone, role))
        connection.commit()

        return jsonify({"message": "User registered successfully!"}), 201
    except pymysql.IntegrityError as e:
        logging.error(f"Integrity error: {e}")
        if "Duplicate entry" in str(e):
            if "username" in str(e):
                return jsonify({"error": "Zvolené username sa už používa!"}), 400
            if "email" in str(e):
                return jsonify({"error": "Zvolený email sa už používa!"}), 400
            if "phone" in str(e):
                return jsonify({"error": "Zvolené telefónné číslo sa už používa!"}), 400
        return jsonify({"error": "Database integrity error occurred!"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Get JSON data from the request
        data = request.json
        username = data['username']
        password = data['password']

        # Query to verify user credentials
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT * FROM users WHERE username = %s AND password = %s
        """
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # If user is found, return success with user details
            return jsonify({
                "message": "Login successful!",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "phone": user[4],
                    "role": user[5]
                }
            }), 200
        else:
            return jsonify({"error": "Invalid username or password!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

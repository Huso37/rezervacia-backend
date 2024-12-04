from flask import Blueprint, request, jsonify
from db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Get JSON data from the request
        data = request.json
        username = data['username']
        email = data['email']
        password = data['password']
        phone = data.get('phone', None)  # Optional field
        role = data.get('role', 'user')  # Default role is 'user'

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
        if "Duplicate entry" in str(e):
            if "username" in str(e):
                return jsonify({"error": "Username already exists!"}), 400
            if "email" in str(e):
                return jsonify({"error": "Email already exists!"}), 400
            if "phone" in str(e):
                return jsonify({"error": "Phone number already exists!"}), 400
        return jsonify({"error": "Integrity error occurred!"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
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

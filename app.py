from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Database Configuration
db_config = {
    "host": "Huso38.mysql.pythonanywhere-services.com",
    "user": "Huso38",
    "password": "sqlroot123",  # Replace with your actual MySQL password
    "database": "Huso38$RezervaciaDB"
}

def get_db_connection():
    """Utility function to connect to the database"""
    return pymysql.connect(**db_config)

@app.route('/')
def home():
    return "Welcome! Use /test_db to check the database connection."

@app.route('/test_db')
def test_db():
    try:
        # Establish database connection
        connection = pymysql.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")  # Simple test query
        result = cursor.fetchone()
        connection.close()
        return f"Database connection successful! Test result: {result}"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

@app.route('/register', methods=['POST'])
def register():
    try:
        # Get JSON data from the request
        data = request.json
        username = data['username']
        email = data['email']
        password = data['password']
        phone = data.get('phone', None)  # Optional field

        # Insert data into the database
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO users (username, email, password, phone)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, email, password, phone))
        connection.commit()

        return jsonify({"message": "User registered successfully!"}), 201
    except pymysql.IntegrityError as e:
        return jsonify({"error": "User with this email already exists!"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        # Get JSON data from the request
        data = request.json
        username = data['username']
        password = data['password']

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to verify user credentials
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
                    "phone": user[4]
                }
            }), 200
        else:
            # If user is not found, return an error
            return jsonify({"error": "Invalid username or password!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
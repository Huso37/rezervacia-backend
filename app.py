from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# MySQL Configuration
db_config = {
    "host": "your_username.mysql.pythonanywhere-services.com",
    "user": "your_username",
    "password": "your_password",
    "database": "your_database_name"
}

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO users (username, email, password, phone) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data['username'], data['email'], data['password'], data['phone']))
        connection.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (data['username'], data['password']))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Login successful", "user": {"username": user[1], "email": user[2], "phone": user[4]}})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, jsonify
# from flask_mysqldb import MySQL
import mysql.connector
import base64
import bcrypt

app = Flask(__name__)

# Configuration for MySQL
mysql_host = 'localhost'
mysql_user = 'anagha'
mysql_password = 'anagha123'
mysql_database = 'authentication'

# MySQL Connection
mysql = mysql.connector.connect(
    host='localhost',
    user='anagha',
    password='anagha123',
    database='authentication'
)
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
     # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = mysql.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    mysql.commit()
    cursor.close()

    return jsonify({'message': 'User registered successfully'})


@app.route('/authentication', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        # Passwords match; authentication succeeds
        auth_key = base64.b64encode(f"{username}:{password}".encode()).decode()
        cursor.execute("INSERT INTO basic_auth_key (username, password, auth_key) VALUES (%s, %s, %s)", (username, user[1], auth_key))
        mysql.commit()
        cursor.close()

        return jsonify({'base64EncodedAuthenticationKey': auth_key})
    else:
        # Passwords don't match or user not found; authentication fails
        return jsonify({'error': 'Authentication failed'}), 401


@app.route('/api/resource', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_resource():
    if request.method == 'POST':
        data = request.get_json()
        auth_key = data.get('auth_key')  # Assuming 'auth_key' is included in the request data

        # Verify the auth_key against the database
        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM basic_auth_key WHERE auth_key = %s", (auth_key,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Auth_key matched, proceed with the request

            # Handle the request, e.g., insert data into a MySQL table
            cursor = mysql.cursor()
            cursor.execute("INSERT INTO execute(auth_key) VALUES (%s)", [auth_key])
            mysql.commit()
            cursor.close()

            return jsonify({'message': 'Data saved successfully'})
        else:
            # Auth_key does not match, return an error message
            return jsonify({'error': 'Unauthorized. Invalid auth_key.'}), 401

    # Handle other HTTP methods (GET, PUT, DELETE) or unsupported methods
    return jsonify({'error': 'Unsupported HTTP method'}), 405


if __name__ == '__main__':
    app.run(debug=True)

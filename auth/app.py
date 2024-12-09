from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import render_template
from flask import jsonify

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="tourismdb",
        user="postgres",
        password="password"
    )

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({'status': 'success', 'message': 'Login successful', 'user_id': user['id']}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

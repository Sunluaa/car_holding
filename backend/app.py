from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from functools import wraps

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="tourismdb",
        user="postgres",
        password="password"
    )

# Функция для проверки авторизации
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            user_id = token.split(" ")[1]  # Bearer token
        except IndexError:
            return jsonify({'message': 'Token format is incorrect!'}), 403

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(user, *args, **kwargs)
    return decorated_function

@app.route('/api/cars', methods=['GET'])
@token_required
def get_cars(user):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM cars")
    cars = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(cars)

@app.route('/api/cars', methods=['POST'])
@token_required
def add_car(user):
    data = request.json
    make = data['make']
    color = data['color']
    year = data['year']
    license_plate = data['license_plate']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO cars (make, color, year, license_plate) VALUES (%s, %s, %s, %s) RETURNING *",
                (make, color, year, license_plate))
    car = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Car added successfully', 'car': car}), 201

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
@token_required
def delete_car(user, car_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cars WHERE id = %s RETURNING *", (car_id,))
    car = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if car:
        return jsonify({'message': 'Car deleted successfully', 'car': car}), 200
    else:
        return jsonify({'message': 'Car not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

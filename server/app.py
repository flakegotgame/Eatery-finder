from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime

app = Flask(__name__)
CORS(app)

SECRET_KEY = "your-secret-key"  

users = [{"email": "test@example.com", "password": "password"}]

# Sample restaurant data
restaurants = [
    {'id': 1, 'name': 'Restaurant A', 'description': 'Delicious Italian food', 'address': '123 Pasta St', 'phone': '123-456', 'website': 'http://restaurant-a.com'},
    {'id': 2, 'name': 'Restaurant B', 'description': 'Authentic Sushi experience', 'address': '456 Fish Rd', 'phone': '789-101', 'website': 'http://restaurant-b.com'},
]

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if user already exists
    for user in users:
        if user['email'] == email:
            return jsonify({'message': 'User already exists'}), 400

    # Register the user
    users.append({'email': email, 'password': password})
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate credentials
    for user in users:
        if user['email'] == email and user['password'] == password:
            # Create JWT token with expiration time (e.g., 1 hour)
            token = jwt.encode({
                'email': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
            }, SECRET_KEY, algorithm='HS256')

            return jsonify({'message': 'Login successful', 'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    # Get the token from the request's Authorization header
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Unauthorized: No token found'}), 401

    try:
        token = token.split(" ")[1]

        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return jsonify(restaurants), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True)

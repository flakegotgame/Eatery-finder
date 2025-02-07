from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Restaurant

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Change this for production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your-default-secret-key")

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

# Authentication Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        token = jwt.encode(
            {'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            app.config['SECRET_KEY'], algorithm='HS256'
        )
        return jsonify({'message': 'Login successful', 'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Unauthorized: No token found'}), 401

    try:
        token = token.split(" ")[1]  # Extract token after 'Bearer'
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        restaurants = Restaurant.query.all()
        # Serialize restaurants to JSON format
        restaurants_data = [r.to_dict() for r in restaurants]

        return jsonify(restaurants_data), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True)

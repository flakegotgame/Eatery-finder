from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Using SQLite (Change for production)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your-default-secret-key")

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    website = db.Column(db.String(200))

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
        restaurants_data = [{'id': r.id, 'name': r.name, 'description': r.description,
                             'address': r.address, 'phone': r.phone, 'website': r.website} for r in restaurants]

        return jsonify(restaurants_data), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True)

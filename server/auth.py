from flask import request, jsonify
from flask_jwt_extended import create_access_token, JWTManager
from app import app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"  # In production, this should be an environment variable
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already in use"}), 400

    hashed_password = generate_password_hash(data['password'])
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        # Generate a JWT token with expiration (e.g., 1 hour)
        token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
        return jsonify(access_token=token), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

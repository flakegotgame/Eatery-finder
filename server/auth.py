from flask import request, jsonify
from flask_jwt_extended import create_access_token, JWTManager
from app import app
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)
    return jsonify({"error": "Invalid credentials"}), 401

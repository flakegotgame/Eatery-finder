import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Database URI for SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask's modification tracking feature
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')  # Secret key for sessions
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")  # JWT secret key

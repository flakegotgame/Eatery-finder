from app import app
from models import db, User, Restaurant

with app.app_context():
    db.create_all()

    user1 = User(username="victor", email="victor@example.com", password="password123")
    restaurant1 = Restaurant(name="Tasty Bites", location="Nairobi")

    db.session.add_all([user1, restaurant1])
    db.session.commit()

    print("Database seeded successfully!")

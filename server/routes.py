from flask import request, jsonify
from flask_restful import Resource
from app import db
from models import User, Restaurant

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

class RestaurantResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants])

def initialize_routes(api):
    api.add_resource(UserResource, '/users')
    api.add_resource(RestaurantResource, '/restaurants')

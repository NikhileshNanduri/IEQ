from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from models import *

bp = Blueprint('authentication', __name__)

# Authentication route
@bp.route('/auth', methods=['POST'])
def authenticate():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        # Fetch user from the database
        user = users_collection.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=username, additional_claims={"role": user["role"]})
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Registration route
@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')  # Default role is 'user'

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        # Check if the username already exists
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        new_user = {
            'username': username,
            'password': hashed_password,
            'role': role
        }
        redis_client.delete('users')
        users_collection.insert_one(new_user)
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

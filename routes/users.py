from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models import *
import json

bp = Blueprint('users', __name__)

# Route to get all users
@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        current_user_role = get_jwt()["role"]
        if current_user_role == "admin":  
            # Check if products exist in the cache
            cached_users = redis_client.get('users')
            if cached_users:
                cached_users_str = cached_users.decode('utf-8')
                return jsonify(json.loads(cached_users_str))            
            else:
                users = list(users_collection.find({}, {'_id': 0}))
                tmp = []
                for user in users:
                    tmp.append(user)
                redis_client.set('users', json.dumps(tmp))
                return jsonify(users)
        else:
            return {"message" : "Restricted view only for admins"} , 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get a specific user by username
@bp.route('/users/<string:username>', methods=['GET'])
@jwt_required()
def get_user(username):
    try:
        current_user_role = get_jwt()["role"]
        if current_user_role == "admin":  
            cached_user = redis_client.get(f'username:{username}')
            if cached_user:
                user_data = json.loads(cached_user.decode('utf-8'))
                return jsonify(user_data)
            else:
                user = users_collection.find_one({'username': username}, {'_id': 0})
                if user:          
                    return jsonify(user)
                return jsonify({"message": "User not found"}), 404        
        else:
            return {"message" : "Restricted view only for admins"} , 401    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a user
@bp.route('/users/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    try:
        current_user_role = get_jwt()["role"]
        if current_user_role == "admin":  
            result = users_collection.delete_one({'username': username})
            if result.deleted_count:
                cached_users = redis_client.get('users')
                if cached_users:
                    cached_users_str = cached_users.decode('utf-8')
                    users = json.loads(cached_users_str)
                    # Remove the user with the specified username
                    users = [user for user in users if user.get('username') != username]
                    redis_client.set('users', json.dumps(users))        
                return jsonify({'message': 'User deleted'})
            return jsonify({'message': 'User not found'}), 404
        else:
            return {"message" : "Restricted view only for admins"} , 401    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

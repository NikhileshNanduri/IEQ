from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from models import *
import json

bp = Blueprint('products', __name__)

# Route to get all products
@bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    try:
        # Check if products exist in the cache
        cached_products = redis_client.get('products')
        if cached_products:
            cached_products_str = cached_products.decode('utf-8')
            return jsonify(json.loads(cached_products_str))            
        else:
            products = list(products_collection.find({}, {'_id': 0}))
            tmp = []
            for product in products:
                tmp.append(product)
            redis_client.set('products', json.dumps(tmp))
            return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get a specific product by ID
@bp.route('/products/<string:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    try:
        cached_product = redis_client.get(f'product:{product_id}')
        if cached_product:
            product_data = json.loads(cached_product.decode('utf-8'))
            return jsonify(product_data)
        else:
            product = products_collection.find_one({'product_id': product_id}, {'_id': 0})
            if product:          
                return jsonify(product)
            return jsonify({"message": "Product not found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to add a new product
@bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    try:
        current_user_role = get_jwt()["role"]
        if current_user_role == "admin":
            data = request.json
            product_id = data['product_id']
            existing_product = products_collection.find_one({'product_id': product_id})
            if existing_product:
                return jsonify({'message': 'Product already exists'}), 400
            redis_client.delete('products')
            products_collection.insert_one(data)
            return {"message" : "Data Inserted"} , 201
        else:
            return {"message" : "Restricted view only for admins"} , 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to update an existing product
@bp.route('/products/<string:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        current_user_role = get_jwt()["role"]
        if current_user_role == "admin":  
            data = request.json
            result = products_collection.update_one({'product_id': product_id}, {'$set': data})
            cached_products = redis_client.get('products')
            if cached_products:
                cached_products_str = cached_products.decode('utf-8')
                products = json.loads(cached_products_str)
                for index, product in enumerate(products):
                    if product.get('product_id') == product_id:
                        # Update the specific product
                        products[index] = data
                        redis_client.set('products', json.dumps(products))      
            if result.modified_count:
                return jsonify(data)
            return jsonify({'message': 'Product not found'}), 404
        else:
            return {"message" : "Restricted view only for admins"} , 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a product
@bp.route('/products/<string:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        current_user_role = get_jwt()["role"]
        if current_user_role == "admin":  
            result = products_collection.delete_one({'product_id': product_id})
            if result.deleted_count:
                cached_products = redis_client.get('products')
                if cached_products:
                    cached_products_str = cached_products.decode('utf-8')
                    products = json.loads(cached_products_str)
                    # Remove the product with the specified product_id
                    products = [product for product in products if product.get('product_id') != product_id]
                    redis_client.set('products', json.dumps(products))        
                return jsonify({'message': 'Product deleted'})
            return jsonify({'message': 'Product not found'}), 404
        else:
            return {"message" : "Restricted view only for admins"} , 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

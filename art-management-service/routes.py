from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from __main__ import app, db, limiter, redis_client
from models.artworks import Artworks
from sqlalchemy import text
import requests
import json


LOGIN_SERVICE_URL = 'http://login-service:5000/api/'

@app.route('/api/artworks/<int:id>', methods=['GET'])
def get_artwork(id):
    artwork = Artworks.query.get(id)
    if artwork:
        return jsonify({
            'id': artwork.id,
            'title': artwork.title,
            'description': artwork.description,
            'price': artwork.price,
            'category': artwork.category,
            'image_url': artwork.image_url,
            'created_at': artwork.created_at.isoformat()
        })
    else:
        return jsonify({'message': 'Artwork not found'}), 404

@app.route('/api/artworks/', methods=['GET'])
def get_all_artworks():
    artworks = Artworks.query.all()
    return jsonify([{
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'category': artwork.category,
        'image_url': artwork.image_url,
        'created_at': artwork.created_at.isoformat()
    } for artwork in artworks])

@app.route('/api/artworks/popular', methods=['GET'])
def get_popular_artworks():
    cache_key = 'popular_artworks'

    cached_results = redis_client.get(cache_key)
    if cached_results:
        return jsonify(message='Results retrieved from cache', data=json.loads(cached_results))

    artworks = Artworks.query.limit(3).all()

    response_data = [{
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'category': artwork.category,
        'image_url': artwork.image_url,
        'created_at': artwork.created_at.isoformat()
    } for artwork in artworks]

    # Cache the results
    redis_client.set(cache_key, json.dumps(response_data), ex=300)

    return jsonify(response_data)

@app.route('/api/artworks/search', methods=['GET'])
def search_artworks():
    title = request.args.get('title')
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    cache_key = f"search:artworks:title={title}&category={category}&min_price={min_price}&max_price={max_price}"

    # Check if the results are already cached
    cached_results = redis_client.get(cache_key)
    if cached_results:
        return jsonify(message='Results retrieved from cache', data=json.loads(cached_results))

    query = Artworks.query

    if title:
        query = query.filter(Artworks.title.ilike(f'%{title}%'))
    if category:
        query = query.filter(Artworks.category.ilike(f'%{category}%'))
    if min_price:
        try:
            query = query.filter(Artworks.price >= float(min_price))
        except ValueError:
            return jsonify({'message': 'Invalid min_price format'}), 400
    if max_price:
        try:
            query = query.filter(Artworks.price <= float(max_price))
        except ValueError:
            return jsonify({'message': 'Invalid max_price format'}), 400

    artworks = query.all()

    response_data = [{
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'category': artwork.category,
        'image_url': artwork.image_url,
        'created_at': artwork.created_at.isoformat()
    } for artwork in artworks]

    # Cache the results
    redis_client.set(cache_key, json.dumps(response_data), ex=300)

    return jsonify(response_data)

@app.route('/api/artworks/', methods=['POST'])
@jwt_required()
def post_artwork():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'price', 'category', 'image_url']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    try:
        price = float(data.get('price'))
    except ValueError:
        return jsonify({'message': 'Price must be a number'}), 400

    new_artwork = Artworks(
        title=data.get('title'),
        description=data.get('description'),
        price=price,
        category=data.get('category'),
        image_url=data.get('image_url')
    )
    db.session.add(new_artwork)
    db.session.commit()
    
    return jsonify({'message': 'Artwork created', 'id': new_artwork.id}), 201

@app.route('/api/artworks/<int:id>', methods=['PUT'])
@jwt_required()
def update_artwork(id):
    artwork = Artworks.query.get(id)
    if not artwork:
        return jsonify({'message': 'Artwork not found'}), 404

    data = request.get_json()

    # Update only the fields present in the request
    if 'title' in data:
        artwork.title = data['title']
    if 'description' in data:
        artwork.description = data['description']
    if 'price' in data:
        try:
            artwork.price = float(data['price'])
        except ValueError:
            return jsonify({'message': 'Price must be a number'}), 400
    if 'category' in data:
        artwork.category = data['category']
    if 'image_url' in data:
        artwork.image_url = data['image_url']

    db.session.commit()

    return jsonify({'message': 'Artwork updated successfully'}), 200


@app.route('/api/artworks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_artwork(id):
    artwork = Artworks.query.get(id)
    if not artwork:
        return jsonify({'message': 'Artwork not found'}), 404

    db.session.delete(artwork)
    db.session.commit()

    return jsonify({'message': 'Artwork deleted successfully'}), 200

@app.route('/api/artworks/status', methods=['GET'])
def status():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'OK', 'database': 'Connected'}), 200
    except Exception as e:
        return jsonify({'status': 'ERROR', 'database': 'Not connected', 'error': str(e)}), 500

@app.route('/api/artworks/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Send a PUT request to the login service to update the user profile
    update_response = requests.put(f'{LOGIN_SERVICE_URL}/users/{user_id}', json=data)
    
    if update_response.status_code != 200:
        return jsonify({'message': update_response.json().get('message', 'Error occurred')}), update_response.status_code
    
    if data.get('password'):
        return jsonify({'message': 'Password updated successfully. Please log-in again'}), 200
    else:
        return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/api/artworks/profile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    user_id = get_jwt_identity()

    headers = {
        'Authorization': f'{request.headers.get("Authorization")}'
    }

    # Send a DELETE request to the login service to delete the user profile
    delete_response = requests.delete(f'{LOGIN_SERVICE_URL}/users/{user_id}', headers=headers)
    
    if delete_response.status_code != 200:
        return jsonify({'message': delete_response.json().get('message', 'Error occurred')}), delete_response.status_code
    
    return jsonify({'message': 'Account deleted successfully'}), 200
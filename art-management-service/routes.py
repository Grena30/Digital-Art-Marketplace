from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from __main__ import app, db, limiter
from models.artworks import Artworks
from sqlalchemy import text
import requests


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

@app.route('/api/artworks/', methods=['POST'])
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

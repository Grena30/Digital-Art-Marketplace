from flask import request, jsonify
from __main__ import app, db, limiter
from models.artworks import Artworks
from sqlalchemy import text


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

@app.route('/api/artworks', methods=['GET'])
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

@app.route('/api/artworks', methods=['POST'])
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

@app.route('/api/artworks/status', methods=['GET'])
def status():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'OK', 'database': 'Connected'}), 200
    except Exception as e:
        return jsonify({'status': 'ERROR', 'database': 'Not connected', 'error': str(e)}), 500
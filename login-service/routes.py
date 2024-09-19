from flask import request, jsonify
from __main__ import app, db
from models.user import User


@app.route('/api/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email, password=password).first()
        if user and user.password == password:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return jsonify({'message': 'Passwords do not match'}), 400

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400

        # Create new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
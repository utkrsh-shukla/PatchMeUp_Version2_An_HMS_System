from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Patient
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['email', 'password', 'name']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'error': 'Email already registered'}), 400
    
    user = User(email=data['email'], role='patient')
    user.set_password(data['password'])
    db.session.add(user)
    db.session.flush()
    
    patient = Patient(
        user_id=user.id, name=data['name'], phone=data.get('phone'),
        date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
        blood_group=data.get('blood_group'), address=data.get('address'), medical_history=data.get('medical_history')
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Registration successful', 'data': user.to_dict(include_role_data=True)}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
    
    if not user.is_active:
        return jsonify({'success': False, 'error': 'Account has been deactivated'}), 403
    
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({
        'success': True, 'message': 'Login successful',
        'data': {'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict(include_role_data=True)}
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user or not user.is_active:
        return jsonify({'success': False, 'error': 'Invalid user'}), 401
    
    access_token = create_access_token(identity=str(current_user_id), additional_claims={'role': user.role})
    return jsonify({'success': True, 'data': {'access_token': access_token}}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    return jsonify({'success': True, 'data': user.to_dict(include_role_data=True)}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

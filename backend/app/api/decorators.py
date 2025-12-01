from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def doctor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'doctor':
            return jsonify({'success': False, 'error': 'Doctor access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def patient_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'patient':
            return jsonify({'success': False, 'error': 'Patient access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

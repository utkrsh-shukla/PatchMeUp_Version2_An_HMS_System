from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class User(db.Model):
    """Base user model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, doctor, patient
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    doctor = db.relationship('Doctor', backref='user', uselist=False, cascade='all, delete-orphan')
    patient = db.relationship('Patient', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_role_data=False):
        """Serialize user to dictionary"""
        data = {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_role_data:
            if self.role == 'doctor' and self.doctor:
                data['doctor'] = self.doctor.to_dict()
            elif self.role == 'patient' and self.patient:
                data['patient'] = self.patient.to_dict()
        
        return data
    
    def __repr__(self):
        return f'<User {self.email}>'

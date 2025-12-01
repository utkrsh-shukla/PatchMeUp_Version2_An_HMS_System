from app import db
from datetime import datetime

class Appointment(db.Model):
    """Appointment model"""
    __tablename__ = 'appointments'
    __table_args__ = (
        db.Index('idx_doctor_date_time', 'doctor_id', 'date', 'time', unique=True),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='booked')  # booked, completed, cancelled, rescheduled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    treatment = db.relationship('Treatment', backref='appointment', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, include_doctor=True, include_patient=True, include_treatment=False):
        """Serialize appointment to dictionary"""
        data = {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date': self.date.isoformat(),
            'time': self.time.strftime('%H:%M'),
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_doctor:
            data['doctor'] = {
                'id': self.doctor.id,
                'name': self.doctor.name,
                'specialization': self.doctor.specialization,
                'department': self.doctor.department.name if self.doctor.department else None
            }
        
        if include_patient:
            data['patient'] = {
                'id': self.patient.id,
                'name': self.patient.name,
                'phone': self.patient.phone,
                'blood_group': self.patient.blood_group
            }
        
        if include_treatment and self.treatment:
            data['treatment'] = self.treatment.to_dict()
        
        return data
    
    def __repr__(self):
        return f'<Appointment {self.id}: {self.patient.name} with {self.doctor.name}>'

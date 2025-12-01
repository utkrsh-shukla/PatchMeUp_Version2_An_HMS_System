from app import db
from datetime import datetime

class Patient(db.Model):
    """Patient profile model"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    blood_group = db.Column(db.String(5))
    medical_history = db.Column(db.Text)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_appointments=False, include_stats=False):
        """Serialize patient to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'address': self.address,
            'blood_group': self.blood_group,
            'medical_history': self.medical_history,
            'email': self.user.email,
            'is_active': self.user.is_active
        }
        
        if include_appointments:
            from app.models.appointment import Appointment
            data['appointments'] = [apt.to_dict(include_treatment=True) 
                                   for apt in self.appointments.order_by(
                                       Appointment.date.desc(), Appointment.time.desc()
                                   ).all()]
        
        if include_stats:
            from datetime import date
            data['total_appointments'] = self.appointments.count()
            data['completed_appointments'] = self.appointments.filter_by(status='completed').count()
            data['upcoming_appointments'] = self.appointments.filter(
                db.and_(
                    db.or_(
                        db.text("appointments.date > :today"),
                        db.and_(
                            db.text("appointments.date = :today"),
                            db.text("appointments.status IN ('booked', 'rescheduled')")
                        )
                    )
                )
            ).params(today=date.today()).count()
        
        return data
    
    def __repr__(self):
        return f'<Patient {self.name}>'

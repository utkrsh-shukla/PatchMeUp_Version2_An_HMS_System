from app import db

class Doctor(db.Model):
    """Doctor profile model"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    phone = db.Column(db.String(20))
    years_of_experience = db.Column(db.Integer)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    availability_slots = db.relationship('Availability', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_availability=False):
        """Serialize doctor to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'specialization': self.specialization,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'phone': self.phone,
            'years_of_experience': self.years_of_experience,
            'email': self.user.email,
            'is_active': self.user.is_active
        }
        
        if include_availability:
            from datetime import date, timedelta
            today = date.today()
            next_7_days = [today + timedelta(days=i) for i in range(7)]
            availability_by_day = {}
            
            for day in next_7_days:
                day_of_week = day.weekday()
                slots = [slot.to_dict() for slot in self.availability_slots.filter_by(
                    day_of_week=day_of_week,
                    is_available=True
                ).all()]
                availability_by_day[day.isoformat()] = {
                    'date': day.isoformat(),
                    'day_name': day.strftime('%A'),
                    'slots': slots
                }
            
            data['availability'] = availability_by_day
        
        return data
    
    def __repr__(self):
        return f'<Doctor {self.name}>'

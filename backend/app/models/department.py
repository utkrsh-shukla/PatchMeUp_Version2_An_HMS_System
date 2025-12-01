from app import db

class Department(db.Model):
    """Department/Specialization model"""
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    doctors = db.relationship('Doctor', backref='department', lazy='dynamic')
    
    def to_dict(self, include_doctors=False):
        """Serialize department to dictionary"""
        # Count active doctors in this department using raw SQL to avoid circular imports
        doctor_count = db.session.execute(
            db.text("""
                SELECT COUNT(*) 
                FROM doctors d 
                JOIN users u ON d.user_id = u.id 
                WHERE d.department_id = :dept_id AND u.is_active = 1
            """),
            {'dept_id': self.id}
        ).scalar()
        

        
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'doctor_count': doctor_count or 0
        }
        
        if include_doctors:
            data['doctors'] = [doctor.to_dict() for doctor in self.doctors if doctor.user.is_active]
        
        return data
    
    def __repr__(self):
        return f'<Department {self.name}>'

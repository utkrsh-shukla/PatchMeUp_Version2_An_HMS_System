"""Database initialization script for HMS V2"""
from app import create_app, db
from app.models import User, Department, Doctor
from datetime import time

def init_database():
    """Initialize database with tables, admin user, and sample departments"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@hospital.com').first()
        
        if not admin:
            print("\nCreating default admin user...")
            admin = User(
                email='admin@hospital.com',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created (email: admin@hospital.com, password: admin123)")
        else:
            print("\n• Admin user already exists")
        
        # Create sample departments
        departments_data = [
            {
                'name': 'Cardiology',
                'description': 'Heart and cardiovascular system care'
            },
            {
                'name': 'Neurology',
                'description': 'Brain and nervous system disorders'
            },
            {
                'name': 'Orthopedics',
                'description': 'Bone, joint, and muscle treatment'
            },
            {
                'name': 'Pediatrics',
                'description': 'Medical care for infants, children, and adolescents'
            },
            {
                'name': 'General Medicine',
                'description': 'General health and wellness care'
            },
            {
                'name': 'Dermatology',
                'description': 'Skin, hair, and nail care'
            },
            {
                'name': 'Oncology',
                'description': 'Cancer diagnosis and treatment'
            }
        ]
        
        print("\nCreating sample departments...")
        for dept_data in departments_data:
            existing = Department.query.filter_by(name=dept_data['name']).first()
            if not existing:
                dept = Department(**dept_data)
                db.session.add(dept)
                print(f"  - {dept_data['name']}")
        
        db.session.commit()
        
        print("\n✓ Database initialized successfully!")
        print("\n" + "=" * 60)
        print("Default Credentials:")
        print("  Admin Email: admin@hospital.com")
        print("  Password: admin123")
        print("=" * 60)

if __name__ == '__main__':
    init_database()

"""Flask API application runner"""
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    
    print("=" * 60)
    print("Hospital Management System V2 - API Server")
    print("=" * 60)
    print(f"\nAPI running at: http://localhost:5000")
    print("\nAPI Endpoints:")
    print("- Health Check: http://localhost:5000/api/health")
    print("- Auth: http://localhost:5000/api/auth/...")
    print("- Admin: http://localhost:5000/api/admin/...")
    print("- Doctor: http://localhost:5000/api/doctor/...")
    print("- Patient: http://localhost:5000/api/patient/...")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Blueprint, request, jsonify
from app import db, cache
from app.models import User, Doctor, Patient, Department, Appointment
from app.api.decorators import admin_required
from datetime import datetime, date

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    stats = cache.get('admin_stats')
    if stats is None:
        stats = {
            'total_doctors': Doctor.query.join(User).filter(User.is_active == True).count(),
            'total_patients': Patient.query.join(User).filter(User.is_active == True).count(),
            'total_appointments': Appointment.query.count(),
            'booked_appointments': Appointment.query.filter_by(status='booked').count(),
            'completed_appointments': Appointment.query.filter_by(status='completed').count(),
            'cancelled_appointments': Appointment.query.filter_by(status='cancelled').count()
        }
        cache.set('admin_stats', stats, timeout=60)
    return jsonify({'success': True, 'data': stats}), 200

@admin_bp.route('/doctors', methods=['GET'])
@admin_required
def list_doctors():
    doctors = Doctor.query.join(User).filter(User.is_active == True).all()
    return jsonify({'success': True, 'data': [doctor.to_dict() for doctor in doctors]}), 200

@admin_bp.route('/doctors', methods=['POST'])
@admin_required
def create_doctor():
    data = request.get_json()
    required_fields = ['email', 'password', 'name', 'specialization']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'error': 'Email already registered'}), 400
    
    user = User(email=data['email'], role='doctor')
    user.set_password(data['password'])
    db.session.add(user)
    db.session.flush()
    
    doctor = Doctor(
        user_id=user.id, name=data['name'], specialization=data['specialization'],
        department_id=data.get('department_id'), phone=data.get('phone'),
        years_of_experience=data.get('years_of_experience')
    )
    db.session.add(doctor)
    db.session.flush()
    
    from app.models.availability import Availability
    from datetime import time
    for day in range(5):
        availability = Availability(doctor_id=doctor.id, day_of_week=day, 
                                  start_time=time(9, 0), end_time=time(17, 0), is_available=True)
        db.session.add(availability)
    
    db.session.commit()
    cache.delete('admin_stats')
    return jsonify({'success': True, 'message': 'Doctor created successfully', 'data': doctor.to_dict()}), 201

@admin_bp.route('/doctors/<int:id>', methods=['GET'])
@admin_required
def get_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    return jsonify({'success': True, 'data': doctor.to_dict(include_availability=True)}), 200

@admin_bp.route('/doctors/<int:id>', methods=['PUT'])
@admin_required
def update_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    data = request.get_json()
    doctor.name = data.get('name', doctor.name)
    doctor.specialization = data.get('specialization', doctor.specialization)
    doctor.department_id = data.get('department_id', doctor.department_id)
    doctor.phone = data.get('phone', doctor.phone)
    doctor.years_of_experience = data.get('years_of_experience', doctor.years_of_experience)
    db.session.commit()
    cache.delete('admin_stats')
    cache.delete(f'doctor_availability_{id}')
    cache.delete(f'doctor_detail_{id}')
    return jsonify({'success': True, 'message': 'Doctor updated successfully', 'data': doctor.to_dict()}), 200

@admin_bp.route('/doctors/<int:id>', methods=['DELETE'])
@admin_required
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    doctor.user.is_active = False
    db.session.commit()
    cache.delete('admin_stats')
    return jsonify({'success': True, 'message': 'Doctor deactivated successfully'}), 200

@admin_bp.route('/patients', methods=['GET'])
@admin_required
def list_patients():
    patients = Patient.query.join(User).filter(User.is_active == True).all()
    return jsonify({'success': True, 'data': [patient.to_dict() for patient in patients]}), 200

@admin_bp.route('/patients/<int:id>', methods=['GET'])
@admin_required
def get_patient(id):
    patient = Patient.query.get_or_404(id)
    return jsonify({'success': True, 'data': patient.to_dict(include_stats=True)}), 200

@admin_bp.route('/patients/<int:id>/history', methods=['GET'])
@admin_required
def get_patient_history(id):
    patient = Patient.query.get_or_404(id)
    return jsonify({'success': True, 'data': patient.to_dict(include_appointments=True)}), 200

@admin_bp.route('/patients/<int:id>', methods=['PUT'])
@admin_required
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    data = request.get_json()
    patient.name = data.get('name', patient.name)
    patient.phone = data.get('phone', patient.phone)
    patient.address = data.get('address', patient.address)
    patient.blood_group = data.get('blood_group', patient.blood_group)
    patient.medical_history = data.get('medical_history', patient.medical_history)
    if data.get('date_of_birth'):
        patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Patient updated successfully', 'data': patient.to_dict()}), 200

@admin_bp.route('/patients/<int:id>', methods=['DELETE'])
@admin_required
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    patient.user.is_active = False
    db.session.commit()
    cache.delete('admin_stats')
    return jsonify({'success': True, 'message': 'Patient deactivated successfully'}), 200

@admin_bp.route('/appointments', methods=['GET'])
@admin_required
def list_appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return jsonify({'success': True, 'data': [apt.to_dict(include_treatment=True) for apt in appointments]}), 200

@admin_bp.route('/appointments/upcoming', methods=['GET'])
@admin_required
def list_upcoming_appointments():
    today = date.today()
    appointments = Appointment.query.filter(
        Appointment.date >= today, Appointment.status.in_(['booked', 'rescheduled'])
    ).order_by(Appointment.date, Appointment.time).all()
    return jsonify({'success': True, 'data': [apt.to_dict() for apt in appointments]}), 200

@admin_bp.route('/search', methods=['GET'])
@admin_required
def search():
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all')
    if not query:
        return jsonify({'success': False, 'error': 'Search query required'}), 400
    
    results = {'doctors': [], 'patients': []}
    if search_type in ['all', 'doctor']:
        doctors = Doctor.query.join(User).filter(
            User.is_active == True, db.or_(Doctor.name.ilike(f'%{query}%'), Doctor.specialization.ilike(f'%{query}%'))
        ).all()
        results['doctors'] = [doctor.to_dict() for doctor in doctors]
    
    if search_type in ['all', 'patient']:
        patients = Patient.query.join(User).filter(User.is_active == True, Patient.name.ilike(f'%{query}%')).all()
        results['patients'] = [patient.to_dict() for patient in patients]
    
    return jsonify({'success': True, 'data': results}), 200

@admin_bp.route('/departments', methods=['GET'])
@admin_required
def list_departments():
    cache.delete('departments_list')
    depts = Department.query.all()
    return jsonify({'success': True, 'data': [dept.to_dict() for dept in depts]}), 200

@admin_bp.route('/users/<int:id>/toggle-status', methods=['PUT'])
@admin_required
def toggle_user_status(id):
    user = User.query.get_or_404(id)
    user.is_active = not user.is_active
    db.session.commit()
    cache.delete('admin_stats')
    return jsonify({
        'success': True, 
        'message': f"User {'activated' if user.is_active else 'deactivated'} successfully",
        'data': {'is_active': user.is_active}
    }), 200

@admin_bp.route('/jobs/trigger-reminders', methods=['POST'])
@admin_required
def trigger_daily_reminders():
    from app.tasks.reminders import send_daily_reminders
    task = send_daily_reminders.delay()
    return jsonify({'success': True, 'message': 'Daily reminders job triggered', 'data': {'task_id': task.id}}), 202

@admin_bp.route('/jobs/trigger-reports', methods=['POST'])
@admin_required
def trigger_monthly_reports():
    from app.tasks.reports import generate_monthly_reports
    task = generate_monthly_reports.delay()
    return jsonify({'success': True, 'message': 'Monthly reports job triggered', 'data': {'task_id': task.id}}), 202

@admin_bp.route('/jobs/<task_id>/status', methods=['GET'])
@admin_required
def get_job_status(task_id):
    from app.celery_config import celery_app
    task = celery_app.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Job is waiting to be processed'}
    elif task.state == 'PROGRESS':
        response = {'state': task.state, 'status': task.info.get('status', 'Processing...'), 'progress': task.info.get('progress', 0)}
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'status': 'Job completed successfully', 'result': task.result}
    else:
        response = {'state': task.state, 'status': 'Job failed', 'error': str(task.info)}
    return jsonify({'success': True, 'data': response}), 200

@admin_bp.route('/jobs/active', methods=['GET'])
@admin_required
def get_active_jobs():
    from app.celery_config import celery_app
    inspect = celery_app.control.inspect()
    active_tasks = inspect.active()
    scheduled_tasks = inspect.scheduled()
    jobs = []
    if active_tasks:
        for worker, tasks in active_tasks.items():
            for task in tasks:
                jobs.append({'id': task['id'], 'name': task['name'], 'worker': worker, 'status': 'running', 
                           'args': task.get('args', []), 'kwargs': task.get('kwargs', {}), 'time_start': task.get('time_start')})
    if scheduled_tasks:
        for worker, tasks in scheduled_tasks.items():
            for task in tasks:
                jobs.append({'id': task['request']['id'], 'name': task['request']['task'], 'worker': worker, 'status': 'scheduled',
                           'args': task['request'].get('args', []), 'kwargs': task['request'].get('kwargs', {}), 'eta': task.get('eta')})
    return jsonify({'success': True, 'data': jobs}), 200

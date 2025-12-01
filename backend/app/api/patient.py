from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import get_jwt_identity
from app import db, cache
from app.models import Patient, Doctor, Department, Appointment, Availability, Treatment
from app.api.decorators import patient_required
from datetime import datetime, date

patient_bp = Blueprint('patient', __name__)

def get_current_patient():
    user_id = int(get_jwt_identity())
    return Patient.query.filter_by(user_id=user_id).first_or_404()

@patient_bp.route('/stats', methods=['GET'])
@patient_required
def get_stats():
    patient = get_current_patient()
    today = date.today()
    stats = {
        'total_appointments': patient.appointments.count(),
        'upcoming_appointments': patient.appointments.filter(
            Appointment.date >= today, Appointment.status.in_(['booked', 'rescheduled'])
        ).count(),
        'completed_appointments': patient.appointments.filter_by(status='completed').count()
    }
    return jsonify({'success': True, 'data': stats}), 200

@patient_bp.route('/departments', methods=['GET'])
@patient_required
def list_departments():
    cache.delete('departments_list')
    depts = Department.query.all()
    return jsonify({'success': True, 'data': [dept.to_dict() for dept in depts]}), 200

@patient_bp.route('/doctors', methods=['GET'])
@patient_required
def list_doctors():
    dept_id = request.args.get('department_id', type=int)
    search_query = request.args.get('search', '').strip()
    
    # Base query - only active doctors
    query = Doctor.query.join(Doctor.user).filter(Doctor.user.has(is_active=True))
    
    # Filter by department if specified
    if dept_id:
        query = query.filter(Doctor.department_id == dept_id)
    
    # Filter by search query (name or specialization)
    if search_query:
        search_filter = db.or_(
            Doctor.name.ilike(f'%{search_query}%'),
            Doctor.specialization.ilike(f'%{search_query}%')
        )
        query = query.filter(search_filter)
    
    doctors = query.all()
    return jsonify({'success': True, 'data': [doctor.to_dict() for doctor in doctors]}), 200

@patient_bp.route('/doctors/<int:id>', methods=['GET'])
@patient_required
def get_doctor_detail(id):
    cache_key = f'doctor_detail_{id}'
    doctor_data = cache.get(cache_key)
    if doctor_data is None:
        doctor = Doctor.query.get_or_404(id)
        doctor_data = doctor.to_dict(include_availability=True)
        cache.set(cache_key, doctor_data, timeout=3600)
    return jsonify({'success': True, 'data': doctor_data}), 200

@patient_bp.route('/appointments', methods=['POST'])
@patient_required
def book_appointment():
    patient = get_current_patient()
    data = request.get_json()
    required_fields = ['doctor_id', 'date', 'time']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    doctor_id = data['doctor_id']
    apt_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    apt_time = datetime.strptime(data['time'], '%H:%M').time()
    
    if apt_date < date.today():
        return jsonify({'success': False, 'error': 'Appointment date must be in the future'}), 400
    
    day_of_week = apt_date.weekday()
    availability_slots = Availability.query.filter_by(doctor_id=doctor_id, day_of_week=day_of_week, is_available=True).all()
    
    if not availability_slots:
        return jsonify({'success': False, 'error': 'Doctor is not available on this day'}), 400
    
    is_within_slot = any(slot.start_time <= apt_time < slot.end_time for slot in availability_slots)
    if not is_within_slot:
        return jsonify({'success': False, 'error': 'Doctor is not available at this time'}), 400
    
    existing = Appointment.query.filter_by(doctor_id=doctor_id, date=apt_date, time=apt_time, status='booked').first()
    if existing:
        return jsonify({'success': False, 'error': 'This time slot is already booked'}), 400
    
    appointment = Appointment(patient_id=patient.id, doctor_id=doctor_id, date=apt_date, 
                            time=apt_time, notes=data.get('notes'), status='booked')
    db.session.add(appointment)
    db.session.commit()
    cache.delete('admin_stats')
    return jsonify({'success': True, 'message': 'Appointment booked successfully', 'data': appointment.to_dict()}), 201

@patient_bp.route('/appointments/upcoming', methods=['GET'])
@patient_required
def get_upcoming_appointments():
    patient = get_current_patient()
    today = date.today()
    appointments = patient.appointments.filter(
        Appointment.date >= today, Appointment.status.in_(['booked', 'rescheduled'])
    ).order_by(Appointment.date, Appointment.time).all()
    return jsonify({'success': True, 'data': [apt.to_dict(include_doctor=True) for apt in appointments]}), 200

@patient_bp.route('/appointments/past', methods=['GET'])
@patient_required
def get_past_appointments():
    patient = get_current_patient()
    appointments = patient.appointments.filter_by(status='completed').order_by(Appointment.date.desc()).all()
    return jsonify({'success': True, 'data': [apt.to_dict(include_doctor=True, include_treatment=True) for apt in appointments]}), 200

@patient_bp.route('/appointments/<int:id>/cancel', methods=['PUT'])
@patient_required
def cancel_appointment(id):
    patient = get_current_patient()
    appointment = Appointment.query.filter_by(id=id, patient_id=patient.id).first_or_404()
    if appointment.status == 'completed':
        return jsonify({'success': False, 'error': 'Cannot cancel completed appointment'}), 400
    appointment.status = 'cancelled'
    appointment.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Appointment cancelled successfully', 'data': appointment.to_dict()}), 200

@patient_bp.route('/appointments/<int:id>/reschedule', methods=['PUT'])
@patient_required
def reschedule_appointment(id):
    patient = get_current_patient()
    appointment = Appointment.query.filter_by(id=id, patient_id=patient.id).first_or_404()
    
    if appointment.status not in ['booked', 'rescheduled']:
        return jsonify({'success': False, 'error': 'Cannot reschedule this appointment'}), 400
    
    data = request.get_json()
    required_fields = ['date', 'time']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields (date, time)'}), 400
    
    new_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    new_time = datetime.strptime(data['time'], '%H:%M').time()
    
    if new_date < date.today():
        return jsonify({'success': False, 'error': 'Appointment date must be in the future'}), 400
    
    # Check if the new slot is the same as current
    if appointment.date == new_date and appointment.time == new_time:
        return jsonify({'success': False, 'error': 'Please select a different date or time'}), 400
    
    # Check doctor availability for the new slot
    day_of_week = new_date.weekday()
    availability_slots = Availability.query.filter_by(
        doctor_id=appointment.doctor_id, 
        day_of_week=day_of_week, 
        is_available=True
    ).all()
    
    if not availability_slots:
        return jsonify({'success': False, 'error': 'Doctor is not available on this day'}), 400
    
    is_within_slot = any(slot.start_time <= new_time < slot.end_time for slot in availability_slots)
    if not is_within_slot:
        return jsonify({'success': False, 'error': 'Doctor is not available at this time'}), 400
    
    # Check for conflicts with other appointments (excluding current appointment)
    existing = Appointment.query.filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.date == new_date,
        Appointment.time == new_time,
        Appointment.status.in_(['booked', 'rescheduled']),
        Appointment.id != appointment.id
    ).first()
    
    if existing:
        return jsonify({'success': False, 'error': 'This time slot is already booked'}), 400
    
    # Update appointment
    appointment.date = new_date
    appointment.time = new_time
    appointment.status = 'rescheduled'
    appointment.updated_at = datetime.utcnow()
    
    db.session.commit()
    cache.delete('admin_stats')
    
    return jsonify({
        'success': True, 
        'message': 'Appointment rescheduled successfully', 
        'data': appointment.to_dict()
    }), 200

@patient_bp.route('/profile', methods=['GET'])
@patient_required
def get_profile():
    patient = get_current_patient()
    return jsonify({'success': True, 'data': patient.to_dict()}), 200

@patient_bp.route('/profile', methods=['PUT'])
@patient_required
def update_profile():
    patient = get_current_patient()
    data = request.get_json()
    patient.name = data.get('name', patient.name)
    patient.phone = data.get('phone', patient.phone)
    patient.address = data.get('address', patient.address)
    patient.blood_group = data.get('blood_group', patient.blood_group)
    patient.medical_history = data.get('medical_history', patient.medical_history)
    if data.get('date_of_birth'):
        patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Profile updated successfully', 'data': patient.to_dict()}), 200

@patient_bp.route('/export-treatments', methods=['POST'])
@patient_required
def export_treatments():
    patient = get_current_patient()
    from app.tasks.export import export_patient_treatments
    task = export_patient_treatments.delay(patient.id)
    return jsonify({'success': True, 'message': 'Export job started. You will be notified when complete.', 'data': {'task_id': task.id}}), 202

@patient_bp.route('/jobs/<task_id>/status', methods=['GET'])
@patient_required
def get_job_status(task_id):
    from app.celery_config import celery_app
    try:
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
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error checking job status: {str(e)}'}), 500

@patient_bp.route('/download-export/<filename>', methods=['GET'])
@patient_required
def download_export(filename):
    """Download exported CSV file"""
    import os
    
    patient = get_current_patient()
    
    # Security check - ensure filename belongs to current patient
    expected_prefix = f'treatments_{patient.name.replace(" ", "_")}_'
    if not filename.startswith(expected_prefix) or not filename.endswith('.csv'):
        return jsonify({'success': False, 'error': 'Invalid file access'}), 403
    
    exports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'exports')
    filepath = os.path.join(exports_dir, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': 'File not found or expired'}), 404
    
    try:
        return send_file(filepath, as_attachment=True, download_name=filename, mimetype='text/csv')
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error downloading file: {str(e)}'}), 500

@patient_bp.route('/treatments', methods=['GET'])
@patient_required
def get_treatment_history():
    """Get patient's treatment history"""
    patient = get_current_patient()
    
    # Get all completed appointments with treatments
    appointments = Appointment.query.filter_by(
        patient_id=patient.id, 
        status='completed'
    ).join(Treatment).order_by(Appointment.date.desc()).all()
    
    treatment_history = []
    for apt in appointments:
        treatment_data = {
            'id': apt.treatment.id,
            'appointment_id': apt.id,
            'date': apt.date.isoformat(),
            'time': apt.time.strftime('%H:%M'),
            'doctor': {
                'id': apt.doctor.id,
                'name': apt.doctor.name,
                'specialization': apt.doctor.specialization,
                'department': apt.doctor.department.name if apt.doctor.department else None
            },
            'treatment': apt.treatment.to_dict(),
            'appointment_notes': apt.notes
        }
        treatment_history.append(treatment_data)
    
    return jsonify({
        'success': True, 
        'data': {
            'patient': patient.to_dict(),
            'treatments': treatment_history,
            'total_treatments': len(treatment_history)
        }
    }), 200

@patient_bp.route('/treatments/<int:treatment_id>', methods=['GET'])
@patient_required
def get_treatment_detail(treatment_id):
    """Get detailed view of a specific treatment"""
    patient = get_current_patient()
    
    # Get treatment and verify it belongs to current patient
    treatment = Treatment.query.join(Appointment).filter(
        Treatment.id == treatment_id,
        Appointment.patient_id == patient.id
    ).first_or_404()
    
    appointment = treatment.appointment
    
    treatment_detail = {
        'id': treatment.id,
        'appointment_id': appointment.id,
        'date': appointment.date.isoformat(),
        'time': appointment.time.strftime('%H:%M'),
        'doctor': {
            'id': appointment.doctor.id,
            'name': appointment.doctor.name,
            'specialization': appointment.doctor.specialization,
            'department': appointment.doctor.department.name if appointment.doctor.department else None,
            'phone': appointment.doctor.phone,
            'years_of_experience': appointment.doctor.years_of_experience
        },
        'treatment': treatment.to_dict(),
        'appointment_notes': appointment.notes,
        'status': appointment.status
    }
    
    return jsonify({'success': True, 'data': treatment_detail}), 200

@patient_bp.route('/doctors/<int:doctor_id>/booked-slots', methods=['GET'])
@patient_required
def get_booked_slots(doctor_id):
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'success': False, 'error': 'Date parameter required'}), 400
    try:
        apt_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    booked_appointments = Appointment.query.filter_by(doctor_id=doctor_id, date=apt_date, status='booked').all()
    booked_times = [apt.time.strftime('%H:%M') for apt in booked_appointments]
    return jsonify({'success': True, 'data': {'date': date_str, 'booked_times': booked_times}}), 200

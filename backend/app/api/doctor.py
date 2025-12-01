from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import db
from app.models import Doctor, Appointment, Treatment, Availability, Patient
from app.api.decorators import doctor_required
from datetime import datetime, date

doctor_bp = Blueprint('doctor', __name__)

def get_current_doctor():
    user_id = int(get_jwt_identity())
    return Doctor.query.filter_by(user_id=user_id).first_or_404()

@doctor_bp.route('/stats', methods=['GET'])
@doctor_required
def get_stats():
    doctor = get_current_doctor()
    today = date.today()
    stats = {
        'total_appointments': doctor.appointments.count(),
        'today_appointments': doctor.appointments.filter_by(date=today).count(),
        'upcoming_appointments': doctor.appointments.filter(
            Appointment.date >= today, Appointment.status.in_(['booked', 'rescheduled'])
        ).count(),
        'completed_appointments': doctor.appointments.filter_by(status='completed').count(),
        'total_patients': db.session.query(Patient.id).join(Appointment).filter(
            Appointment.doctor_id == doctor.id
        ).distinct().count()
    }
    return jsonify({'success': True, 'data': stats}), 200

@doctor_bp.route('/appointments/today', methods=['GET'])
@doctor_required
def get_today_appointments():
    doctor = get_current_doctor()
    today = date.today()
    appointments = doctor.appointments.filter_by(date=today).order_by(Appointment.time).all()
    return jsonify({'success': True, 'data': [apt.to_dict(include_patient=True, include_treatment=True) for apt in appointments]}), 200

@doctor_bp.route('/appointments/upcoming', methods=['GET'])
@doctor_required
def get_upcoming_appointments():
    doctor = get_current_doctor()
    today = date.today()
    appointments = doctor.appointments.filter(
        Appointment.date >= today, Appointment.status.in_(['booked', 'rescheduled'])
    ).order_by(Appointment.date, Appointment.time).all()
    return jsonify({'success': True, 'data': [apt.to_dict(include_patient=True) for apt in appointments]}), 200

@doctor_bp.route('/appointments', methods=['GET'])
@doctor_required
def list_appointments():
    doctor = get_current_doctor()
    appointments = doctor.appointments.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return jsonify({'success': True, 'data': [apt.to_dict(include_patient=True, include_treatment=True) for apt in appointments]}), 200

@doctor_bp.route('/appointments/<int:id>/complete', methods=['PUT'])
@doctor_required
def complete_appointment(id):
    doctor = get_current_doctor()
    appointment = Appointment.query.filter_by(id=id, doctor_id=doctor.id).first_or_404()
    appointment.status = 'completed'
    appointment.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Appointment marked as completed', 'data': appointment.to_dict()}), 200

@doctor_bp.route('/appointments/<int:id>/cancel', methods=['PUT'])
@doctor_required
def cancel_appointment(id):
    doctor = get_current_doctor()
    appointment = Appointment.query.filter_by(id=id, doctor_id=doctor.id).first_or_404()
    appointment.status = 'cancelled'
    appointment.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Appointment cancelled', 'data': appointment.to_dict()}), 200

@doctor_bp.route('/appointments/<int:id>/treatment', methods=['POST'])
@doctor_required
def add_treatment(id):
    doctor = get_current_doctor()
    appointment = Appointment.query.filter_by(id=id, doctor_id=doctor.id).first_or_404()
    data = request.get_json()
    
    if not data.get('diagnosis'):
        return jsonify({'success': False, 'error': 'Diagnosis is required'}), 400
    
    if appointment.treatment:
        return jsonify({'success': False, 'error': 'Treatment record already exists for this appointment'}), 400
    
    treatment = Treatment(appointment_id=appointment.id, diagnosis=data['diagnosis'], 
                         prescription=data.get('prescription'), notes=data.get('notes'))
    appointment.status = 'completed'
    db.session.add(treatment)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Treatment record added successfully', 'data': treatment.to_dict()}), 201

@doctor_bp.route('/appointments/<int:id>/treatment', methods=['PUT'])
@doctor_required
def update_treatment(id):
    doctor = get_current_doctor()
    appointment = Appointment.query.filter_by(id=id, doctor_id=doctor.id).first_or_404()
    
    if not appointment.treatment:
        return jsonify({'success': False, 'error': 'No treatment record found for this appointment'}), 404
    
    data = request.get_json()
    if not data.get('diagnosis'):
        return jsonify({'success': False, 'error': 'Diagnosis is required'}), 400
    
    # Update treatment record
    treatment = appointment.treatment
    treatment.diagnosis = data['diagnosis']
    treatment.prescription = data.get('prescription')
    treatment.notes = data.get('notes')
    treatment.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Treatment record updated successfully', 'data': treatment.to_dict()}), 200

@doctor_bp.route('/patients/<int:id>/history', methods=['GET'])
@doctor_required
def get_patient_history(id):
    doctor = get_current_doctor()
    patient = Patient.query.get_or_404(id)
    appointments = Appointment.query.filter_by(patient_id=patient.id, doctor_id=doctor.id, status='completed').order_by(Appointment.date.desc()).all()
    return jsonify({
        'success': True,
        'data': {'patient': patient.to_dict(), 'appointments': [apt.to_dict(include_doctor=False, include_treatment=True) for apt in appointments]}
    }), 200

@doctor_bp.route('/availability', methods=['GET'])
@doctor_required
def get_availability():
    doctor = get_current_doctor()
    availability_slots = Availability.query.filter_by(doctor_id=doctor.id).all()
    by_day = {}
    for slot in availability_slots:
        day = slot.day_of_week
        if day not in by_day:
            by_day[day] = []
        by_day[day].append(slot.to_dict())
    return jsonify({'success': True, 'data': by_day}), 200

@doctor_bp.route('/availability', methods=['POST'])
@doctor_required
def add_availability():
    doctor = get_current_doctor()
    data = request.get_json()
    required_fields = ['day_of_week', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    availability = Availability(
        doctor_id=doctor.id, day_of_week=data['day_of_week'],
        start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
        end_time=datetime.strptime(data['end_time'], '%H:%M').time(), is_available=True
    )
    db.session.add(availability)
    db.session.commit()
    
    from app import cache
    cache.delete(f'doctor_availability_{doctor.id}')
    cache.delete(f'doctor_detail_{doctor.id}')
    return jsonify({'success': True, 'message': 'Availability slot added', 'data': availability.to_dict()}), 201

@doctor_bp.route('/availability/<int:id>', methods=['DELETE'])
@doctor_required
def delete_availability(id):
    doctor = get_current_doctor()
    slot = Availability.query.filter_by(id=id, doctor_id=doctor.id).first_or_404()
    db.session.delete(slot)
    db.session.commit()
    
    from app import cache
    cache.delete(f'doctor_availability_{doctor.id}')
    cache.delete(f'doctor_detail_{doctor.id}')
    return jsonify({'success': True, 'message': 'Availability slot deleted'}), 200

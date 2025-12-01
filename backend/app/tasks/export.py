from app.celery_config import celery_app
import csv, requests, json, os
from datetime import datetime

EXPORTS_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQAS6ohpE0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=KkhQn8lqoWzMJ4S5_ZEselBOwwfHCFLMIQuXVATkeUA"

@celery_app.task(bind=True, name='app.tasks.export.export_patient_treatments')
def export_patient_treatments(self, patient_id):
    from app import create_app
    from app.models import Patient, Appointment
    
    app = create_app()
    with app.app_context():
        patient = Patient.query.get(patient_id)
        if not patient:
            try:
                payload = {"text": f"❌ *CSV Export Failed*\n\nPatient with ID {patient_id} not found.\n\n🏥 PatchMeUp Hospital"}
                requests.post(EXPORTS_WEBHOOK_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=10)
            except:
                pass
            return {'status': 'error', 'message': 'Patient not found'}
        
        appointments = Appointment.query.filter_by(patient_id=patient_id, status='completed').order_by(Appointment.date.desc()).all()
        appointments_with_treatment = [apt for apt in appointments if apt.treatment]
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'treatments_{patient.name.replace(" ", "_")}_{timestamp}.csv'
        
        # Create exports directory if it doesn't exist
        exports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'exports')
        os.makedirs(exports_dir, exist_ok=True)
        filepath = os.path.join(exports_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User ID', 'Username', 'Appointment Date', 'Time', 'Consulting Doctor', 'Department', 
                               'Specialization', 'Diagnosis', 'Treatment Given', 'Prescription', 'Treatment Notes', 'Next Visit Suggested'])
                
                for apt in appointments_with_treatment:
                    writer.writerow([patient.user_id, patient.name, apt.date.strftime('%Y-%m-%d'), apt.time.strftime('%H:%M'),
                                   apt.doctor.name, apt.doctor.department.name if apt.doctor.department else 'N/A',
                                   apt.doctor.specialization, apt.treatment.diagnosis, apt.treatment.diagnosis,
                                   apt.treatment.prescription or 'N/A', apt.treatment.notes or 'N/A', 'As per doctor\'s advice'])
            
            csv_preview = []
            if appointments_with_treatment:
                for apt in appointments_with_treatment[:3]:
                    csv_preview.append({
                        'date': apt.date.strftime('%b %d, %Y'),
                        'doctor': apt.doctor.name,
                        'diagnosis': apt.treatment.diagnosis[:50] + '...' if len(apt.treatment.diagnosis) > 50 else apt.treatment.diagnosis
                    })
            
            message_text = f"✅ *CSV Export Completed*\n\n👤 *Patient:* {patient.name}\n📧 *Email:* {patient.user.email}\n"
            message_text += f"📊 *Records Exported:* {len(appointments_with_treatment)}\n📁 *File:* {filename}\n"
            message_text += f"⏰ *Generated:* {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n"
            
            if csv_preview:
                message_text += f"📋 *Preview of exported data:*\n"
                for i, record in enumerate(csv_preview, 1):
                    message_text += f"{i}. {record['date']} - Dr. {record['doctor']}\n   Diagnosis: {record['diagnosis']}\n"
                if len(appointments_with_treatment) > 3:
                    message_text += f"   ... and {len(appointments_with_treatment) - 3} more records\n"
            else:
                message_text += "📋 No treatment records found for this patient.\n"
            
            message_text += f"\n💾 CSV file has been generated and stored.\n🏥 PatchMeUp Hospital"
            
            try:
                response = requests.post(EXPORTS_WEBHOOK_URL, headers={'Content-Type': 'application/json'}, 
                                       data=json.dumps({"text": message_text}), timeout=10)
                if response.status_code == 200:
                    print(f"Successfully sent CSV export notification to Google Chat for patient {patient.name}")
                else:
                    print(f"Failed to send CSV export notification. Status: {response.status_code}")
            except Exception as e:
                print(f"Error sending CSV export notification to Google Chat: {str(e)}")
            
            # Don't delete the file - keep it for download
            return {'status': 'completed', 'patient_id': patient_id, 'patient_name': patient.name,
                   'records_exported': len(appointments_with_treatment), 'filename': filename, 
                   'filepath': filepath, 'notification_method': 'google_chat'}
            
        except Exception as e:
            try:
                payload = {"text": f"❌ *CSV Export Failed*\n\n👤 Patient: {patient.name}\n📧 Email: {patient.user.email}\n🚫 Error: {str(e)}\n\n🏥 PatchMeUp Hospital"}
                requests.post(EXPORTS_WEBHOOK_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=10)
            except:
                pass
            return {'status': 'error', 'message': str(e), 'patient_id': patient_id}

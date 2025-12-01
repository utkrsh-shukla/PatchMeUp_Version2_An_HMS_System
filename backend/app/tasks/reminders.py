from app.celery_config import celery_app
from datetime import date
import requests, json

REMINDERS_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQAS6ohpE0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=c_8jGkZCcpdnhZ911atEJsL1mhQ_Hgum1iP1swgDBh8"

@celery_app.task(name='app.tasks.reminders.send_daily_reminders')
def send_daily_reminders():
    from app import create_app
    from app.models import Appointment
    
    app = create_app()
    with app.app_context():
        today = date.today()
        appointments = Appointment.query.filter_by(date=today, status='booked').all()
        sent_count = 0
        
        if appointments:
            appointment_details = []
            for appointment in appointments:
                appointment_details.append({
                    'patient': appointment.patient.name, 'doctor': appointment.doctor.name,
                    'specialization': appointment.doctor.specialization, 'time': appointment.time.strftime('%I:%M %p'),
                    'notes': appointment.notes or 'No special notes'
                })
            
            message_text = f"🏥 *Daily Appointment Reminders - {today.strftime('%B %d, %Y')}*\n\n📅 *{len(appointments)} appointments scheduled for today:*\n\n"
            for i, apt in enumerate(appointment_details, 1):
                message_text += f"*{i}. {apt['patient']}*\n   👨‍⚕️ Doctor: {apt['doctor']} ({apt['specialization']})\n   ⏰ Time: {apt['time']}\n   📝 Notes: {apt['notes']}\n\n"
            message_text += "⚠️ *Reminder: Patients should arrive 10 minutes before their scheduled time.*\n🏥 PatchMeUp Hospital - Your Health, Our Priority"
            
            try:
                response = requests.post(REMINDERS_WEBHOOK_URL, headers={'Content-Type': 'application/json'}, 
                                       data=json.dumps({"text": message_text}), timeout=10)
                if response.status_code == 200:
                    sent_count = len(appointments)
                    print(f"Successfully sent daily reminders to Google Chat for {sent_count} appointments")
                else:
                    print(f"Failed to send to Google Chat. Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                print(f"Error sending reminder to Google Chat: {str(e)}")
        else:
            try:
                payload = {"text": f"🏥 *Daily Appointment Reminders - {today.strftime('%B %d, %Y')}*\n\n✅ No appointments scheduled for today.\n\n🏥 PatchMeUp Hospital"}
                response = requests.post(REMINDERS_WEBHOOK_URL, headers={'Content-Type': 'application/json'}, 
                                       data=json.dumps(payload), timeout=10)
                if response.status_code == 200:
                    print("Successfully sent 'no appointments' message to Google Chat")
            except Exception as e:
                print(f"Error sending 'no appointments' message to Google Chat: {str(e)}")
        
        return {'status': 'completed', 'date': today.isoformat(), 'total_appointments': len(appointments),
               'reminders_sent': sent_count, 'notification_method': 'google_chat'}

from app.celery_config import celery_app
from datetime import datetime, timedelta
import requests, json

REPORTS_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQAS6ohpE0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=LN32M3WbXY0uke38HWshleCGKSleHB79SkquQvRW14U"

@celery_app.task(name='app.tasks.reports.generate_monthly_reports')
def generate_monthly_reports():
    from app import create_app
    from app.models import Doctor, Appointment
    
    app = create_app()
    with app.app_context():
        today = datetime.now()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        
        doctors = Doctor.query.join(Doctor.user).filter(Doctor.user.has(is_active=True)).all()
        report_data = []
        total_system_appointments = total_system_completed = total_system_cancelled = 0
        
        for doctor in doctors:
            appointments = Appointment.query.filter(
                Appointment.doctor_id == doctor.id, Appointment.date >= first_day_last_month.date(),
                Appointment.date <= last_day_last_month.date()
            ).all()
            
            total_appointments = len(appointments)
            completed = len([a for a in appointments if a.status == 'completed'])
            cancelled = len([a for a in appointments if a.status == 'cancelled'])
            
            treatments = []
            for apt in appointments:
                if apt.status == 'completed' and apt.treatment:
                    treatments.append({
                        'patient': apt.patient.name, 'date': apt.date.strftime('%b %d'),
                        'diagnosis': apt.treatment.diagnosis[:50] + '...' if len(apt.treatment.diagnosis) > 50 else apt.treatment.diagnosis,
                        'prescription': apt.treatment.prescription[:50] + '...' if apt.treatment.prescription and len(apt.treatment.prescription) > 50 else (apt.treatment.prescription or 'N/A')
                    })
            
            report_data.append({'doctor': doctor, 'total': total_appointments, 'completed': completed, 
                              'cancelled': cancelled, 'treatments': treatments[:5]})
            
            total_system_appointments += total_appointments
            total_system_completed += completed
            total_system_cancelled += cancelled
        
        month_name = last_day_last_month.strftime('%B %Y')
        message_text = f"📊 *Monthly Activity Report - {month_name}*\n\n🏥 *Hospital Overview:*\n"
        message_text += f"   📅 Total Appointments: {total_system_appointments}\n   ✅ Completed: {total_system_completed}\n   ❌ Cancelled: {total_system_cancelled}\n"
        message_text += f"   📈 Success Rate: {(total_system_completed/total_system_appointments*100):.1f}%\n\n" if total_system_appointments > 0 else "   📈 Success Rate: 0%\n\n"
        
        message_text += f"👨‍⚕️ *Doctor Performance:*\n\n"
        for data in report_data:
            if data['total'] > 0:
                doctor = data['doctor']
                message_text += f"*Dr. {doctor.name}* ({doctor.specialization})\n   📊 {data['total']} total | ✅ {data['completed']} completed | ❌ {data['cancelled']} cancelled\n"
                if data['treatments']:
                    message_text += f"   🔬 Recent Treatments:\n"
                    for treatment in data['treatments']:
                        message_text += f"      • {treatment['patient']} ({treatment['date']}): {treatment['diagnosis']}\n"
                message_text += "\n"
        
        if total_system_appointments == 0:
            message_text += "No appointments recorded for this month.\n\n"
        
        message_text += f"📋 *Report generated on:* {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n🏥 PatchMeUp Hospital Management System"
        
        sent_count = 0
        try:
            response = requests.post(REPORTS_WEBHOOK_URL, headers={'Content-Type': 'application/json'}, 
                                   data=json.dumps({"text": message_text}), timeout=10)
            if response.status_code == 200:
                sent_count = 1
                print(f"Successfully sent monthly report to Google Chat for {month_name}")
            else:
                print(f"Failed to send monthly report to Google Chat. Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error sending monthly report to Google Chat: {str(e)}")
        
        return {'status': 'completed', 'month': month_name, 'reports_sent': sent_count, 'total_doctors': len(doctors),
               'total_appointments': total_system_appointments, 'notification_method': 'google_chat'}

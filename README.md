# Hospital Management System V2

## S Grade (10 Grade Point) Capstone Project For Modern Application Development - 2 Course Under IIT Madras
<img width="406" height="448" alt="image" src="https://github.com/user-attachments/assets/e549e56e-7564-42bf-bc2f-2a761271687b" />


## 🏥 Overview

A comprehensive hospital management system built with modern web technologies, featuring role-based access control, appointment scheduling, automated job processing, and real-time notifications via Google Chat.

## ✨ Key Features

### 🔐 **User Management**
- **Multi-role Authentication**: Admin, Doctor, and Patient roles
- **JWT Security**: Token-based authentication with role-based access control
- **Profile Management**: Comprehensive user profile management

### 📅 **Appointment System**
- **Smart Booking**: Patients can browse doctors and book appointments
- **Availability Management**: Doctors can set their weekly availability
- **Status Tracking**: Real-time appointment status updates
- **Treatment Records**: Complete medical history tracking

### 🤖 **Automated Jobs (Celery + Redis)**
- **Daily Reminders**: Automatic appointment reminders at 8:00 AM
- **Monthly Reports**: Comprehensive activity reports on 1st of each month
- **CSV Export**: On-demand patient treatment history export
- **Google Chat Integration**: Real-time notifications for all jobs

### 📊 **Dashboard Features**
- **Admin Dashboard**: System statistics, user management, job monitoring
- **Doctor Dashboard**: Appointment management, patient records, performance metrics
- **Patient Dashboard**: Doctor browsing, appointment history, profile management

## 🛠 Technology Stack

### **Backend**
- **Framework**: Flask (Python)
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-JWT-Extended
- **Job Queue**: Celery with Redis
- **Caching**: Redis
- **API**: RESTful API design

### **Frontend**
- **Framework**: Vue.js 3 (Composition API)
- **State Management**: Vuex
- **Routing**: Vue Router
- **UI Framework**: Bootstrap 5
- **HTTP Client**: Axios
- **Build Tool**: Vite

### **Infrastructure**
- **Message Broker**: Redis
- **Task Queue**: Celery
- **Notifications**: Google Chat Webhooks
- **Containerization**: Docker & Docker Compose

## 🚀 Quick Start

### **Prerequisites**
- Python 3.11+
- Node.js 16+
- Redis Server

### **1. Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python init_db.py

# Verify setup (optional but recommended)
python verify_setup.py

# Start the API server
python run.py
```

### **2. Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

### **3. Celery Jobs Setup (For Background Tasks)**

#### Prerequisites
Make sure Docker Desktop is installed and running.

#### Step 1: Start Redis with Docker
```bash
docker run -d -p 6379:6379 redis:alpine
```

#### Step 2: Start Celery Worker
Open a new terminal in the `backend` directory:
```bash
cd backend

# Windows
celery -A celery_worker.celery_app worker --loglevel=info --pool=solo

# Linux/Mac
celery -A celery_worker.celery_app worker --loglevel=info
```

#### Step 3: Start Celery Beat (Required for scheduled jobs)
Open another terminal in the `backend` directory:
```bash
cd backend
celery -A celery_worker.celery_app beat --loglevel=info
```

> **Note:** Celery Beat is required for automatic daily reminders (8:00 AM) and monthly reports (1st of each month at 9:00 AM). Without it, scheduled jobs won't run.

## 🔑 Default Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@hospital.com | admin123 |


## 📱 Application URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5173/admin/dashboard
- **Doctor Dashboard**: http://localhost:5173/doctor/dashboard
- **Patient Dashboard**: http://localhost:5173/patient/dashboard

## 🎯 Core Workflows

### **For Patients**
1. Register/Login → Browse Doctors → Book Appointment → View History → Export Records

### **For Doctors**
1. Login → Set Availability → Manage Appointments → Add Treatments → View Reports

### **For Admins**
1. Login → Monitor System → Manage Users → Trigger Jobs 

## 🔧 Advanced Features

### **Automated Job System**
- **Daily Reminders**: Sends Google Chat notifications for same-day appointments
- **Monthly Reports**: Generates comprehensive doctor performance reports
- **CSV Export**: Asynchronous export of patient treatment history
- **Real-time Monitoring**: Live job status tracking via admin interface

### **Google Chat Integration**
All system notifications are sent to Google Chat with rich formatting:
- Appointment reminders with patient details
- Monthly reports with statistics and charts
- Export completion notifications with data previews

## 📁 Project Structure

```
HMS_V2/
├── backend/           # Flask API server
├── frontend/          # Vue.js application           
└── README.md          # This file
```

## 📚 Documentation

- **Setup Guide**: `PROJECT_SETUP.md`
- **Features**: `FEATURES.md`
- **Submission Guide**: `PROJECT_SUBMISSION_GUIDE.md`
- **Celery Jobs**: `extras/documentation/GOOGLE_CHAT_WEBHOOKS.md`

## 🧪 Testing

The system includes comprehensive testing scripts in the `extras/testing/` folder:
- Webhook testing
- Job execution testing
- API endpoint testing


## 🎉 Production Ready

This system is production-ready with:
- ✅ Comprehensive error handling
- ✅ Security best practices
- ✅ Scalable architecture
- ✅ Real-time job processing
- ✅ Professional UI/UX
- ✅ Complete documentation

## 📞 Support

**Quick Help**:
1. Run `python backend/verify_setup.py` to check your setup
2. Check `backend/TROUBLESHOOTING.md` for common issues
3. Review documentation in the `extras/` folder

**Common Issues**:
- **Celery won't start**: Make sure Redis is running (`docker run -d -p 6379:6379 redis:alpine`)
- **401 errors**: Normal behavior - tokens auto-refresh
- **Database errors**: Run `python init_db.py`

---




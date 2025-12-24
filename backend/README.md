# Hospital Management System V2 - Backend

Flask-based REST API for Hospital Management System with JWT authentication, Redis caching, and Celery background jobs.

## Features

- **RESTful API** with JWT authentication
- **Role-based access control** (Admin, Doctor, Patient)
- **Redis caching** for performance optimization
- **Background jobs** with Celery:
  - Daily appointment reminders
  - Monthly doctor reports
  - CSV export of patient treatments

## Requirements

- Python 3.8+
- Redis Server
- SQLite

## Installation

1. **Clone and navigate to backend directory:**
```bash
cd v2/backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database:**
```bash
python init_db.py
```

## Running the Application

### 1. Start Redis Server

**Option A: Using Docker (Recommended)**
```bash
docker run -d -p 6379:6379 redis:alpine
```

**Option B: Using native Redis installation**
```bash
redis-server
```

### 2. Start Flask API
```bash
python run.py
```
API will be available at `http://localhost:5000`

### 3. Start Celery Worker

Open a new terminal in the `backend` directory:

**Windows:**
```bash
celery -A celery_worker.celery_app worker --loglevel=info --pool=solo
```

**Linux/Mac:**
```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

### 4. Start Celery Beat (Required for scheduled tasks)

Open another terminal in the `backend` directory:
```bash
celery -A celery_worker.celery_app beat --loglevel=info
```

> **Note:** Celery Beat is required for automatic scheduled jobs:
> - **Daily Reminders**: Runs at 8:00 AM daily
> - **Monthly Reports**: Runs on 1st of each month at 9:00 AM
> 
> Without Celery Beat running, these scheduled jobs will not execute.

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Patient registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token
- `GET /api/auth/me` - Get current user

### Admin Endpoints
- `GET /api/admin/stats` - Dashboard statistics
- `GET /api/admin/doctors` - List doctors
- `POST /api/admin/doctors` - Create doctor
- `PUT /api/admin/doctors/<id>` - Update doctor
- `DELETE /api/admin/doctors/<id>` - Deactivate doctor
- `GET /api/admin/patients` - List patients
- `GET /api/admin/search?q=<query>&type=<type>` - Search

### Doctor Endpoints
- `GET /api/doctor/stats` - Dashboard stats
- `GET /api/doctor/appointments/today` - Today's appointments
- `POST /api/doctor/appointments/<id>/treatment` - Add treatment
- `GET /api/doctor/availability` - Get availability
- `POST /api/doctor/availability` - Add availability slot

### Patient Endpoints
- `GET /api/patient/departments` - List departments
- `GET /api/patient/doctors` - List doctors
- `POST /api/patient/appointments` - Book appointment
- `GET /api/patient/profile` - Get profile
- `POST /api/patient/export-treatments` - Export CSV

## Default Credentials

- **Admin**: admin@hospital.com / admin123

## Background Jobs

1. **Daily Reminders** - Runs at 8:00 AM daily
2. **Monthly Reports** - Runs on 1st of each month at 9:00 AM
3. **CSV Export** - User-triggered asynchronous job

## Caching Strategy

- Dashboard stats: 5 minutes
- Department list: 24 hours
- Doctor availability: 1 hour

Cache is automatically invalidated on data updates.

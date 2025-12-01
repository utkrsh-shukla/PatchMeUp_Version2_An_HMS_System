"""Models package for HMS V2"""

from app.models.user import User
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.treatment import Treatment
from app.models.availability import Availability

__all__ = [
    'User',
    'Department',
    'Doctor',
    'Patient',
    'Appointment',
    'Treatment',
    'Availability'
]

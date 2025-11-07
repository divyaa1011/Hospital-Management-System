"""Simple CRUD helpers (SQLAlchemy)."""

from typing import List, Dict
from .db import db
from .models import Patient
from .exceptions import PatientNotFound

def create_patient(data: Dict) -> Patient:
    patient = Patient(name=data["name"], age=int(data["age"]), disease=data["disease"])
    db.session.add(patient)
    db.session.commit()
    return patient

def get_all_patients() -> List[Patient]:
    return Patient.query.order_by(Patient.id).all()

def get_patient(patient_id: int) -> Patient:
    patient = Patient.query.get(patient_id)
    if not patient:
        raise PatientNotFound(f"Patient {patient_id} not found")
    return patient

def update_patient(patient_id: int, data: Dict) -> Patient:
    patient = get_patient(patient_id)
    if "name" in data:
        patient.name = data["name"]
    if "age" in data:
        patient.age = int(data["age"])
    if "disease" in data:
        patient.disease = data["disease"]
    db.session.commit()
    return patient

def delete_patient(patient_id: int) -> None:
    patient = get_patient(patient_id)
    db.session.delete(patient)
    db.session.commit()

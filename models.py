from app import db
from marshmallow import Schema, fields, validate
import datetime

class PatientSchema(Schema):
    face_id = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    dob = fields.Date(required=True)
    gender = fields.String(required=True, validate=validate.OneOf(["Male", "Female"]))

class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    face_id = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String, nullable=False)
    contact_info = db.Column(db.String)
    address = db.Column(db.Text)
    medical_history = db.Column(db.Text)

    # Relationships (if needed)
    visits = db.relationship('Visit', backref='patient', lazy=True)

class FacialData(db.Model):
    face_id = db.Column(db.String, primary_key=True)
    encoding = db.Column(db.LargeBinary)
    image = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Visit(db.Model):
    visit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    visit_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    doctor_id = db.Column(db.Integer)

    # Relationships (if needed)
    patient = db.relationship('Patient', backref='visits', lazy=True)

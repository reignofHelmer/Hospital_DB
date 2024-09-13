from flask import Flask, request, jsonify
import numpy as np
from facial_recog import capture_and_encode_face
from flask_sqlalchemy import SQLAlchemy
from config import Config
import face_recognition
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.config['JWT_SECRET_KEY'] = 'ebdb6af4a5834a2157e5e35aa6dc2c5cc52b3fcc84c0b4fe6225ae7c3651265b'
jwt = JWTManager(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Create a login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # Authenticate user (add real authentication logic here)
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

# Create error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Define your models
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
    face_encoding = db.Column(db.LargeBinary)  # Store face encoding as binary data

@app.route('/')
def index():
    return "Welcome to the Facial Recognition API!"

@app.route('/add_patient', methods=['POST'])
@jwt_required()  # Require JWT for this endpoint
def add_patient():
    data = request.json
    encoding = capture_and_encode_face()  # Use the function without importing db here

    if not encoding:
        return jsonify({"message": "No face detected."}), 400

    encoding_bytes = np.array(encoding).tobytes()  # Save face encoding as bytes

    new_patient = Patient(
        face_id=data['face_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=data['dob'],
        gender=data['gender'],
        contact_info=data.get('contact_info'),
        address=data.get('address'),
        medical_history=data.get('medical_history'),
        face_encoding=encoding_bytes
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient added successfully"}), 201

@app.route('/get_patients', methods=['GET'])
@jwt_required()  # Require JWT for this endpoint
def get_patients():
    patients = Patient.query.all()
    return jsonify([{
        "patient_id": p.patient_id,
        "face_id": p.face_id,
        "first_name": p.first_name,
        "last_name": p.last_name,
        "dob": p.dob,
        "gender": p.gender,
        "contact_info": p.contact_info,
        "address": p.address,
        "medical_history": p.medical_history
    } for p in patients])

@app.route('/authenticate', methods=['POST'])
@jwt_required()  # Require JWT for this endpoint
def authenticate():
    file = request.files['image']
    image = face_recognition.load_image_file(file)
    image_encoding = face_recognition.face_encodings(image)

    if not image_encoding:
        return jsonify({"message": "No face detected"}), 400

    encoding_to_match = image_encoding[0]

    # Retrieve all patients and compare their encodings
    patients = Patient.query.all()
    for patient in patients:
        stored_encoding = np.frombuffer(patient.face_encoding, dtype=np.float64)
        matches = face_recognition.compare_faces([stored_encoding], encoding_to_match)

        if True in matches:
            return jsonify({"message": f"Authenticated {patient.first_name} {patient.last_name}"}), 200

    return jsonify({"message": "No match found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

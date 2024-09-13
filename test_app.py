import pytest
from app import app, db  # Make sure to import your Flask app and database

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all tables
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_add_patient(client):
    response = client.post('/add_patient', json={
        "face_id": "test123",
        "first_name": "John",
        "last_name": "Doe",
        "dob": "1990-01-01",
        "gender": "Male"
    })
    assert response.status_code == 201
    assert response.json == {"message": "Patient added successfully"}

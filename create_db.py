from app import app, db
import os
from cryptography.fernet import Fernet

def generate_key():
    # Generate a new key and print it; store this key securely
    key = Fernet.generate_key()
    print(f"Generated Key: {key.decode()}")
    # Save this key securely and load it in your application configuration
    return key

def load_key():
    # Load the key from an environment variable or a secure location
    key = os.getenv('ENCRYPTION_KEY')  # Ensure this environment variable is set
    if not key:
        raise ValueError("Encryption key not found. Set the ENCRYPTION_KEY environment variable.")
    return key.encode()

def encrypt_encoding(encoding):
    key = load_key()  # Load the key from the environment variable
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(encoding.tobytes())

# Create database and tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

# Optional: Generate and print a new key (run this separately if you need to generate a new key)
# generate_key()

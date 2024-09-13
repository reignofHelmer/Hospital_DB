import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:wXcYRBVkjcEEJbiSuVwDWIRzKGhIcVze@autorack.proxy.rlwy.net:21682/railway'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # Securely set your key
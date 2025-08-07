# config.py
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"  # change to MySQL if needed
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://simulator:DBsimUl4tor;@10.245.16.16:3306/simulator'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 7))
    )
    JWT_COOKIE_SECURE = False # True jika pakai HTTPS
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_ACCESS_COOKIE_NAME = 'access_token'     # ini tidak akan dipakai karena access_token dari header
    JWT_REFRESH_COOKIE_NAME = 'refresh_token'
    
    # Set CORS origins based on environment
    # Local development: port 4200, Docker production: port 4242
    if os.getenv('FLASK_ENV') == 'production':
        CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:4242,http://127.0.0.1:4242')
    else:
        CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:4200,http://127.0.0.1:4200')
# config.py
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment-specific .env file
# Check if FLASK_ENV is already set (e.g., by Docker)
flask_env = os.getenv('FLASK_ENV', 'development')

if flask_env == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

class Config:
    # SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"  # change to MySQL if needed
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://simulator:DBsimUl4tor;@10.245.16.16:3306/simulator'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'echo': True
    # }
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
    
    # CORS origins are now loaded directly from the environment-specific .env file
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
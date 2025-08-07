# config.py
from datetime import timedelta

class Config:
    # SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"  # change to MySQL if needed
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://simulator:DBsimUl4tor;@10.245.16.16:3306/simulator'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-930702274-analis3'
    JWT_SECRET_KEY = 'your-super-secret-jwt-key-930702274-analis3'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # optional
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)  # optional
    JWT_COOKIE_SECURE = False # True jika pakai HTTPS
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_ACCESS_COOKIE_NAME = 'access_token'     # ini tidak akan dipakai karena access_token dari header
    JWT_REFRESH_COOKIE_NAME = 'refresh_token'
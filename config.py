# config.py
from datetime import timedelta

class Config:
    # SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"  # change to MySQL if needed
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://simulator:DBsimUl4tor;@10.245.16.16:3306/simulator'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-930702274-analis3'
    JWT_SECRET_KEY = 'your-super-secret-jwt-key-930702274-analis3'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)  # optional


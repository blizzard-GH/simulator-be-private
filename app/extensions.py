from flask_jwt_extended import JWTManager
from flask_cors import CORS

jwt = JWTManager()
cors = CORS()

# def init_cors(app):
#     CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)

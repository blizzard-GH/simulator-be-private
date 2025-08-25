# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS
from .extensions import jwt, cors


db = SQLAlchemy()

# from app.routes.user_routes import user_test_bp
from app.routes.returnsheet_grid_routes import returnsheet_grid_bp
from app.routes.returnsheet_form_data_routes import returnsheet_form_data_bp
from app.routes.l3_other_parties_routes import l3_other_parties_bp
from app.routes.l4_income_subject_to_final_routes import l4_income_subject_to_final_bp
from app.routes.l9_tangible_asset_routes import l9_tangible_asset_bp
from app.routes.l9_intangible_asset_routes import l9_intangible_asset_bp
from app.routes.l9_group_of_building_routes import l9_group_of_building_bp
from app.routes.auth_routes import auth_bp
from app.routes.app_user_routes import app_user_bp
from app.routes.returnsheet_routes import returnsheet_bp
from elasticapm.contrib.flask import ElasticAPM   # 👈 import APM

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    origins = app.config['CORS_ORIGINS']
    if isinstance(origins, str):
        origins = [o.strip() for o in origins.split(',')]

    CORS(app, origins=origins, supports_credentials=True)
    # cors.init_app(app, supports_credentials=True, origins=["http://127.0.0.1:4200"])
    # cors.init_app(app,
    #           supports_credentials=True,
    #           origins=['http://127.0.0.1:4200'],
    #           resources={r"/api/*": {"origins": "http://127.0.0.1:4200"}})

    # for docker
    # cors.init_app(app,
    #           supports_credentials=True,
    #           origins=['http://127.0.0.1:4242'],
    #           resources={r"/api/*": {"origins": "http://127.0.0.1:4242"}})
    
    app.register_blueprint(returnsheet_grid_bp)
    app.register_blueprint(returnsheet_form_data_bp)
    app.register_blueprint(l3_other_parties_bp)
    app.register_blueprint(l4_income_subject_to_final_bp)
    app.register_blueprint(l9_tangible_asset_bp)
    app.register_blueprint(l9_intangible_asset_bp)
    app.register_blueprint(l9_group_of_building_bp)
    app.register_blueprint(auth_bp)  # 🔐 JWT login
    app.register_blueprint(app_user_bp)
    app.register_blueprint(returnsheet_bp)
    with app.app_context():
        db.create_all()

    # --- Elastic APM init ---
    if getattr(Config, "ELASTIC_APM_ENABLED", False):
        app.config['ELASTIC_APM'] = {
            'SERVICE_NAME': 'python-backend',
            'SERVER_URL': Config.ELASTIC_APM_SERVER_URL,
            # 'SERVER_URL': getattr(Config, "ELASTIC_APM_SERVER_URL", "http://apm-server:8200"),
            'SECRET_TOKEN': Config.ELASTIC_APM_SECRET_TOKEN,  # if you enable auth in apm-server
            # 'SECRET_TOKEN': getattr(Config, "ELASTIC_APM_SECRET_TOKEN", ""),  # if you enable auth in apm-server
            'ENVIRONMENT': getattr(Config, "ENV", "development"),
            # 'ENVIRONMENT': getattr(Config, "ENV", "development"),
            'ENVIRONMENT': Config.ENV,
            'CAPTURE_HEADERS': True,
            'TRANSACTION_SAMPLE_RATE': Config.ELASTIC_APM_SAMPLE_RATE,  # 👈 here
        }
        global apm
        apm = ElasticAPM(app)

    return app

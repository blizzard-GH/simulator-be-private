# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS

db = SQLAlchemy()

from app.routes.user_routes import user_bp
from app.routes.returnsheet_grid_routes import returnsheet_grid_bp
from app.routes.returnsheet_form_data_routes import returnsheet_form_data_bp
from app.routes.l3_other_parties_routes import l3_other_parties_bp
from app.routes.l4_income_subject_to_final_routes import l4_income_subject_to_final_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Allow all origins (for dev only)
    CORS(app)

    # from .routes.user_routes import user_bp
    # app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(user_bp)
    app.register_blueprint(returnsheet_grid_bp)
    app.register_blueprint(returnsheet_form_data_bp)
    app.register_blueprint(l3_other_parties_bp)
    app.register_blueprint(l4_income_subject_to_final_bp)

    with app.app_context():
        db.create_all()

    return app

import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT, TIMESTAMP
from sqlalchemy import text, DECIMAL, String
from app import db

class RSReturnsheetFormData(db.Model):
    __tablename__ = 'RS_RETURNSHEET_FORM_DATA'

    z_record_id = db.Column(String(55), primary_key=True)
    z_aggregate_identifier = db.Column(String(55))
    z_aggregate_version = db.Column(DECIMAL(19, 0))
    z_return_sheet_version_code = db.Column(String(50))
    z_form_data = db.Column(LONGTEXT)
    z_last_updated_date = db.Column(
        TIMESTAMP(fsp=6),
        nullable=False,
        server_default=text('current_timestamp(6) ON UPDATE current_timestamp(6)')
    )
    z_is_migrated = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_is_migrated_and_updated = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_creation_date = db.Column(
        TIMESTAMP(fsp=6),
        nullable=False,
        server_default=text('current_timestamp(6)')
    )

    def get_main_form_data(self):
        try:
            data = json.loads(self.z_form_data or '{}')
            return data.get('MainFormData', {})
        except json.JSONDecodeError:
            return {}
        
    @property
    def form_data(self):
        return json.loads(self.z_form_data) if self.z_form_data else {}

    @form_data.setter
    def form_data(self, value):
        self.z_form_data = json.dumps(value)

    def get_main_form_value(self, key, default=None):
        """Get a value from MainFormData safely"""
        return self.form_data.get("MainFormData", {}).get(key, default)

        
    def set_main_form_value(self, key, value):
        """Set a value inside MainFormData (create MainFormData if missing)"""
        data = self.form_data
        if "MainFormData" not in data:
            data["MainFormData"] = {}
        data["MainFormData"][key] = value
        self.form_data = data

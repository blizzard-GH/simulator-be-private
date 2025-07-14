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

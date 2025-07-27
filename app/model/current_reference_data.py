from sqlalchemy import Index, String, text
from sqlalchemy.dialects.mysql import BIGINT
from app import db

class CurrentReferenceData(db.Model):
    __tablename__ = 'CURRENT_REFERENCE_DATA'

    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='ID')
    reference_data_type = db.Column(db.String(200), nullable=False, comment='Tipe Data Referensi')
    code = db.Column(db.String(500), nullable=False, comment='Kode Data Referensi')
    code_description = db.Column(db.String(500), nullable=True, comment='Deskripsi Kode Data Referensi')
    app_language_id = db.Column(db.String(200), nullable=False, comment='Bahasa')
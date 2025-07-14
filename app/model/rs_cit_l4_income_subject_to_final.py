from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy import String, DECIMAL, text
from app import db

class RSCITL4IncomeSubjectToFinal(db.Model):
    __tablename__ = 'RS_CIT_L4_INCOME_SUBJECT_TO_FINAL'

    z_record_id = db.Column(String(55), primary_key=True)
    z_return_sheet_record_id = db.Column(String(55))
    z_tax_object_code = db.Column(String(3000))
    z_tax_object = db.Column(String(3000))
    z_tax_base = db.Column(DECIMAL(38, 8))
    z_tax_rate = db.Column(DECIMAL(38, 8))
    z_income_tax = db.Column(DECIMAL(38, 8))
    z_income_tax_usd = db.Column(DECIMAL(38, 8))
    z_is_deleted = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_is_manually = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_withholdingslips_aggregate_identifier = db.Column(String(55))
    z_table_source = db.Column(String(2000))
    z_last_updated_date = db.Column(
        TIMESTAMP(fsp=6),
        nullable=False,
        server_default=text('current_timestamp(6) ON UPDATE current_timestamp(6)')
    )
    z_creation_date = db.Column(
        TIMESTAMP(fsp=6),
        nullable=False,
        server_default=text('current_timestamp(6)')
    )
    z_is_migrated = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_is_migrated_and_updated = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_tin = db.Column(String(250))
    z_name = db.Column(String(250))
    z_tax_base_usd = db.Column(DECIMAL(38, 8))

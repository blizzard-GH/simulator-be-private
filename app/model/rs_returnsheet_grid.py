# model/rs_returnsheet_grid.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.dialects.mysql import TIMESTAMP
from datetime import date
from app import db

class RSReturnsheetGrid(db.Model):
    __tablename__ = 'RS_RETURNSHEET_GRID'

    Z_RECORD_ID = db.Column(db.String(55), primary_key=True)
    Z_TAXPAYER_AGGREGATE_IDENTIFIER = db.Column(db.String(55))
    Z_AGGREGATE_IDENTIFIER = db.Column(db.String(55))
    Z_AGGREGATE_VERSION = db.Column(db.Numeric(19, 0))
    Z_TAX_TYPE_CODE = db.Column(db.String(255))
    Z_RETURN_SHEET_TYPE_CODE = db.Column(db.String(255))
    Z_TAX_PERIOD_CODE = db.Column(db.String(255))
    Z_RETURN_SHEET_STATUS_CODE = db.Column(db.String(255))
    Z_RETURN_SHEET_VERSION_CODE = db.Column(db.String(255))
    Z_EXPECTED_RETURN_DATE = db.Column(db.Date)
    Z_RETURN_DATE = db.Column(db.Date)
    Z_ENTERED_DATE = db.Column(db.Date)
    Z_ASSESSMENT_DATE = db.Column(db.Date)
    Z_RETURN_SHEET_MODEL = db.Column(db.String(255))
    Z_TAX_OBJECT_DECIMAL = db.Column(db.String(50))
    Z_TAX_REGION_CODE = db.Column(db.String(255))
    Z_TAX_OFFICE_CODE = db.Column(db.String(255))
    Z_LETTER_APPENDIX = db.Column(db.String(255))
    Z_SUBMIT_TIMESTAMP = db.Column(db.Numeric(19, 0))
    Z_REJECTION_REASON = db.Column(db.String(255))
    Z_TOTAL_DECLARED_AMOUNT = db.Column(db.Numeric(38, 8))
    Z_DATE_NOTICE_OF_LATE_FILLING = db.Column(db.String(255))
    Z_BOOKKEEPING_PERIOD = db.Column(db.String(10))
    Z_PROCESS_REQUEST_STATUS = db.Column(db.String(256))
    Z_BPS_NO = db.Column(db.String(100))
    Z_CHANNEL_CODE = db.Column(db.String(100))
    Z_DATE_OF_RECEIPT = db.Column(db.Date)
    Z_PROOF_OF_RECEIPT = db.Column(db.String(100))
    Z_IS_ARCHIVED = db.Column(db.Numeric(1, 0), server_default=text('0'))
    Z_LAST_UPDATED_DATE = db.Column(TIMESTAMP(fsp=6), nullable=False, server_default=text('current_timestamp(6) ON UPDATE current_timestamp(6)'))
    Z_REJECTION_DECIMAL = db.Column(db.String(100))
    Z_IS_MIGRATED = db.Column(db.Numeric(1, 0), server_default=text('0'))
    Z_IS_MIGRATED_AND_UPDATED = db.Column(db.Numeric(1, 0), server_default=text('0'))
    Z_CREATION_DATE = db.Column(TIMESTAMP(fsp=6), nullable=False, server_default=text('current_timestamp(6)'))
    Z_PREFILL_STATUS = db.Column(db.String(50))
    Z_PREFILL_LAST_UPDATED = db.Column(TIMESTAMP(fsp=6), nullable=False, server_default=text("'0000-00-00 00:00:00.000000'"))
    Z_PREFILL_START = db.Column(TIMESTAMP(fsp=6), nullable=False, server_default=text("'0000-00-00 00:00:00.000000'"))
    Z_PREFILL_END = db.Column(TIMESTAMP(fsp=6), nullable=False, server_default=text("'0000-00-00 00:00:00.000000'"))
    Z_IS_TRANSACTION_WITH_RELATED = db.Column(db.Numeric(1, 0))
    Z_DOCUMENT_FORM_DECIMAL = db.Column(db.String(255))
    Z_DOCUMENT_FORM_AGGREGATE_IDENTIFIER = db.Column(db.String(16))
    Z_DOCUMENT_RECEIPT_DECIMAL = db.Column(db.String(255))
    Z_DOCUMENT_RECEIPT_AGGREGATE_IDENTIFIER = db.Column(db.String(16))
    Z_RETURN_SHEET_DECIMAL = db.Column(db.String(100))
    Z_SUBMIT_IN_PROGRESS_STATUS = db.Column(db.Numeric(1, 0), server_default=text('0'))
    Z_TIN = db.Column(db.String(16))
    Z_NAME = db.Column(db.String(255))

    # def to_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DECIMAL, text
from sqlalchemy.dialects.mysql import TIMESTAMP
from app import db
import datetime
import decimal

class PyBilling(db.Model):
    __tablename__ = 'PY_BILLING'

    z_record_id = db.Column(
        String(55),
        primary_key=True,
        server_default=text('uuid()')
    )
    z_aggregate_identifier = db.Column(String(55))
    z_aggregate_version = db.Column(DECIMAL(19, 0))
    z_taxpayer_aggregate_identifier = db.Column(String(55))
    z_taxpayer_tin_or_nik = db.Column(String(255))
    z_taxpayer_name = db.Column(String(500))
    z_taxpayer_address = db.Column(String(400))
    z_currency = db.Column(String(50))
    z_nominal = db.Column(DECIMAL(38, 8))
    z_number_of_transaction_details = db.Column(DECIMAL(38, 10))
    z_billing_code = db.Column(String(16))
    z_billing_code_sequence = db.Column(DECIMAL(38, 10))
    z_is_paid = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_payment_record_id = db.Column(String(55))
    z_return_sheet_type_code = db.Column(String(255))
    z_period_code = db.Column(String(50))
    z_billing_channel_code = db.Column(String(200))
    z_work_unit_code = db.Column(String(100))
    z_location_code = db.Column(String(100))
    z_is_paid_by_balance_transfer = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_remark = db.Column(String(400))
    z_last_updated_date = db.Column(
        TIMESTAMP(fsp=6),
        server_default=text('current_timestamp(6) ON UPDATE current_timestamp(6)')
    )
    z_creation_date = db.Column(
        TIMESTAMP(fsp=6),
        server_default=text('current_timestamp(6)')
    )
    z_is_migrated = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_is_migrated_and_updated = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_billing_code_creation_time = db.Column(
        TIMESTAMP(fsp=6),
        server_default=text("'0000-00-00 00:00:00.000000'")
    )
    z_billing_code_expiration_time = db.Column(
        TIMESTAMP(fsp=6),
        server_default=text("'0000-00-00 00:00:00.000000'")
    )
    z_is_expired_status_updated = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_deposit_desc = db.Column(String(100))
    z_deposit_month = db.Column(String(100))
    z_deposit_year = db.Column(DECIMAL(10, 0))
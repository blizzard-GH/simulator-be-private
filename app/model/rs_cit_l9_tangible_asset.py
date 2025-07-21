from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DECIMAL, Date, text
from sqlalchemy.dialects.mysql import TIMESTAMP
from app import db

class RSCITL9TangibleAsset(db.Model):
    __tablename__ = 'RS_CIT_L9_TANGIBLE_ASSET'

    z_record_id = db.Column(String(55), primary_key=True)
    z_return_sheet_record_id = db.Column(String(55))
    z_group_type = db.Column(String(3000))
    z_group_asset_type = db.Column(String(3000))
    z_month_year_acquisition = db.Column(Date)
    z_acquisition_price = db.Column(DECIMAL(38, 8))
    z_remaining_beginning_value = db.Column(DECIMAL(38, 8))
    z_method_commercial = db.Column(String(3000))
    z_method_fiscal = db.Column(String(3000))
    z_fiscal_year_value = db.Column(DECIMAL(38, 8))
    z_notes = db.Column(String(3000))
    z_is_deleted = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_is_manually = db.Column(DECIMAL(1, 0), server_default=text('0'))
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

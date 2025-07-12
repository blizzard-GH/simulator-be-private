from sqlalchemy import Column, DECIMAL, MetaData, String, Table, text
from sqlalchemy.dialects.mysql import LONGTEXT, TIMESTAMP

metadata = MetaData()


t_RS_RETURNSHEET_FORM_DATA = Table(
    'RS_RETURNSHEET_FORM_DATA', metadata,
    Column('Z_RECORD_ID', String(55)),
    Column('Z_AGGREGATE_IDENTIFIER', String(55)),
    Column('Z_AGGREGATE_VERSION', DECIMAL(19, 0)),
    Column('Z_RETURN_SHEET_VERSION_CODE', String(50)),
    Column('Z_FORM_DATA', LONGTEXT),
    Column('Z_LAST_UPDATED_DATE', TIMESTAMP(fsp=6), nullable=False, server_default=text('current_timestamp(6) ON UPDATE current_timestamp(6)')),
    Column('Z_IS_MIGRATED', DECIMAL(1, 0), server_default=text('0')),
    Column('Z_IS_MIGRATED_AND_UPDATED', DECIMAL(1, 0), server_default=text('0')),
    Column('Z_CREATION_DATE', TIMESTAMP(fsp=6), nullable=False, server_default=text('current_timestamp(6)'))
)

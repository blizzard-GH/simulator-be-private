from sqlalchemy import Column, DECIMAL, Date, MetaData, String, Table, text
from sqlalchemy.dialects.mysql import TIMESTAMP

metadata = MetaData()


t_RS_CIT_L9_GROUP_OF_BUILDING = Table(
    'RS_CIT_L9_GROUP_OF_BUILDING', metadata,
    Column('Z_RECORD_ID', String(55)),
    Column('Z_RETURN_SHEET_RECORD_ID', String(55)),
    Column('Z_GROUP_TYPE', String(3000)),
    Column('Z_GROUP_ASSET_TYPE', String(3000)),
    Column('Z_MONTH_YEAR_ACQUISITION', Date),
    Column('Z_ACQUISITION_PRICE', DECIMAL(38, 8)),
    Column('Z_REMAINING_BEGINNING_VALUE', DECIMAL(38, 8)),
    Column('Z_METHOD_COMMERCIAL', String(3000)),
    Column('Z_METHOD_FISCAL', String(3000)),
    Column('Z_FISCAL_YEAR_VALUE', DECIMAL(38, 8)),
    Column('Z_NOTES', String(3000)),
    Column('Z_IS_DELETED', DECIMAL(1, 0), server_default=text('0')),
    Column('Z_IS_MANUALLY', DECIMAL(1, 0), server_default=text('0')),
    Column('Z_LAST_UPDATED_DATE', TIMESTAMP(fsp=6), nullable=False, server_default=text('current_timestamp(6) ON UPDATE current_timestamp(6)')),
    Column('Z_CREATION_DATE', TIMESTAMP(fsp=6), nullable=False, server_default=text('current_timestamp(6)')),
    Column('Z_IS_MIGRATED', DECIMAL(1, 0), server_default=text('0')),
    Column('Z_IS_MIGRATED_AND_UPDATED', DECIMAL(1, 0), server_default=text('0'))
)

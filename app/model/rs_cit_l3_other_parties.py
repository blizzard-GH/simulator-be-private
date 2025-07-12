from sqlalchemy import Column, DECIMAL, Date, MetaData, String, Table, text
from sqlalchemy.dialects.mysql import TIMESTAMP

metadata = MetaData()


t_RS_CIT_L3_OTHER_PARTIES = Table(
    'RS_CIT_L3_OTHER_PARTIES', metadata,
    Column('Z_RECORD_ID', String(55)),
    Column('Z_RETURN_SHEET_RECORD_ID', String(55)),
    Column('Z_TAXPAYER_NAME', String(3000)),
    Column('Z_TIN', String(3000)),
    Column('Z_TAX_TYPE', String(3000)),
    Column('Z_TAX_BASE', DECIMAL(38, 8)),
    Column('Z_INCOME_TAX', DECIMAL(38, 8)),
    Column('Z_INCOME_TAX_USD', DECIMAL(38, 8)),
    Column('Z_WITHHOLDING_SLIPS_DECIMAL', String(3000)),
    Column('Z_WITHHOLDING_SLIPS_DATE', Date),
    Column('Z_IS_DELETED', DECIMAL(1, 0), server_default=text('0')),
    Column('Z_IS_MANUALLY', DECIMAL(1, 0), server_default=text('0')),
    Column('Z_WITHHOLDINGSLIPS_AGGREGATE_IDENTIFIER', String(55)),
    Column('Z_TABLE_SOURCE', String(2000)),
    Column('Z_LAST_UPDATED_DATE', TIMESTAMP(fsp=6), nullable=False, server_default=text('current_timestamp(6) ON UPDATE current_timestamp(6)')),
    Column('Z_CREATION_DATE', TIMESTAMP(fsp=6), nullable=False, server_default=text('current_timestamp(6)')),
    Column('Z_IS_MIGRATED', DECIMAL(1, 0), server_default=text('0')),
    Column('Z_IS_MIGRATED_AND_UPDATED', DECIMAL(1, 0), server_default=text('0'))
)

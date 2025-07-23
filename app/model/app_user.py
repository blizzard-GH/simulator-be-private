from sqlalchemy import Index, text
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class APPUSER(db.Model):
    __tablename__ = 'APP_USER'
    __table_args__ = (
        Index('CORPORATE_TIN', 'CORPORATE_TIN', unique=True),
        Index('PERSONAL_TIN', 'PERSONAL_TIN', unique=True),
    )

    ID = db.Column(BIGINT(20), primary_key=True, comment='ID')
    PERSONAL_TIN = db.Column(db.String(16), nullable=False, comment='NPWP 16 digit')
    CORPORATE_TIN = db.Column(db.String(16), nullable=False, comment='NPWP Badan 16 digit')
    PERSONAL_NAME = db.Column(db.String(255), nullable=False, comment='Nama Wajib Pajak')
    CORPORATE_NAME = db.Column(db.String(255), nullable=False, comment='Nama Wajib Pajak Badan')
    CREATION_DATE = db.Column(db.TIMESTAMP, server_default=text('current_timestamp() ON UPDATE current_timestamp()'), comment='Tanggal Pembuatan')
    LAST_LOGIN_DATE = db.Column(db.TIMESTAMP, server_default=text("'0000-00-00 00:00:00'"), comment='Tanggal Login Terakhir')
    PASSWORD_HASH = db.Column("PASSWORD", db.String(255), nullable=True, comment='Password hash')
    PASSPHRASE_HASH = db.Column("PASSPHRASE", db.String(255), nullable=True, comment='Passphrase hash')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')
    
    @property
    def passphrase(self):
        raise AttributeError('Passphrase is not a readable attribute.')

    @password.setter
    def password(self, raw_password):
        self.PASSWORD_HASH = generate_password_hash(raw_password)
    
    @passphrase.setter
    def passphrase(self, raw_passphrase):
        self.PASSPHRASE_HASH = generate_password_hash(raw_passphrase)

    def check_password(self, password):
        return check_password_hash(self.PASSWORD_HASH, password)
    
    def check_passphrase(self, passphrase):
        return check_password_hash(self.PASSPHRASE_HASH, passphrase)
    


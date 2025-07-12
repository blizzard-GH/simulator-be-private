from sqlalchemy import Index, text
from sqlalchemy.dialects.mysql import BIGINT
from app import db

class TblUser(db.Model):
    __tablename__ = 'tbl_user'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('tbl_user_npwp15_IDX', 'npwp15', unique=True),
        Index('username', 'username', unique=True),
    )

    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='ID')
    npwp15 = db.Column(db.String(15), nullable=False, comment='NPWP 15 digit')
    username = db.Column(db.String(16), nullable=False, comment='NPWP 16 digit')
    email = db.Column(db.String(255), nullable=False, comment='email address')
    nama_wp = db.Column(db.String(255), nullable=False, comment='Nama Wajib Pajak')
    jenis_wp = db.Column(
        db.Enum('personal', 'corporate', 'government'),
        nullable=False,
        comment='Jenis Wajib Pajak'
    )
    status = db.Column(
        db.Enum('y', 'n'),
        server_default=text("'n'"),
        nullable=False,
        comment='Status akun'
    )
    status_email = db.Column(
        db.Enum('y', 'n'),
        server_default=text("'n'"),
        nullable=False,
        comment='Status pengiriman email'
    )
    password = db.Column(db.String(255), nullable=True, comment='Password hash')
    first_login = db.Column(db.TIMESTAMP, nullable=True, comment='Login Pertama')
    last_login = db.Column(db.TIMESTAMP, nullable=True, comment='Login Terakhir')
    created_at = db.Column(db.TIMESTAMP, nullable=True)

    # def to_dict(self):
    #     return {"id": self.id, "npwp15": self.npwp15, "username": self.username}
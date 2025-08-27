from datetime import datetime
import uuid

from sqlalchemy import null
from ..model.app_user import APPUSER
from flask import abort
from ..utils.serializer import model_to_dict
from app import db

def get_app_user_by_tin_service(tin):
    appUser = APPUSER.query.filter_by(TIN=tin).first()

    if not appUser:
        abort(404, description=f"User with TIN {tin} not found")

    return model_to_dict(appUser)

def get_corporate_user_by_personal_tin_service(tin):
    appUser = APPUSER.query.filter_by(TIN_PERSONAL=tin, ROLE=1).first()

    if not appUser:
        abort(404, description=f"User with TIN {tin} not found")

    return model_to_dict(appUser)

def create_app_user_service(tin):
    personalUser = APPUSER(
        TIN=tin,
        NAME="NAMA" + tin[6:],
        password="P@jakTumbuh1ndonesiaT@ngguh",
        passphrase="P@jakTumbuh1ndonesiaT@ngguh",
        IS_CORPORATE=0,
        # TIN_PERSONAL=null,
        # CREATION_DATE=datetime.now(),
        # LAST_LOGIN_DATE=datetime.now(),
        ROLE=0,
        # Z_TAXPAYER_AGGREGATE_IDENTIFIER=str(uuid.uuid4())
    )
    corporateUser = APPUSER(
        TIN="0" + tin[1:],
        NAME="BADAN" + tin[6:],
        password="P@jakTumbuh1ndonesiaT@ngguh",
        passphrase="P@jakTumbuh1ndonesiaT@ngguh",
        IS_CORPORATE=1,
        TIN_PERSONAL=tin,
        # CREATION_DATE=datetime.now(),
        # LAST_LOGIN_DATE=datetime.now(),
        ROLE=1,
        # Z_TAXPAYER_AGGREGATE_IDENTIFIER=str(uuid.uuid4())
    )
    db.session.add(personalUser)
    db.session.add(corporateUser)
    db.session.commit()
    return model_to_dict(personalUser)

def update_last_login_date_by_tin_service(tin):
    appUser = APPUSER.query.filter_by(TIN=tin).first()
    appUser.LAST_LOGIN_DATE = datetime.now()
    db.session.commit()
    return model_to_dict(appUser)

def check_passphrase_service(tin, passphrase):
    appUser = APPUSER.query.filter_by(TIN=tin).first()
    if not appUser:
        abort(404, description=f"User with TIN {tin} not found")
    return appUser.check_passphrase(passphrase)
    
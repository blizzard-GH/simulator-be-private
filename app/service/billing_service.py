from ..model.py_billing import PyBilling
from ..model.rs_returnsheet_grid import RSReturnsheetGrid
from ..utils.serializer import model_to_dict, models_to_list,serialize_model_or_list
from sqlalchemy import desc
from app import db
from flask import jsonify, json
from sqlalchemy import Null
from datetime import datetime
import random
import uuid

def get_billing_by_tai_service(tai):
    billing = PyBilling.query.filter(PyBilling.z_taxpayer_aggregate_identifier==tai, PyBilling.z_is_paid==0).order_by(desc(PyBilling.z_creation_date)).all()
    return serialize_model_or_list(billing)

def pay_billing_service(tai,z_payment_record_id):
    try:
        billing = PyBilling.query.filter(PyBilling.z_taxpayer_aggregate_identifier==tai, PyBilling.z_payment_record_id==z_payment_record_id, PyBilling.z_is_paid==0).order_by(desc(PyBilling.z_creation_date)).first()
        if not billing:
            print("Billing not found")
            return jsonify({"error": "Billing not found"}), 404
        billing.z_is_paid = 1

        returnsheetgrid = RSReturnsheetGrid.query.filter(RSReturnsheetGrid.Z_RECORD_ID==z_payment_record_id).first()
        if not returnsheetgrid:
            print("Returnsheet Grid not found")
            return jsonify({"error": "Returnsheet Grid not found"}), 404
            
        returnsheetgrid.Z_RETURN_SHEET_STATUS_CODE = "SUBMITTED"
        returnsheetgrid.Z_RETURN_DATE = datetime.now()

        # Count rows in DB
        row_count = db.session.query(RSReturnsheetGrid).count() + 1  # +1 if you want next number

        # Format row count with leading zeros (5 digits: 00018)
        row_number = f"{row_count:05d}"

        # Generate random 4-digit number
        random_num = f"{random.randint(0, 9999):04d}"

        # Build Z_BPS_NO
        returnsheetgrid.Z_BPS_NO = f"BPS-{row_number}/CT/KPP.{random_num}/2025"
        
        db.session.commit()
        return {"message": "Billing paid successfully"}, 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
def new_billing_service(tai, data):
    try:

        grid = RSReturnsheetGrid.query.filter(RSReturnsheetGrid.Z_RECORD_ID==data.get("citrForm").get("Z_RECORD_ID")).first()
        if not grid:
            print("Returnsheet Grid not found")
            return jsonify({"error": "Returnsheet Grid not found"}), 404

        if grid.Z_RETURN_SHEET_MODEL == "NORMAL":
            nominal = data.get("mainForm").get("IncomeTaxMustPaid")
        else:
            nominal = data.get("mainForm").get("UnderpaymentIncomeDueAmended")
        
        new_billing = PyBilling(
            z_aggregate_identifier = str(uuid.uuid4()),
            z_aggregate_version = 1,
            z_taxpayer_aggregate_identifier = tai,
            z_taxpayer_tin_or_nik = data.get("mainForm").get("Tin"),
            z_taxpayer_name = data.get("mainForm").get("Name"),
            z_taxpayer_address = None,
            z_currency = 'IDR',
            z_nominal = nominal,
            z_number_of_transaction_details = 1,
            z_billing_code = ''.join(str(random.randint(0, 9)) for _ in range(15)),
            z_billing_code_sequence = None,
            z_is_paid = 0,
            z_payment_record_id = data.get("citrForm").get("Z_RECORD_ID"),
            z_return_sheet_type_code = grid.Z_RETURN_SHEET_TYPE_CODE,
            z_period_code = grid.Z_TAX_PERIOD_CODE,
            z_billing_channel_code = '0-8888-000021',
            z_work_unit_code = '560862',
            z_location_code = '3174011002',
            z_is_paid_by_balance_transfer = 0,
            z_remark = None,
            z_last_updated_date = datetime.now(),
            z_creation_date = datetime.now(),
            z_is_migrated = 0,
            z_is_migrated_and_updated = 0,
            z_billing_code_creation_time = datetime.now(),
            z_billing_code_expiration_time = datetime(2038, 1, 18, 23, 59, 59),
            z_is_expired_status_updated = 1,
            z_deposit_desc = None,
            z_deposit_month = None,
            z_deposit_year = None
        )

        db.session.add(new_billing)
        db.session.commit()
        return {"message": "Billing created successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
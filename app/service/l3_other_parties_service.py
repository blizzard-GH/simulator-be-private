from sqlalchemy import null
from ..model.rs_cit_l3_other_parties import RSCITL3OtherParties
from flask import abort, jsonify
from ..utils.serializer import serialize_model_or_list
from app import db
from datetime import datetime
import random
import uuid

def get_l3_other_parties_by_returnsheet_record_id_service(returnsheet_record_id):
    l3OtherService = RSCITL3OtherParties.query.filter_by(z_return_sheet_record_id=returnsheet_record_id, z_is_deleted=0).all()

    if not l3OtherService:
        abort(404, description=f"L3 Other Parties with Returnsheet Record ID {returnsheet_record_id} not found")

    return serialize_model_or_list(l3OtherService)

def insert_prefill_withholding_by_returnsheet_record_id_service(returnsheet_record_id, option):

    try:
        rows_to_insert = 5 if option == "0" else 10 if option == "1" else 15

        new_record = []
        for i in range(rows_to_insert):
            record = RSCITL3OtherParties(
                z_record_id=str(uuid.uuid4()),
                z_return_sheet_record_id=returnsheet_record_id,
                z_taxpayer_name="Taxpayer Name " + str(i),
                z_tin=str(random.randint(10**15, 10**16 - 1)),
                z_tax_type=random.choice(options),
                z_tax_base=10000000,
                z_income_tax=100000,
                z_income_tax_usd=61.18,
                z_withholding_slips_decimal="SSP"+str(i),
                z_withholding_slips_date=datetime.now(),
                z_is_deleted=0,
                z_is_manually=1,
                z_withholdingslips_aggregate_identifier=str(uuid.uuid4()),
                z_table_source=null,
                z_last_updated_date=datetime.now(),
                z_creation_date=datetime.now(),
                z_is_migrated=0,
                z_is_migrated_and_updated=0
            )
            new_record.append(record)

        db.session.bulk_save_objects(new_record)
        db.session.commit()

        return jsonify({"message": f"{rows_to_insert} rows inserted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

options = [
    "ARTICLE15",
    "ARTICLE21",
    "ARTICLE22",
    "ARTICLE23",
    "ARTICLE26",
    "BORNEBYGOVERNMENT",
    "BORNEBYGOVERNMENTFOREIGNAID",
    "EXCESSOVERPAYMENT"
]
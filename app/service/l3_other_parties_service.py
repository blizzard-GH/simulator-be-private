from ..model.rs_cit_l3_other_parties import RSCITL3OtherParties
from flask import abort
from ..utils.serializer import serialize_model_or_list

def get_l3_other_parties_by_returnsheet_record_id_service(returnsheet_record_id):
    l3OtherService = RSCITL3OtherParties.query.filter_by(z_return_sheet_record_id=returnsheet_record_id).all()

    if not l3OtherService:
        abort(404, description=f"Returnsheet Form Data with Record ID {returnsheet_record_id} not found")

    return serialize_model_or_list(l3OtherService)
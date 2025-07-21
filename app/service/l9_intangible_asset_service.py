from ..model.rs_cit_l9_intangible_asset import RSCITL9IntangibleAsset
from flask import abort
from ..utils.serializer import serialize_model_or_list

def get_l9_intangible_asset_by_returnsheet_record_id_service(returnsheet_record_id):
    l9IntangibleAsset = RSCITL9IntangibleAsset.query.filter_by(z_return_sheet_record_id=returnsheet_record_id, z_is_deleted=0).all()

    if not l9IntangibleAsset:
        abort(404, description=f"L9 Intangible Asset with Returnsheet Record ID {returnsheet_record_id} not found")

    return serialize_model_or_list(l9IntangibleAsset)
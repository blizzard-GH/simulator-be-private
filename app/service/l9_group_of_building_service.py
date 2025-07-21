from ..model.rs_cit_l9_group_of_building import RSCITL9GroupOfBuilding
from flask import abort
from ..utils.serializer import serialize_model_or_list

def get_l9_group_of_building_by_returnsheet_record_id_service(returnsheet_record_id):
    l9GroupOfBuilding = RSCITL9GroupOfBuilding.query.filter_by(z_return_sheet_record_id=returnsheet_record_id, z_is_deleted=0).all()

    if not l9GroupOfBuilding:
        abort(404, description=f"L9 Group Of Building with Returnsheet Record ID {returnsheet_record_id} not found")

    return serialize_model_or_list(l9GroupOfBuilding)
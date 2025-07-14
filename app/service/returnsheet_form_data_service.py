from ..model.rs_returnsheet_form_data import RSReturnsheetFormData
from flask import abort
from ..utils.serializer import model_to_dict, models_to_list

def get_returnsheet_form_data_by_record_id_service(recordId):
    returnsheetFormData = RSReturnsheetFormData.query.filter_by(z_record_id=recordId).first()

    if not returnsheetFormData:
        abort(404, description=f"Returnsheet Form Data with Record ID {recordId} not found")

    return model_to_dict(returnsheetFormData)
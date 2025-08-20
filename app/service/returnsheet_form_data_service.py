from ..model.rs_returnsheet_form_data import RSReturnsheetFormData
from flask import abort
from ..utils.serializer import model_to_dict, models_to_list
from ..service import returnsheet_grid_service

def get_returnsheet_form_data_by_record_id_service(recordId, tai):
    returnsheetGrid = returnsheet_grid_service.check_returnsheet_grid_by_record_id_service(recordId, tai)
    if not returnsheetGrid:
        abort(401, description=f"Returnsheet Form Data with Record ID {recordId} not found")

    returnsheetFormData = RSReturnsheetFormData.query.filter_by(z_record_id=recordId).first()

    if not returnsheetFormData:
        abort(404, description=f"Returnsheet Form Data with Record ID {recordId} not found")

    return model_to_dict(returnsheetFormData)

def get_returnsheet_form_data_by_aggregate_identifier_service(aggregate_identifier):
    returnsheetFormData = RSReturnsheetFormData.query.filter_by(z_aggregate_identifier=aggregate_identifier).first()

    if not returnsheetFormData:
        abort(404, description=f"Returnsheet Form Data with Record ID {aggregate_identifier} not found")

    return model_to_dict(returnsheetFormData)

def get_returnsheet_main_form_data_by_record_id_service(recordid):
    returnsheetFormData = RSReturnsheetFormData.query.filter_by(z_record_id=recordid).first()

    if not returnsheetFormData:
        abort(404, description=f"Returnsheet Form Data with Record ID {recordid} not found")

    return returnsheetFormData.get_main_form_data()

def get_returnsheet_main_form_data_by_aggregate_identifier_service(aggregate_identifier):
    returnsheetFormData = RSReturnsheetFormData.query.filter_by(z_aggregate_identifier=aggregate_identifier).first()

    if not returnsheetFormData:
        abort(404, description=f"Returnsheet Form Data with Record ID {aggregate_identifier} not found")

    return returnsheetFormData.get_main_form_data()
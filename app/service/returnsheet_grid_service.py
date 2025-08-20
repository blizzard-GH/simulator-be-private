from ..model.rs_returnsheet_grid import RSReturnsheetGrid
from ..utils.serializer import model_to_dict, models_to_list,serialize_model_or_list
from sqlalchemy import desc
from flask import abort

def get_returnsheet_grid_by_record_id_service(recordId, tai):
    returnsheetGrid = RSReturnsheetGrid.query.filter_by(Z_RECORD_ID=recordId,Z_TAXPAYER_AGGREGATE_IDENTIFIER=tai).first()

    if not returnsheetGrid:
        abort(404, description=f"Returnsheet Grid with Record ID {recordId} not found")

    return model_to_dict(returnsheetGrid)

def check_returnsheet_grid_by_record_id_service(recordId, tai):
    returnsheetGrid = RSReturnsheetGrid.query.filter_by(Z_RECORD_ID=recordId,Z_TAXPAYER_AGGREGATE_IDENTIFIER=tai).first()

    if not returnsheetGrid:
        abort(401, description=f"Returnsheet Grid with Record ID {recordId} not found")

    return model_to_dict(returnsheetGrid)

def get_all_returnsheet_grid_service(limit=20):
    returnsheetGrid = RSReturnsheetGrid.query.order_by(desc(RSReturnsheetGrid.Z_CREATION_DATE)).limit(limit).all()
    return models_to_list(returnsheetGrid)

def get_not_submitted_returnsheet_grid_by_tai_service(tai):
    returnsheetGrid = RSReturnsheetGrid.query.filter(
        RSReturnsheetGrid.Z_TAXPAYER_AGGREGATE_IDENTIFIER == tai,
        RSReturnsheetGrid.Z_RETURN_SHEET_STATUS_CODE.in_(['DRAFT', 'CREATED'])
    ).order_by(desc(RSReturnsheetGrid.Z_CREATION_DATE)).all()
    return serialize_model_or_list(returnsheetGrid)

def get_submitted_returnsheet_grid_by_tai_service(tai):
    returnsheetGrid = RSReturnsheetGrid.query.filter_by(Z_TAXPAYER_AGGREGATE_IDENTIFIER=tai,Z_RETURN_SHEET_STATUS_CODE='SUBMITTED').order_by(desc(RSReturnsheetGrid.Z_CREATION_DATE)).all()
    return serialize_model_or_list(returnsheetGrid)

def get_waiting_for_payment_returnsheet_grid_by_tai_service(tai):
    returnsheetGrid = RSReturnsheetGrid.query.filter_by(Z_TAXPAYER_AGGREGATE_IDENTIFIER=tai,Z_RETURN_SHEET_STATUS_CODE='WAITINGFORPAYMENT').order_by(desc(RSReturnsheetGrid.Z_CREATION_DATE)).all()
    return serialize_model_or_list(returnsheetGrid)

def get_canceled_returnsheet_grid_by_tai_service(tai):
    returnsheetGrid = RSReturnsheetGrid.query.filter_by(Z_TAXPAYER_AGGREGATE_IDENTIFIER=tai,Z_RETURN_SHEET_STATUS_CODE='CANCELED').order_by(desc(RSReturnsheetGrid.Z_CREATION_DATE)).all()
    return serialize_model_or_list(returnsheetGrid)

def get_rejected_returnsheet_grid_by_tai_service(tai):
    returnsheetGrid = RSReturnsheetGrid.query.filter_by(Z_TAXPAYER_AGGREGATE_IDENTIFIER=tai,Z_RETURN_SHEET_STATUS_CODE='REJECTED').order_by(desc(RSReturnsheetGrid.Z_CREATION_DATE)).all()
    return serialize_model_or_list(returnsheetGrid)
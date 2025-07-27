from ..model.current_reference_data import CurrentReferenceData
from flask import abort
from ..utils.serializer import model_to_dict

def get_current_reference_data_by_reference_data_type_and_code_service(reference_data_type, code):
    currentReferenceData = CurrentReferenceData.query.filter_by(reference_data_type=reference_data_type, code=code).first()

    if not currentReferenceData:
        abort(404, description=f"Current Reference Data with Reference Data Type {reference_data_type} and Code {code} not found")

    return model_to_dict(currentReferenceData)
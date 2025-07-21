from ..model.rs_cit_l4_income_subject_to_final import RSCITL4IncomeSubjectToFinal
from flask import abort
from ..utils.serializer import serialize_model_or_list

def get_l4_income_subject_to_final_by_returnsheet_record_id_service(returnsheet_record_id):
    l4IncomeSubjectToFinal = RSCITL4IncomeSubjectToFinal.query.filter_by(z_return_sheet_record_id=returnsheet_record_id, z_is_deleted=0).all()

    if not l4IncomeSubjectToFinal:
        abort(404, description=f"Returnsheet Form Data with Record ID {returnsheet_record_id} not found")

    return serialize_model_or_list(l4IncomeSubjectToFinal)
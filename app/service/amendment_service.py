from sqlalchemy import Null, desc
from app import db
from flask import jsonify, json
from app import db
from datetime import datetime
import uuid

from app.model.rs_cit_l3_other_parties import RSCITL3OtherParties
from app.model.rs_cit_l4_income_subject_to_final import RSCITL4IncomeSubjectToFinal
from app.model.rs_cit_l9_group_of_building import RSCITL9GroupOfBuilding
from app.model.rs_cit_l9_intangible_asset import RSCITL9IntangibleAsset
from app.model.rs_cit_l9_tangible_asset import RSCITL9TangibleAsset
from app.model.rs_returnsheet_grid import RSReturnsheetGrid
from app.model.rs_returnsheet_form_data import RSReturnsheetFormData
from app.service.l3_other_parties_service import get_l3_other_parties_by_returnsheet_record_id_service
from app.service.l4_income_subject_to_final_service import get_l4_income_subject_to_final_by_returnsheet_record_id_service
from app.service.l9_group_of_building_service import get_l9_group_of_building_by_returnsheet_record_id_service
from app.service.l9_intangible_asset_service import get_l9_intangible_asset_by_returnsheet_record_id_service
from app.service.l9_tangible_asset_service import get_l9_tangible_asset_by_returnsheet_record_id_service

def get_latest_returnsheet(tai, taxType,taxReturnPeriodType,taxYear,taxReturnModel):
    last_spt = {}
    taxType = taxType
    taxPeriodCode = taxReturnPeriodType+str(taxYear)
    taxReturnModel = taxReturnModel
    # Z_TAX_PERIOD_CODE
    
    grid = RSReturnsheetGrid.query.filter_by(Z_TAXPAYER_AGGREGATE_IDENTIFIER=tai,Z_TAX_TYPE_CODE=taxType,Z_TAX_PERIOD_CODE=taxPeriodCode).order_by(desc(RSReturnsheetGrid.Z_SUBMIT_TIMESTAMP)).first()
    if not grid:
        return jsonify({"error": "Returnsheet Grid not found"}), 404
    
    form_data = RSReturnsheetFormData.query.filter_by(z_record_id=grid.Z_RECORD_ID).first()
    if not form_data:
        return jsonify({"error": "Returnsheet Form Data not found"}), 404
    
    l3OtherParties = RSCITL3OtherParties.query.filter_by(z_return_sheet_record_id=grid.Z_RECORD_ID).all()
    l4IncomeSubjectToFinals = RSCITL4IncomeSubjectToFinal.query.filter_by(z_return_sheet_record_id=grid.Z_RECORD_ID, z_is_deleted=0).all()
    l9TangibleAssets = RSCITL9TangibleAsset.query.filter_by(z_return_sheet_record_id=grid.Z_RECORD_ID, z_is_deleted=0).all()
    l9GroupOfBuildings = RSCITL9GroupOfBuilding.query.filter_by(z_return_sheet_record_id=grid.Z_RECORD_ID, z_is_deleted=0).all()
    l9IntangibleAssets = RSCITL9IntangibleAsset.query.filter_by(z_return_sheet_record_id=grid.Z_RECORD_ID, z_is_deleted=0).all()

    last_spt["grid"] = grid
    last_spt["form_data"] = form_data
    if l3OtherParties:
        last_spt["l3_other_parties"] = l3OtherParties
    if l4IncomeSubjectToFinals:
        last_spt["l4_income_subject_to_finals"] = l4IncomeSubjectToFinals
    if l9TangibleAssets:
        last_spt["l9_tangible_assets"] = l9TangibleAssets
    if l9GroupOfBuildings:
        last_spt["l9_group_of_buildings"] = l9GroupOfBuildings
    if l9IntangibleAssets:
        last_spt["l9_intangible_assets"] = l9IntangibleAssets
    
    return last_spt

# def get_latest_returnsheet_form_data(taxType,taxReturnPeriodType,taxYear,taxReturnModel):
#     x = RSReturnsheetFormData.query.filter_by(Z_TAX_TYPE_CODE=taxType,Z_TAX_PERIOD_CODE=taxReturnPeriodType+taxYear.toString(),Z_TAX_RETURN_SHEET_MODEL_CODE=taxReturnModel).order_by(RSReturnsheetFormData.Z_AGGREGATE_VERSION.desc()).first()
#     return x

def create_amendment_service(tai, taxType, taxReturnPeriodType, taxYear, taxReturnModel):
    # taxType = returnsheetCreateForm.get("TaxType")
    # taxReturnPeriodType = returnsheetCreateForm.get("TaxReturnPeriodType")
    # taxYear = returnsheetCreateForm.get("TaxYear")
    # taxReturnModel = returnsheetCreateForm.get("TaxReturnModel")
    try:

        # Get latest returnsheet grid
        last_spt = get_latest_returnsheet(tai,taxType,taxReturnPeriodType,taxYear,taxReturnModel)
        
        # Check if returnsheet grid exists
        if not last_spt:
            return jsonify({"error": "Returnsheet not found"}), 404
        
        # Check if returnsheet grid is submitted
        if last_spt["grid"].Z_RETURN_SHEET_STATUS_CODE != "SUBMITTED":
            return jsonify({"error": "Last Returnsheet is not submitted"}), 400
            
        # Create new returnsheet grid
        returnsheet_grid_new = RSReturnsheetGrid(
            # z_record_id=str(uuid.uuid4()),
            Z_RECORD_ID=str(uuid.uuid4()),
            Z_TAXPAYER_AGGREGATE_IDENTIFIER=last_spt["grid"].Z_TAXPAYER_AGGREGATE_IDENTIFIER,
            Z_AGGREGATE_IDENTIFIER=str(uuid.uuid4()),
            Z_AGGREGATE_VERSION=last_spt["grid"].Z_AGGREGATE_VERSION,
            Z_TAX_TYPE_CODE=last_spt["grid"].Z_TAX_TYPE_CODE,
            Z_RETURN_SHEET_TYPE_CODE=last_spt["grid"].Z_RETURN_SHEET_TYPE_CODE,
            Z_TAX_PERIOD_CODE=last_spt["grid"].Z_TAX_PERIOD_CODE,
            Z_RETURN_SHEET_STATUS_CODE="CREATED",
            Z_RETURN_SHEET_VERSION_CODE=last_spt["grid"].Z_RETURN_SHEET_VERSION_CODE,
            Z_EXPECTED_RETURN_DATE=last_spt["grid"].Z_EXPECTED_RETURN_DATE,
            Z_RETURN_DATE=last_spt["grid"].Z_RETURN_DATE,
            Z_ENTERED_DATE=last_spt["grid"].Z_ENTERED_DATE,
            Z_ASSESSMENT_DATE=last_spt["grid"].Z_ASSESSMENT_DATE,
            Z_RETURN_SHEET_MODEL="AMENDMENT",
            Z_TAX_OBJECT_DECIMAL=last_spt["grid"].Z_TAX_OBJECT_DECIMAL,
            Z_TAX_REGION_CODE=last_spt["grid"].Z_TAX_REGION_CODE,
            Z_TAX_OFFICE_CODE=last_spt["grid"].Z_TAX_OFFICE_CODE,
            Z_LETTER_APPENDIX=last_spt["grid"].Z_LETTER_APPENDIX,
            Z_SUBMIT_TIMESTAMP=last_spt["grid"].Z_SUBMIT_TIMESTAMP,
            Z_REJECTION_REASON=last_spt["grid"].Z_REJECTION_REASON,
            Z_TOTAL_DECLARED_AMOUNT=last_spt["grid"].Z_TOTAL_DECLARED_AMOUNT,
            Z_DATE_NOTICE_OF_LATE_FILLING=last_spt["grid"].Z_DATE_NOTICE_OF_LATE_FILLING,
            Z_BOOKKEEPING_PERIOD=last_spt["grid"].Z_BOOKKEEPING_PERIOD,
            Z_PROCESS_REQUEST_STATUS=last_spt["grid"].Z_PROCESS_REQUEST_STATUS,
            Z_BPS_NO="",
            Z_CHANNEL_CODE=last_spt["grid"].Z_CHANNEL_CODE,
            Z_DATE_OF_RECEIPT=None,
            Z_PROOF_OF_RECEIPT="",
            Z_IS_ARCHIVED=last_spt["grid"].Z_IS_ARCHIVED,
            Z_LAST_UPDATED_DATE=datetime.now(),
            Z_REJECTION_DECIMAL=last_spt["grid"].Z_REJECTION_DECIMAL,
            Z_IS_MIGRATED=last_spt["grid"].Z_IS_MIGRATED,
            Z_IS_MIGRATED_AND_UPDATED=last_spt["grid"].Z_IS_MIGRATED_AND_UPDATED,
            Z_CREATION_DATE=datetime.now(),
            Z_PREFILL_STATUS="",
            Z_PREFILL_LAST_UPDATED=None,
            Z_PREFILL_START=None,
            Z_PREFILL_END=None,
            Z_IS_TRANSACTION_WITH_RELATED=last_spt["grid"].Z_IS_TRANSACTION_WITH_RELATED,
            Z_DOCUMENT_FORM_DECIMAL=last_spt["grid"].Z_DOCUMENT_FORM_DECIMAL,
            Z_DOCUMENT_FORM_AGGREGATE_IDENTIFIER=last_spt["grid"].Z_DOCUMENT_FORM_AGGREGATE_IDENTIFIER,
            Z_DOCUMENT_RECEIPT_DECIMAL=last_spt["grid"].Z_DOCUMENT_RECEIPT_DECIMAL,
            Z_DOCUMENT_RECEIPT_AGGREGATE_IDENTIFIER=last_spt["grid"].Z_DOCUMENT_RECEIPT_AGGREGATE_IDENTIFIER,
            Z_RETURN_SHEET_DECIMAL=last_spt["grid"].Z_RETURN_SHEET_DECIMAL,
            Z_SUBMIT_IN_PROGRESS_STATUS=last_spt["grid"].Z_SUBMIT_IN_PROGRESS_STATUS
        )
        db.session.add(returnsheet_grid_new)

        # Create new returnsheet form data
        returnsheet_form_data_new = RSReturnsheetFormData(
            z_record_id=returnsheet_grid_new.Z_RECORD_ID,
            z_aggregate_identifier=last_spt["form_data"].z_aggregate_identifier,
            z_aggregate_version=last_spt["form_data"].z_aggregate_version,
            z_return_sheet_version_code=last_spt["form_data"].z_return_sheet_version_code,
            z_form_data=last_spt["form_data"].z_form_data,
            z_last_updated_date=datetime.now(),
            z_is_migrated=last_spt["form_data"].z_is_migrated,
            z_is_migrated_and_updated=last_spt["form_data"].z_is_migrated_and_updated,
            z_creation_date=datetime.now()
        )
        db.session.add(returnsheet_form_data_new)

        if last_spt["l3_other_parties"]:
            # Create L3 Other Parties
            for l3OtherParty in last_spt["l3_other_parties"]:
                l3OtherPartyNew = RSCITL3OtherParties(
                    z_record_id=str(uuid.uuid4()),
                    z_return_sheet_record_id=returnsheet_grid_new.Z_RECORD_ID,
                    z_taxpayer_name=l3OtherParty.z_taxpayer_name,
                    z_tin=l3OtherParty.z_tin,
                    z_tax_type=l3OtherParty.z_tax_type,
                    z_tax_base=l3OtherParty.z_tax_base,
                    z_income_tax=l3OtherParty.z_income_tax,
                    z_income_tax_usd=l3OtherParty.z_income_tax_usd,
                    z_withholding_slips_decimal=l3OtherParty.z_withholding_slips_decimal,
                    z_withholding_slips_date=l3OtherParty.z_withholding_slips_date,
                    z_is_deleted=l3OtherParty.z_is_deleted,
                    z_is_manually=l3OtherParty.z_is_manually,
                    z_withholdingslips_aggregate_identifier=l3OtherParty.z_withholdingslips_aggregate_identifier,
                    z_table_source=l3OtherParty.z_table_source,
                    z_last_updated_date=datetime.now(),
                    z_creation_date=datetime.now(),
                    z_is_migrated=l3OtherParty.z_is_migrated,
                    z_is_migrated_and_updated=l3OtherParty.z_is_migrated_and_updated
                )
                db.session.add(l3OtherPartyNew)

        if last_spt["l4_income_subject_to_finals"]:
            # Create L4 Income Subject To Final
            for l4IncomeSubjectToFinal in last_spt["l4_income_subject_to_finals"]:
                l4IncomeSubjectToFinalNew = RSCITL4IncomeSubjectToFinal(
                    z_record_id=str(uuid.uuid4()),
                    z_return_sheet_record_id=returnsheet_grid_new.Z_RECORD_ID,
                    z_tax_object_code=l4IncomeSubjectToFinal.z_tax_object_code,
                    z_tax_object=l4IncomeSubjectToFinal.z_tax_object,
                    z_tax_base=l4IncomeSubjectToFinal.z_tax_base,
                    z_tax_rate=l4IncomeSubjectToFinal.z_tax_rate,
                    z_income_tax=l4IncomeSubjectToFinal.z_income_tax,
                    z_income_tax_usd=l4IncomeSubjectToFinal.z_income_tax_usd,
                    z_is_deleted=l4IncomeSubjectToFinal.z_is_deleted,
                    z_is_manually=l4IncomeSubjectToFinal.z_is_manually,
                    z_withholdingslips_aggregate_identifier=l4IncomeSubjectToFinal.z_withholdingslips_aggregate_identifier,
                    z_table_source=l4IncomeSubjectToFinal.z_table_source,
                    z_last_updated_date=l4IncomeSubjectToFinal.z_last_updated_date,
                    z_creation_date=l4IncomeSubjectToFinal.z_creation_date,
                    z_is_migrated=l4IncomeSubjectToFinal.z_is_migrated,
                    z_is_migrated_and_updated=l4IncomeSubjectToFinal.z_is_migrated_and_updated,
                    z_tin=l4IncomeSubjectToFinal.z_tin,
                    z_name=l4IncomeSubjectToFinal.z_name,
                    z_tax_base_usd=l4IncomeSubjectToFinal.z_tax_base_usd
                )
                db.session.add(l4IncomeSubjectToFinalNew)

        if last_spt["l9_tangible_assets"]:
            # Create L9 Tangible Asset
            for l9TangibleAsset in last_spt["l9_tangible_assets"]:
                l9TangibleAssetNew = RSCITL9TangibleAsset(
                    z_record_id=str(uuid.uuid4()),
                    z_return_sheet_record_id=returnsheet_grid_new.Z_RECORD_ID,
                    z_group_type=l9TangibleAsset.z_group_type,
                    z_group_asset_type=l9TangibleAsset.z_group_asset_type,
                    z_month_year_acquisition=l9TangibleAsset.z_month_year_acquisition,
                    z_acquisition_price=l9TangibleAsset.z_acquisition_price,
                    z_remaining_beginning_value=l9TangibleAsset.z_remaining_beginning_value,
                    z_method_commercial=l9TangibleAsset.z_method_commercial,
                    z_method_fiscal=l9TangibleAsset.z_method_fiscal,
                    z_fiscal_year_value=l9TangibleAsset.z_fiscal_year_value,
                    z_notes=l9TangibleAsset.z_notes,
                    z_is_deleted=l9TangibleAsset.z_is_deleted,
                    z_is_manually=l9TangibleAsset.z_is_manually,
                    z_last_updated_date=l9TangibleAsset.z_last_updated_date,
                    z_creation_date=l9TangibleAsset.z_creation_date,
                    z_is_migrated=l9TangibleAsset.z_is_migrated,
                    z_is_migrated_and_updated=l9TangibleAsset.z_is_migrated_and_updated
                )
                db.session.add(l9TangibleAssetNew)

        if last_spt["l9_group_of_buildings"]:
            # Create L9 Group of Building
            for l9GroupOfBuilding in last_spt["l9_group_of_buildings"]:
                l9GroupOfBuildingNew = RSCITL9GroupOfBuilding(
                    z_record_id=str(uuid.uuid4()),
                    z_return_sheet_record_id=returnsheet_grid_new.Z_RECORD_ID,
                    z_group_type=l9GroupOfBuilding.z_group_type,
                    z_group_asset_type=l9GroupOfBuilding.z_group_asset_type,
                    z_month_year_acquisition=l9GroupOfBuilding.z_month_year_acquisition,
                    z_acquisition_price=l9GroupOfBuilding.z_acquisition_price,
                    z_remaining_beginning_value=l9GroupOfBuilding.z_remaining_beginning_value,
                    z_method_commercial=l9GroupOfBuilding.z_method_commercial,
                    z_method_fiscal=l9GroupOfBuilding.z_method_fiscal,
                    z_fiscal_year_value=l9GroupOfBuilding.z_fiscal_year_value,
                    z_notes=l9GroupOfBuilding.z_notes,
                    z_is_deleted=l9GroupOfBuilding.z_is_deleted,
                    z_is_manually=l9GroupOfBuilding.z_is_manually,
                    z_last_updated_date=l9GroupOfBuilding.z_last_updated_date,
                    z_creation_date=l9GroupOfBuilding.z_creation_date,
                    z_is_migrated=l9GroupOfBuilding.z_is_migrated,
                    z_is_migrated_and_updated=l9GroupOfBuilding.z_is_migrated_and_updated
                )
                db.session.add(l9GroupOfBuildingNew)

        if last_spt["l9_intangible_assets"]:
            # Create L9 Intangible Asset
            for l9IntangibleAsset in last_spt["l9_intangible_assets"]:
                l9IntangibleAssetNew = RSCITL9IntangibleAsset(
                    z_record_id=str(uuid.uuid4()),
                    z_return_sheet_record_id=returnsheet_grid_new.Z_RECORD_ID,
                    z_group_type=l9IntangibleAsset.z_group_type,
                    z_group_asset_type=l9IntangibleAsset.z_group_asset_type,
                    z_month_year_acquisition=l9IntangibleAsset.z_month_year_acquisition,
                    z_acquisition_price=l9IntangibleAsset.z_acquisition_price,
                    z_remaining_beginning_value=l9IntangibleAsset.z_remaining_beginning_value,
                    z_method_commercial=l9IntangibleAsset.z_method_commercial,
                    z_method_fiscal=l9IntangibleAsset.z_method_fiscal,
                    z_fiscal_year_value=l9IntangibleAsset.z_fiscal_year_value,
                    z_notes=l9IntangibleAsset.z_notes,
                    z_is_deleted=l9IntangibleAsset.z_is_deleted,
                    z_is_manually=l9IntangibleAsset.z_is_manually,
                    z_last_updated_date=l9IntangibleAsset.z_last_updated_date,
                    z_creation_date=l9IntangibleAsset.z_creation_date,
                    z_is_migrated=l9IntangibleAsset.z_is_migrated,
                    z_is_migrated_and_updated=l9IntangibleAsset.z_is_migrated_and_updated
                )
                db.session.add(l9IntangibleAssetNew)
    
        db.session.commit()
        return jsonify({"message": "success"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
        
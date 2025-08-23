from sqlalchemy import Null, desc
from app import db
from flask import jsonify, json
from app import db
from datetime import datetime
import uuid

from app.model.form_data import FormData
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
from app.utils.date_utils import parse_date, parse_payload_date

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

def amendment_returnsheet_service(tai, taxType, taxReturnPeriodType, taxYear, taxReturnModel):
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
            Z_SUBMIT_IN_PROGRESS_STATUS=last_spt["grid"].Z_SUBMIT_IN_PROGRESS_STATUS,
            Z_TIN=last_spt["grid"].Z_TIN,
            Z_NAME=last_spt["grid"].Z_NAME
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
        # set nilai UnderpaymentIncomeInAmended menjadi nilai dari spt sebelumnya
        constIncomeTaxMustPaid = last_spt["form_data"].get_main_form_value("IncomeTaxMustPaid")
        # returnsheet_form_data_new.set_main_form_value("IncomeTaxMustPaid",0)
        returnsheet_form_data_new.set_main_form_value("UnderpaymentIncomeInAmended",constIncomeTaxMustPaid)

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
                    z_withholding_slips_date=parse_date(l3OtherParty.z_withholding_slips_date),  # datetime.now(),
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
                    z_last_updated_date=datetime.now(),
                    z_creation_date=datetime.now(),
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
                    z_month_year_acquisition=parse_date(l9TangibleAsset.z_month_year_acquisition),  # l9TangibleAsset.z_month_year_acquisition,
                    z_acquisition_price=l9TangibleAsset.z_acquisition_price,
                    z_remaining_beginning_value=l9TangibleAsset.z_remaining_beginning_value,
                    z_method_commercial=l9TangibleAsset.z_method_commercial,
                    z_method_fiscal=l9TangibleAsset.z_method_fiscal,
                    z_fiscal_year_value=l9TangibleAsset.z_fiscal_year_value,
                    z_notes=l9TangibleAsset.z_notes,
                    z_is_deleted=l9TangibleAsset.z_is_deleted,
                    z_is_manually=l9TangibleAsset.z_is_manually,
                    z_last_updated_date=datetime.now(),
                    z_creation_date=datetime.now(),
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
                    z_month_year_acquisition=parse_date(l9GroupOfBuilding.z_month_year_acquisition),  # l9GroupOfBuilding.z_month_year_acquisition,
                    z_acquisition_price=l9GroupOfBuilding.z_acquisition_price,
                    z_remaining_beginning_value=l9GroupOfBuilding.z_remaining_beginning_value,
                    z_method_commercial=l9GroupOfBuilding.z_method_commercial,
                    z_method_fiscal=l9GroupOfBuilding.z_method_fiscal,
                    z_fiscal_year_value=l9GroupOfBuilding.z_fiscal_year_value,
                    z_notes=l9GroupOfBuilding.z_notes,
                    z_is_deleted=l9GroupOfBuilding.z_is_deleted,
                    z_is_manually=l9GroupOfBuilding.z_is_manually,
                    z_last_updated_date=datetime.now(),
                    z_creation_date=datetime.now(),
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
                    z_month_year_acquisition=parse_date(l9IntangibleAsset.z_month_year_acquisition),  # l9IntangibleAsset.z_month_year_acquisition,
                    z_acquisition_price=l9IntangibleAsset.z_acquisition_price,
                    z_remaining_beginning_value=l9IntangibleAsset.z_remaining_beginning_value,
                    z_method_commercial=l9IntangibleAsset.z_method_commercial,
                    z_method_fiscal=l9IntangibleAsset.z_method_fiscal,
                    z_fiscal_year_value=l9IntangibleAsset.z_fiscal_year_value,
                    z_notes=l9IntangibleAsset.z_notes,
                    z_is_deleted=l9IntangibleAsset.z_is_deleted,
                    z_is_manually=l9IntangibleAsset.z_is_manually,
                    z_last_updated_date=datetime.now(),
                    z_creation_date=datetime.now(),
                    z_is_migrated=l9IntangibleAsset.z_is_migrated,
                    z_is_migrated_and_updated=l9IntangibleAsset.z_is_migrated_and_updated
                )
                db.session.add(l9IntangibleAssetNew)
    
        db.session.commit()
        return jsonify({"message": "Amendment saved successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
def save_returnsheet_service(data, status):
    try:
        return_sheet_record_id = data.get("citrForm").get("Z_RECORD_ID")
        
        # ------- 1. Save to RS_RETURNSHEET_GRID -------
        grid = RSReturnsheetGrid.query.filter_by(Z_RECORD_ID=return_sheet_record_id).first()
        if grid:
            grid.Z_LAST_UPDATED_DATE = datetime.now()
            grid.Z_RETURN_SHEET_STATUS_CODE = status


        # ------- 2. Save to RS_RETURNSHEET_FORM_DATA -------
        rs_form_data = RSReturnsheetFormData.query.filter_by(z_record_id=return_sheet_record_id).first()
        if rs_form_data:
            rs_form_data.z_last_updated_date = datetime.now()


        # ---------- set signerposition ----------
        rs_form_data.set_main_form_value("SignerPosition", data.get("mainForm").get("SignerPosition"))

        # ---------- set L1cTreeData ----------
        rs_form_data.set_l1c_form_value("L1cTreeData", data.get("l1cForm").get("l1cGrid1data"))

        # ---------- set L1cTreeTotalRow ----------
        rs_form_data.set_l1c_form_value("L1cTreeTotalRow", data.get("l1cForm").get("l1cTreeTotalRow"))

        # ---------- set L1cAssets ----------
        rs_form_data.set_l1c_form_value("L1cAssets", data.get("l1cForm").get("l1cAssetsForm"))
        
        # ---------- set L1cLiabilitiesAndEquity ----------
        rs_form_data.set_l1c_form_value("L1cLiabilitiesAndEquity", data.get("l1cForm").get("l1cLiabilitiesAndEquityForm"))

        # ---------- set L2 ListOfShareholders ----------
        if data.get("l2Form").get("ListOfShareholders"):
            tes = rs_form_data.get_list_of_ownership_value("ListOfShareholders")
            rs_form_data.set_list_of_ownership_value("ListOfShareholders", data.get("l2Form").get("ListOfShareholders"))
            rs_form_data.set_list_of_ownership_value("TotalPaidInCapital", data.get("l2Form").get("TotalPaidInCapital"))
            rs_form_data.set_list_of_ownership_value("TotalPaidInCapitalPercentage", data.get("l2Form").get("TotalPaidInCapitalPercentage"))
            rs_form_data.set_list_of_ownership_value("TotalDividend", data.get("l2Form").get("TotalDividend"))

        # ---------- set L3 IncomeOverseas ----------
        if data.get("l3Form").get("IncomeOverseas"):
            for IncomeOversea in data.get("l3Form").get("IncomeOverseas"):
                IncomeOversea["DateOfTransaction"] = parse_payload_date(IncomeOversea["DateOfTransaction"])
            rs_form_data.set_list_income_tax_withheld_by_other_parties_value("IncomeOverseas", data.get("l3Form").get("IncomeOverseas"))
            rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OverseasTotalNetIncome", data.get("l3Form").get("OverseasTotalNetIncome"))
            rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OverseasTotalTaxPayable", data.get("l3Form").get("OverseasTotalTaxPayable"))
            rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OverseasTotalTaxCredit", data.get("l3Form").get("OverseasTotalTaxCredit"))
            rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OverseasRefundPreviousYear", data.get("l3Form").get("OverseasRefundPreviousYear"))
            rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OverseasTotalCalculatedCurrentYear", data.get("l3Form").get("OverseasTotalCalculatedCurrentYear"))
        
        rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OtherPartiesTotalTaxBase", data.get("l3Form").get("OtherPartiesTotalTaxBase"))
        rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OtherPartiesIncomeTaxWithheld", data.get("l3Form").get("OtherPartiesIncomeTaxWithheld"))
        rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OtherPartiesIncomeTaxWithheldUsd", data.get("l3Form").get("OtherPartiesIncomeTaxWithheldUsd"))
        rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OtherPartiesOverseasIncomeTax", data.get("l3Form").get("OtherPartiesOverseasIncomeTax"))
        rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OtherPartiesTotalCredit", data.get("l3Form").get("OtherPartiesTotalCredit"))
        rs_form_data.set_list_income_tax_withheld_by_other_parties_value("OtherPartiesTotalCreditUsd", data.get("l3Form").get("OtherPartiesTotalCreditUsd"))

        # ---------- set L4 ListOfIncomeSubjectToFinalTaxAndNonTaxableObject ----------
        if data.get("l4Form").get("ListOfIncomeSubjectToFinalTaxAndNonTaxableObject"):
            rs_form_data.set_list_of_income_subject_to_final_tax_and_non_taxable_object_value("TotalTaxBase", data.get("l4Form").get("ListOfIncomeSubjectToFinalTaxAndNonTaxableObject").get("TotalTaxBase"))
            rs_form_data.set_list_of_income_subject_to_final_tax_and_non_taxable_object_value("TotalFinalIncomeTaxPayable", data.get("l4Form").get("ListOfIncomeSubjectToFinalTaxAndNonTaxableObject").get("TotalFinalIncomeTaxPayable"))
            rs_form_data.set_list_of_income_subject_to_final_tax_and_non_taxable_object_value("TotalFinalIncomeTaxPayableUsd", data.get("l4Form").get("ListOfIncomeSubjectToFinalTaxAndNonTaxableObject").get("TotalFinalIncomeTaxPayableUsd"))
            rs_form_data.set_list_of_income_subject_to_final_tax_and_non_taxable_object_value("TotalGrossIncome", data.get("l4Form").get("ListOfIncomeSubjectToFinalTaxAndNonTaxableObject").get("TotalGrossIncome"))

        if data.get("l4Form").get("ListOfIncomeSubjectToFinalTaxAndNonTaxableObject").get("ListOfIncomeExcludedFromIncomeTax"):
            rs_form_data.set_list_of_income_subject_to_final_tax_and_non_taxable_object_value("ListOfIncomeExcludedFromIncomeTax", data.get("l4Form").get("ListOfIncomeSubjectToFinalTaxAndNonTaxableObject").get("ListOfIncomeExcludedFromIncomeTax"))

        # ---------- set L6 FiscalYearIncomeTax ----------
        if data.get("l6Form"):
            rs_form_data.set_fiscal_year_income_tax_value("IncomeAsTheBasisOfInstallment", data.get("l6Form").get("IncomeAsTheBasisOfInstallment"))
            rs_form_data.set_fiscal_year_income_tax_value("FiscalLossCompensation", data.get("l6Form").get("FiscalLossCompensation"))
            rs_form_data.set_fiscal_year_income_tax_value("TaxableIncome", data.get("l6Form").get("TaxableIncome"))
            rs_form_data.set_fiscal_year_income_tax_value("IncomeTaxPayable", data.get("l6Form").get("IncomeTaxPayable"))
            rs_form_data.set_fiscal_year_income_tax_value("TaxCreditWitheld", data.get("l6Form").get("TaxCreditWitheld"))
            rs_form_data.set_fiscal_year_income_tax_value("IncomeTaxSelfpaid", data.get("l6Form").get("IncomeTaxSelfpaid"))
            rs_form_data.set_fiscal_year_income_tax_value("FollowingFiscalYear", data.get("l6Form").get("FollowingFiscalYear"))

        # ---------- set L6 CalculationFacilitiesIncomeTaxRateReduction ----------
        if data.get("l8Form").get("CalculationFacilitiesIncomeTaxRateReduction"):
            rs_form_data.set_calculation_facilities_income_tax_rate_reduction_value("GrossTurnOver", data.get("l8Form").get("CalculationFacilitiesIncomeTaxRateReduction").get("GrossTurnOver"))
            rs_form_data.set_calculation_facilities_income_tax_rate_reduction_value("TaxableIncomeShareOfGrossCirculationGrantedFacility", data.get("l8Form").get("CalculationFacilitiesIncomeTaxRateReduction").get("GrossTurnOver"))
            rs_form_data.set_calculation_facilities_income_tax_rate_reduction_value("TaxableIncomeShareOfGrossCirculationNotGrantedFacility", data.get("l8Form").get("CalculationFacilitiesIncomeTaxRateReduction").get("GrossTurnOver"))
            rs_form_data.set_calculation_facilities_income_tax_rate_reduction_value("IncomeTaxPayableFromTaxableIncomeShareOfGrossCirculationGrantedFacility", data.get("l8Form").get("CalculationFacilitiesIncomeTaxRateReduction").get("GrossTurnOver"))
            rs_form_data.set_calculation_facilities_income_tax_rate_reduction_value("IncomeTaxPayableFromTaxableIncomeShareOfGrossCirculationNotGrantedFacility", data.get("l8Form").get("CalculationFacilitiesIncomeTaxRateReduction").get("GrossTurnOver"))
            rs_form_data.set_calculation_facilities_income_tax_rate_reduction_value("TotalIncomeTax", data.get("l8Form").get("CalculationFacilitiesIncomeTaxRateReduction").get("GrossTurnOver"))
        
        # ---------- set L9 Form RecapitulationFiscalDepreciationAmortization ----------
        if data.get("l9Form").get("L9Form").get("RecapitulationFiscalDepreciationAmortization"):
            rs_form_data.set_l9_form_value("TotalFiscalDepreciationTangible", data.get("l9Form").get("L9Form").get("TotalFiscalDepreciationTangible")) # TotalFiscalDepreciationTangible
            rs_form_data.set_l9_form_value("TotalCommercialDepreciationTangible", data.get("l9Form").get("L9Form").get("TotalCommercialDepreciationTangible")) # TotalCommercialDepreciationTangible
            rs_form_data.set_l9_form_value("DiferencesDepreciationTangible", data.get("l9Form").get("L9Form").get("DiferencesDepreciationTangible")) # DiferencesDepreciationTangible
            rs_form_data.set_l9_form_value("TotalFiscalAmortization", data.get("l9Form").get("L9Form").get("TotalFiscalAmortization")) # TotalFiscalAmortization
            rs_form_data.set_l9_form_value("TotalCommercialAmortization", data.get("l9Form").get("L9Form").get("TotalCommercialAmortization")) # TotalCommercialAmortization
            rs_form_data.set_l9_form_value("DiferencesAmortization", data.get("l9Form").get("L9Form").get("DiferencesAmortization")) # DiferencesAmortization
            rs_form_data.set_l9_form_value("TotalTable1", data.get("l9Form").get("L9Form").get("TotalTable1")) # TotalTable1
            rs_form_data.set_l9_form_value("TotalTable2", data.get("l9Form").get("L9Form").get("TotalTable2")) # TotalTable2
            rs_form_data.set_l9_form_value("TotalTable3", data.get("l9Form").get("L9Form").get("TotalTable3")) # TotalTable3
            rs_form_data.set_l9_form_value("TotalTable4", data.get("l9Form").get("L9Form").get("TotalTable4")) # TotalTable4
            rs_form_data.set_l9_form_value("TotalTable5", data.get("l9Form").get("L9Form").get("TotalTable5")) # TotalTable5
            rs_form_data.set_l9_form_value("TotalTable6", data.get("l9Form").get("L9Form").get("TotalTable6")) # TotalTable6
            rs_form_data.set_l9_form_value("TotalTable7", data.get("l9Form").get("L9Form").get("TotalTable7")) # TotalTable7
            rs_form_data.set_l9_form_value("TotalTable8", data.get("l9Form").get("L9Form").get("TotalTable8")) # TotalTable8
            rs_form_data.set_l9_form_value("TotalTable9", data.get("l9Form").get("L9Form").get("TotalTable9")) # TotalTable9
            rs_form_data.set_l9_form_value("TotalTable10", data.get("l9Form").get("L9Form").get("TotalTable10")) # TotalTable10
            rs_form_data.set_l9_form_value("TotalTable11", data.get("l9Form").get("L9Form").get("TotalTable11")) # TotalTable11
            rs_form_data.set_l9_form_value("TotalTable12", data.get("l9Form").get("L9Form").get("TotalTable12")) # TotalTable12

        # ---------- set L11B Form ----------
        if data.get("l11bForm").get("L11BForm"):
            rs_form_data.set_l11b_form_value("CommercialNettIncome", data.get("l11bForm").get("L11BForm").get("CommercialNettIncome"))
            rs_form_data.set_l11b_form_value("DepreciationAndAmortizationExpenses", data.get("l11bForm").get("L11BForm").get("DepreciationAndAmortizationExpenses"))
            rs_form_data.set_l11b_form_value("IncomeTaxExpense", data.get("l11bForm").get("L11BForm").get("IncomeTaxExpense"))
            rs_form_data.set_l11b_form_value("BorrowingCostExpense", data.get("l11bForm").get("L11BForm").get("BorrowingCostExpense"))
            rs_form_data.set_l11b_form_value("Ebitda", data.get("l11bForm").get("L11BForm").get("Ebitda"))
            rs_form_data.set_l11b_form_value("Ebitda25", data.get("l11bForm").get("L11BForm").get("Ebitda25"))

        if data.get("l11bForm").get("BorrowingCosts"):
            rs_form_data.set_l11b_form_value("BorrowingCosts", data.get("l11bForm").get("BorrowingCosts"))

        if data.get("l11bForm").get("TotalBorrowingCosts"):
            rs_form_data.set_l11b_form_value("TotalBorrowingCosts", data.get("l11bForm").get("TotalBorrowingCosts"))

        # ---------- set Main Form ----------
        if data.get("mainForm"):
            # rs_form_data.set_main_form_value("TaxYear", data.get("mainForm").get("TaxYear")) # TaxYear
            # rs_form_data.set_main_form_value("Status", data.get("mainForm").get("Status")) # Status
            # rs_form_data.set_main_form_value("AccountingPeriodStart", data.get("mainForm").get("AccountingPeriodStart")) # Status
            # rs_form_data.set_main_form_value("AccountingPeriodEnd", data.get("mainForm").get("AccountingPeriodEnd")) # Status
            rs_form_data.set_main_form_value("AccountingMethod", data.get("mainForm").get("AccountingMethod")) # Status
            # rs_form_data.set_main_form_value("Tin", data.get("mainForm").get("Tin")) # Status
            # rs_form_data.set_main_form_value("Name", data.get("mainForm").get("Name")) # Status
            # rs_form_data.set_main_form_value("EmailAddress", data.get("mainForm").get("EmailAddress")) # Status
            # rs_form_data.set_main_form_value("PhoneNumber", data.get("mainForm").get("PhoneNumber")) # Status
            rs_form_data.set_main_form_value("BusinessClassification", data.get("mainForm").get("BusinessClassification")) # Status
            rs_form_data.set_main_form_value("AuditedFinancialStatements", data.get("mainForm").get("AuditedFinancialStatements")) # Status
            rs_form_data.set_main_form_value("AuditorOpinion", data.get("mainForm").get("AuditorOpinion")) # Status
            rs_form_data.set_main_form_value("TinAccountant", data.get("mainForm").get("TinAccountant")) # Status
            rs_form_data.set_main_form_value("NameAccountant", data.get("mainForm").get("NameAccountant")) # Status
            rs_form_data.set_main_form_value("IsIncomeUnder", data.get("mainForm").get("IsIncomeUnder")) # Status
            rs_form_data.set_main_form_value("IsIncomeSolely", data.get("mainForm").get("IsIncomeSolely")) # Status
            rs_form_data.set_main_form_value("IsIncomeSubject", data.get("mainForm").get("IsIncomeSubject")) # Status
            rs_form_data.set_main_form_value("TotalIncomeSubject", data.get("mainForm").get("TotalIncomeSubject")) # Status
            rs_form_data.set_main_form_value("IsIncomeExcluded", data.get("mainForm").get("IsIncomeExcluded")) # Status
            rs_form_data.set_main_form_value("TotalIncomeExcluded", data.get("mainForm").get("TotalIncomeExcluded")) # Status
            rs_form_data.set_main_form_value("NetIncomeBeforeTax", data.get("mainForm").get("NetIncomeBeforeTax")) # Status
            rs_form_data.set_main_form_value("IsNetIncomeReduction", data.get("mainForm").get("IsNetIncomeReduction")) # Status
            rs_form_data.set_main_form_value("TotalNetIncomeReduction", data.get("mainForm").get("TotalNetIncomeReduction")) # Status
            rs_form_data.set_main_form_value("IsGrossIncomeVocational", data.get("mainForm").get("IsGrossIncomeVocational")) # Status
            rs_form_data.set_main_form_value("TotalGrossIncomeVocational", data.get("mainForm").get("TotalGrossIncomeVocational")) # Status
            rs_form_data.set_main_form_value("FiscalNetIncomeAfterTax", data.get("mainForm").get("FiscalNetIncomeAfterTax")) # Status
            rs_form_data.set_main_form_value("IsCarriedForward", data.get("mainForm").get("IsCarriedForward")) # Status
            rs_form_data.set_main_form_value("TotalCarriedForward", data.get("mainForm").get("TotalCarriedForward")) # Status
            rs_form_data.set_main_form_value("TaxableIncome", data.get("mainForm").get("TaxableIncome")) # Status
            rs_form_data.set_main_form_value("IsGrossIncomeResearch", data.get("mainForm").get("IsGrossIncomeResearch")) # Status
            rs_form_data.set_main_form_value("TotalGrossIncomeResearch", data.get("mainForm").get("TotalGrossIncomeResearch")) # Status
            rs_form_data.set_main_form_value("TaxRate", data.get("mainForm").get("TaxRate")) # Status
            rs_form_data.set_main_form_value("IncomeTaxInAYear", data.get("mainForm").get("IncomeTaxInAYear")) # Status
            rs_form_data.set_main_form_value("IsIncomeTaxOverseas", data.get("mainForm").get("IsIncomeTaxOverseas")) # Status
            rs_form_data.set_main_form_value("TotalIncomeTaxOverseas", data.get("mainForm").get("TotalIncomeTaxOverseas")) # Status
            rs_form_data.set_main_form_value("InstallmentOfIncome", data.get("mainForm").get("InstallmentOfIncome")) # Status
            rs_form_data.set_main_form_value("NoticeOfCollection", data.get("mainForm").get("NoticeOfCollection")) # Status
            rs_form_data.set_main_form_value("IsIncomeTaxDeduction", data.get("mainForm").get("IsIncomeTaxDeduction")) # Status
            rs_form_data.set_main_form_value("TotalIncomeTaxDeduction", data.get("mainForm").get("TotalIncomeTaxDeduction")) # Status
            rs_form_data.set_main_form_value("UnderpaymentIncomeTax", data.get("mainForm").get("UnderpaymentIncomeTax")) # Status
            rs_form_data.set_main_form_value("IsApprovalInstallment", data.get("mainForm").get("IsApprovalInstallment")) # Status
            rs_form_data.set_main_form_value("TotalApprovalInstallment", data.get("mainForm").get("TotalApprovalInstallment")) # Status
            rs_form_data.set_main_form_value("IncomeTaxMustPaid", data.get("mainForm").get("IncomeTaxMustPaid")) # Status
            rs_form_data.set_main_form_value("UnderpaymentIncomeInAmended", data.get("mainForm").get("UnderpaymentIncomeInAmended")) # Status
            rs_form_data.set_main_form_value("UnderpaymentIncomeDueAmended", data.get("mainForm").get("UnderpaymentIncomeDueAmended")) # Status
            rs_form_data.set_main_form_value("OverpaymentIncomeTax", data.get("mainForm").get("OverpaymentIncomeTax")) # Status
            rs_form_data.set_main_form_value("BankAccount", data.get("mainForm").get("BankAccount")) # Status
            rs_form_data.set_main_form_value("AccountNumber", data.get("mainForm").get("AccountNumber")) # Status
            rs_form_data.set_main_form_value("BankCode", data.get("mainForm").get("BankCode")) # Status
            rs_form_data.set_main_form_value("BankName", data.get("mainForm").get("BankName")) # Status
            rs_form_data.set_main_form_value("AccountHolderName", data.get("mainForm").get("AccountHolderName")) # Status
            rs_form_data.set_main_form_value("IsCriteriaObligatedSubmit", data.get("mainForm").get("IsCriteriaObligatedSubmit")) # Status
            rs_form_data.set_main_form_value("TotalCriteriaObligatedSubmit", data.get("mainForm").get("TotalCriteriaObligatedSubmit")) # Status
            rs_form_data.set_main_form_value("IsTransactionWithRelated", data.get("mainForm").get("IsTransactionWithRelated")) # Status
            rs_form_data.set_main_form_value("IsObligationTransferPricing", data.get("mainForm").get("IsObligationTransferPricing")) # Status
            rs_form_data.set_main_form_value("IsCapitalInvestmentAffilated", data.get("mainForm").get("IsCapitalInvestmentAffilated")) # Status
            rs_form_data.set_main_form_value("IsDebtFromShareholders", data.get("mainForm").get("IsDebtFromShareholders")) # Status
            rs_form_data.set_main_form_value("IsDeclareFiscalDepreciation", data.get("mainForm").get("IsDeclareFiscalDepreciation")) # Status
            rs_form_data.set_main_form_value("IsDeclareEntertainmentExpense", data.get("mainForm").get("IsDeclareEntertainmentExpense")) # Status
            rs_form_data.set_main_form_value("IsInvestmentOtherIncome", data.get("mainForm").get("IsInvestmentOtherIncome")) # Status
            rs_form_data.set_main_form_value("IsRemainingExcess", data.get("mainForm").get("IsRemainingExcess")) # Status
            rs_form_data.set_main_form_value("IsReceiveDividendIncome", data.get("mainForm").get("IsReceiveDividendIncome")) # Status
            rs_form_data.set_main_form_value("ExcessOfFinalIncome", data.get("mainForm").get("ExcessOfFinalIncome")) # Status
            rs_form_data.set_main_form_value("CheckboxDeclaration", data.get("mainForm").get("CheckboxDeclaration")) # Status
            rs_form_data.set_main_form_value("SignBy", data.get("mainForm").get("SignBy")) # Status
            rs_form_data.set_main_form_value("SignerTin", data.get("mainForm").get("SignerTin")) # Status
            rs_form_data.set_main_form_value("SignerName", data.get("mainForm").get("SignerName")) # Status
            rs_form_data.set_main_form_value("SignerPosition", data.get("mainForm").get("SignerPosition")) # Status
            rs_form_data.set_main_form_value("AskForReplacement", data.get("mainForm").get("AskForReplacement")) # Status
            rs_form_data.set_main_form_value("AuditOpinionPdf", data.get("mainForm").get("AuditOpinionPdf")) # Status
            rs_form_data.set_main_form_value("CalculationAfterTaxPdf", data.get("mainForm").get("CalculationAfterTaxPdf")) # Status
            rs_form_data.set_main_form_value("CalculationCreditedIncomePdf", data.get("mainForm").get("CalculationCreditedIncomePdf")) # Status
            rs_form_data.set_main_form_value("ConsolidatedFinancialPdf", data.get("mainForm").get("ConsolidatedFinancialPdf")) # Status
            rs_form_data.set_main_form_value("DateOfSubmit", data.get("mainForm").get("DateOfSubmit")) # Status
            rs_form_data.set_main_form_value("ElectronicReceiptPdf", data.get("mainForm").get("ElectronicReceiptPdf")) # Status
            rs_form_data.set_main_form_value("FinancialForeignPdf", data.get("mainForm").get("FinancialForeignPdf")) # Status
            rs_form_data.set_main_form_value("FinancialStatementPdf", data.get("mainForm").get("FinancialStatementPdf")) # Status
            rs_form_data.set_main_form_value("FinancialStatementXls", data.get("mainForm").get("FinancialStatementXls")) # Status
            rs_form_data.set_main_form_value("IncomeTaxForeignPdf", data.get("mainForm").get("IncomeTaxForeignPdf")) # Status
            rs_form_data.set_main_form_value("IsIncomeTaxOverseasWithholding", data.get("mainForm").get("IsIncomeTaxOverseasWithholding")) # Status
            rs_form_data.set_main_form_value("IsReceiveDividendIncomeNumber", data.get("mainForm").get("IsReceiveDividendIncomeNumber")) # Status
            rs_form_data.set_main_form_value("IsUnderPSCGrossSplitScheme", data.get("mainForm").get("IsUnderPSCGrossSplitScheme")) # Status
            rs_form_data.set_main_form_value("MonthlyReportPdf", data.get("mainForm").get("MonthlyReportPdf")) # Status
            rs_form_data.set_main_form_value("OrderDocumentsPdf", data.get("mainForm").get("OrderDocumentsPdf")) # Status
            rs_form_data.set_main_form_value("PercentageOfTaxRate", data.get("mainForm").get("PercentageOfTaxRate")) # Status
            rs_form_data.set_main_form_value("ProofOfIncomePdf", data.get("mainForm").get("ProofOfIncomePdf")) # Status
            rs_form_data.set_main_form_value("ProofOfReinvestmentPdf", data.get("mainForm").get("ProofOfReinvestmentPdf")) # Status
            rs_form_data.set_main_form_value("ProofOfZakatPdf", data.get("mainForm").get("ProofOfZakatPdf")) # Status
            rs_form_data.set_main_form_value("ReplacementPrevious", data.get("mainForm").get("ReplacementPrevious")) # Status
            rs_form_data.set_main_form_value("ReportOfShareholderPdf", data.get("mainForm").get("ReportOfShareholderPdf")) # Status
            rs_form_data.set_main_form_value("WithholdingSlipPdf", data.get("mainForm").get("WithholdingSlipPdf")) # Status

        # ---------- set Financial Statement ----------
        if data.get("FinancialStatement"):
            for r in data.get("FinancialStatement"):
                
                if not r.get("DocumentAggregateIdentifier"):
                    # rs_form_data.set_financial_statement_value("DocumentAggregateIdentifier", data.get("FinancialStatement").get("DocumentAggregateIdentifier"))
                    r.update({"DocumentAggregateIdentifier": str(uuid.uuid4())})
                # else:
            #         rs_form_data.set_financial_statement_value("DocumentAggregateIdentifier", str(uuid.uuid4())) # DocumentAggregateIdentifier
            # rs_form_data.set_financial_statement_value("DocumentId", data.get("FinancialStatement").get("DocumentId"))
            # rs_form_data.set_financial_statement_value("DocumentType", data.get("FinancialStatement").get("DocumentType"))
            # rs_form_data.set_financial_statement_value("FileName", data.get("FinancialStatement").get("FileName"))
            
            rs_form_data.set_financial_statement(data.get("FinancialStatement"))

        # ------- 3. Save to RS_L3_OTHER_PARTIES -------
        # a. Extract all IDs from payload
        l3_payload_ids = {
            item["z_record_id"]
            for item in data.get("l3Form", {}).get("L3OtherParties", [])
            if item.get("z_record_id")
        }

        # b. Fetch all records currently in DB
        l3_existing_records = RSCITL3OtherParties.query.filter_by(
            z_return_sheet_record_id=return_sheet_record_id, 
            z_is_deleted=0
        ).all()
        l3_existing_ids = {r.z_record_id for r in l3_existing_records}

        for l3_other_party in data.get("l3Form").get("L3OtherParties",[]):
            z_record_id = l3_other_party.get("z_record_id")
            
            # If no record_id in payload → generate new one
            if not z_record_id:
                z_record_id = str(uuid.uuid4())
                l3_other_party["z_record_id"] = z_record_id

            # c. Find existing record
            existing = next((r for r in l3_existing_records if r.z_record_id == z_record_id), None)
            
            # d. Update existing record
            if existing:
                existing.z_taxpayer_name = l3_other_party.get("z_taxpayer_name")
                existing.z_tin = l3_other_party.get("z_tin")
                existing.z_tax_type = l3_other_party.get("z_tax_type")
                existing.z_tax_base = l3_other_party.get("z_tax_base")
                existing.z_income_tax = l3_other_party.get("z_income_tax")
                existing.z_income_tax_usd = l3_other_party.get("z_income_tax_usd")
                existing.z_withholding_slips_decimal = l3_other_party.get("z_withholding_slips_decimal")
                existing.z_withholding_slips_date = parse_date(l3_other_party.get("z_withholding_slips_date"))
                existing.z_last_updated_date = datetime.now()
            
            # e. Create new record
            else:
                new = RSCITL3OtherParties(
                    z_record_id = z_record_id,
                    z_return_sheet_record_id = return_sheet_record_id,
                    z_taxpayer_name = l3_other_party.get("z_taxpayer_name"),
                    z_tin = l3_other_party.get("z_tin"),
                    z_tax_type = l3_other_party.get("z_tax_type"),
                    z_tax_base = l3_other_party.get("z_tax_base"),
                    z_income_tax = l3_other_party.get("z_income_tax"),
                    z_income_tax_usd = l3_other_party.get("z_income_tax_usd"),
                    z_withholding_slips_decimal = l3_other_party.get("z_withholding_slips_decimal"),
                    z_withholding_slips_date = parse_date(l3_other_party.get("z_withholding_slips_date")),
                    z_is_deleted = 0,
                    z_is_manually = 1,
                    z_withholdingslips_aggregate_identifier = Null,
                    z_table_source = Null,
                    z_last_updated_date = datetime.now(),
                    z_creation_date = datetime.now(),
                    z_is_migrated = 0,
                    z_is_migrated_and_updated = 0
                )
                db.session.add(new)
        
        # f. Handle deletes (records in DB but not in payload)
        to_delete_l3 = [r for r in l3_existing_records if r.z_record_id not in l3_payload_ids]
        for record in to_delete_l3:
            record.z_is_deleted = 1
        

        # ------- 4. Save to RS_L4_INCOME_SUBJECT_TO_FINAL -------
        # a. Extract all IDs from payload
        l4_payload_ids = {
            item["z_record_id"] 
            for item in data.get("l4Form", {}).get("L4IncomeSubjectToFinal", [])
            if item.get("z_record_id")    
        }

        # b. Fetch all records currently in DB
        # l4_existing_records = RSCITL4IncomeSubjectToFinal.query.filter_by(z_return_sheet_record_id=return_sheet_record_id, z_is_deleted=0).all()
        l4_existing_records = RSCITL4IncomeSubjectToFinal.query.filter_by(
            z_return_sheet_record_id=return_sheet_record_id, 
            z_is_deleted=0
        ).all()
        l4_existing_ids = {r.z_record_id for r in l4_existing_records}

        for l4_income_subject_to_final in data.get("l4Form").get("L4IncomeSubjectToFinal",[]):
            z_record_id = l4_income_subject_to_final.get("z_record_id")

            # If no record_id in payload → generate new one
            if not z_record_id:
                z_record_id = str(uuid.uuid4())
                l4_income_subject_to_final["z_record_id"] = z_record_id

            # c. Find existing record
            existing = next((r for r in l4_existing_records if r.z_record_id == z_record_id), None)
            
            # d. Update existing record
            if existing:
                existing.z_tax_base = l4_income_subject_to_final.get("z_tax_base")
                existing.z_tax_base_usd = l4_income_subject_to_final.get("z_tax_base_usd")
                existing.z_tax_rate = l4_income_subject_to_final.get("z_tax_rate")
                existing.z_income_tax = l4_income_subject_to_final.get("z_income_tax")
                existing.z_income_tax_usd = l4_income_subject_to_final.get("z_income_tax_usd")
                existing.z_last_updated_date = datetime.now()
            
            # e. Create new record
            else:
                new = RSCITL4IncomeSubjectToFinal(
                    z_record_id = z_record_id,
                    z_return_sheet_record_id = return_sheet_record_id,
                    z_tax_object_code = l4_income_subject_to_final.get("z_tax_object_code"),
                    z_tax_object = l4_income_subject_to_final.get("z_tax_object"),
                    z_tax_base = l4_income_subject_to_final.get("z_tax_base"),
                    z_tax_rate = l4_income_subject_to_final.get("z_tax_rate"),
                    z_income_tax = l4_income_subject_to_final.get("z_income_tax"),
                    z_income_tax_usd = l4_income_subject_to_final.get("z_income_tax"),
                    z_is_deleted = int(l4_income_subject_to_final.get("z_is_deleted")),
                    z_is_manually = int(l4_income_subject_to_final.get("z_is_manually")),
                    z_withholdingslips_aggregate_identifier = str(uuid.uuid4()),
                    z_table_source = l4_income_subject_to_final.get("z_table_source"),
                    z_last_updated_date = datetime.now(),
                    z_creation_date = datetime.now(),
                    z_is_migrated = int(l4_income_subject_to_final.get("z_is_migrated")),
                    z_is_migrated_and_updated = int(l4_income_subject_to_final.get("z_is_migrated_and_updated")),
                    z_tin = l4_income_subject_to_final.get("z_tin"),
                    z_name = l4_income_subject_to_final.get("z_name"),
                    z_tax_base_usd = l4_income_subject_to_final.get("z_tax_base")
                )
                db.session.add(new)
        
        # f. Handle deletes (records in DB but not in payload)
        to_delete_l4 = [r for r in l4_existing_records if r.z_record_id not in l4_payload_ids]
        for record in to_delete_l4:
            record.z_is_deleted = 1


        # ------- 5. Save to RS_L9_TANGIBLE_ASSET -------
        # a. Extract all IDs from payload
        l9_tangible_asset_payload_ids = {item["z_record_id"] for item in data.get("l9Form").get("L9TangibleAsset")}

        # b. Fetch all records currently in DB
        l9_tangible_asset_existing_records = RSCITL9TangibleAsset.query.filter_by(z_return_sheet_record_id=return_sheet_record_id, z_is_deleted=0).all()
        l9_tangible_asset_existing_ids = {l9_tangible_asset_record.z_record_id for l9_tangible_asset_record in l9_tangible_asset_existing_records}

        for l9_tangible_asset in data.get("l9Form").get("L9TangibleAsset"):
            z_record_id = l9_tangible_asset.get("z_record_id")

            # c. Find existing record
            existing = RSCITL9TangibleAsset.query.filter_by(z_record_id=z_record_id).first()
            
            # d. Update existing record
            if existing:
                existing.z_group_asset_type = l9_tangible_asset.get("z_group_asset_type")
                existing.z_month_year_acquisition = parse_date(l9_tangible_asset.get("z_month_year_acquisition"))
                existing.z_acquisition_price = l9_tangible_asset.get("z_acquisition_price")
                existing.z_remaining_beginning_value = l9_tangible_asset.get("z_remaining_beginning_value")
                existing.z_method_commercial = l9_tangible_asset.get("z_method_commercial")
                existing.z_method_fiscal = l9_tangible_asset.get("z_method_fiscal")
                existing.z_fiscal_year_value = l9_tangible_asset.get("z_fiscal_year_value")
                existing.z_notes = l9_tangible_asset.get("z_notes")
                existing.z_last_updated_date = datetime.now()
            
            # e. Create new record
            else:
                new = RSCITL9TangibleAsset(
                    z_record_id = str(uuid.uuid4()),
                    z_return_sheet_record_id = return_sheet_record_id,
                    z_group_type = l9_tangible_asset.get("z_group_type"),
                    z_group_asset_type = l9_tangible_asset.get("z_group_asset_type"),
                    z_month_year_acquisition = parse_date(l9_tangible_asset.get("z_month_year_acquisition")),
                    z_acquisition_price = l9_tangible_asset.get("z_acquisition_price"),
                    z_remaining_beginning_value = l9_tangible_asset.get("z_remaining_beginning_value"),
                    z_method_commercial = l9_tangible_asset.get("z_method_commercial"),
                    z_method_fiscal = l9_tangible_asset.get("z_method_fiscal"),
                    z_fiscal_year_value = l9_tangible_asset.get("z_fiscal_year_value"),
                    z_notes = l9_tangible_asset.get("z_notes"),
                    z_is_deleted = l9_tangible_asset.get("z_is_deleted"),
                    z_is_manually = l9_tangible_asset.get("z_is_manually"),
                    z_last_updated_date = datetime.now(),
                    z_creation_date = datetime.now(),
                    z_is_migrated = l9_tangible_asset.get("z_is_migrated"),
                    z_is_migrated_and_updated = l9_tangible_asset.get("z_is_migrated_and_updated")
                )
                db.session.add(new)

        # f. Handle deletes (records in DB but not in payload)
        to_delete_l9_tangible_asset = [r for r in l9_tangible_asset_existing_records if r.z_record_id not in l9_tangible_asset_payload_ids]
        for record in to_delete_l9_tangible_asset:
            record.z_is_deleted = 1


        # ------- 6. Save to RS_L9_GROUP_OF_BUILDING -------
        # a. Extract all IDs from payload
        l9_group_of_building_payload_ids = {item["z_record_id"] for item in data.get("l9Form").get("L9GroupOfBuilding")}

        # b. Fetch all records currently in DB
        l9_group_of_building_existing_records = RSCITL9GroupOfBuilding.query.filter_by(z_return_sheet_record_id=return_sheet_record_id, z_is_deleted=0).all()
        l9_group_of_building_existing_ids = {l9_group_of_building_record.z_record_id for l9_group_of_building_record in l9_group_of_building_existing_records}

        for l9_group_of_building in data.get("l9Form").get("L9GroupOfBuilding"):
            z_record_id = l9_group_of_building.get("z_record_id")

            # c. Find existing record
            existing = RSCITL9GroupOfBuilding.query.filter_by(z_record_id=z_record_id).first()
            
            # d. Update existing record
            if existing:
                existing.z_group_asset_type = l9_group_of_building.get("z_group_asset_type")
                existing.z_month_year_acquisition = parse_date(l9_group_of_building.get("z_month_year_acquisition"))
                existing.z_acquisition_price = l9_group_of_building.get("z_acquisition_price")
                existing.z_remaining_beginning_value = l9_group_of_building.get("z_remaining_beginning_value")
                existing.z_method_commercial = l9_group_of_building.get("z_method_commercial")
                existing.z_method_fiscal = l9_group_of_building.get("z_method_fiscal")
                existing.z_fiscal_year_value = l9_group_of_building.get("z_fiscal_year_value")
                existing.z_notes = l9_group_of_building.get("z_notes")
                existing.z_last_updated_date = datetime.now()
            
            # e. Create new record
            else:
                new = RSCITL9GroupOfBuilding(
                    z_record_id = str(uuid.uuid4()),
                    z_return_sheet_record_id = return_sheet_record_id,
                    z_group_type = l9_group_of_building.get("z_group_type"),
                    z_group_asset_type = l9_group_of_building.get("z_group_asset_type"),
                    z_month_year_acquisition = parse_date(l9_group_of_building.get("z_month_year_acquisition")),
                    z_acquisition_price = l9_group_of_building.get("z_acquisition_price"),
                    z_remaining_beginning_value = l9_group_of_building.get("z_remaining_beginning_value"),
                    z_method_commercial = l9_group_of_building.get("z_method_commercial"),
                    z_method_fiscal = l9_group_of_building.get("z_method_fiscal"),
                    z_fiscal_year_value = l9_group_of_building.get("z_fiscal_year_value"),
                    z_notes = l9_group_of_building.get("z_notes"),
                    z_is_deleted = l9_group_of_building.get("z_is_deleted"),
                    z_is_manually = l9_group_of_building.get("z_is_manually"),
                    z_last_updated_date = datetime.now(),
                    z_creation_date = datetime.now(),
                    z_is_migrated = l9_group_of_building.get("z_is_migrated"),
                    z_is_migrated_and_updated = l9_group_of_building.get("z_is_migrated_and_updated"),
                )
                db.session.add(new)

        # f. Handle deletes (records in DB but not in payload)
        to_delete_l9_group_of_building = [r for r in l9_group_of_building_existing_records if r.z_record_id not in l9_group_of_building_payload_ids]
        for record in to_delete_l9_group_of_building:
            record.z_is_deleted = 1


        # ------- 7. Save to RS_L9_INTANGIBLE_ASSET -------
        # a. Extract all IDs from payload
        l9_intangible_asset_payload_ids = {item["z_record_id"] for item in data.get("l9Form").get("L9IntangibleAsset")}

        # b. Fetch all records currently in DB
        l9_intangible_asset_existing_records = RSCITL9IntangibleAsset.query.filter_by(z_return_sheet_record_id=return_sheet_record_id, z_is_deleted=0).all()
        l9_intangible_asset_existing_ids = {l9_intangible_asset_record.z_record_id for l9_intangible_asset_record in l9_intangible_asset_existing_records}

        for l9_intangible_asset in data.get("l9Form").get("L9IntangibleAsset"):
            z_record_id = l9_intangible_asset.get("z_record_id")

            # c. Find existing record
            existing = RSCITL9IntangibleAsset.query.filter_by(z_record_id=z_record_id).first()
            
            # d. Update existing record
            if existing:
                existing.z_group_asset_type = l9_intangible_asset.get("z_group_asset_type")
                existing.z_month_year_acquisition = parse_date(l9_intangible_asset.get("z_month_year_acquisition"))
                existing.z_acquisition_price = l9_intangible_asset.get("z_acquisition_price")
                existing.z_remaining_beginning_value = l9_intangible_asset.get("z_remaining_beginning_value")
                existing.z_method_commercial = l9_intangible_asset.get("z_method_commercial")
                existing.z_method_fiscal = l9_intangible_asset.get("z_method_fiscal")
                existing.z_fiscal_year_value = l9_intangible_asset.get("z_fiscal_year_value")
                existing.z_notes = l9_intangible_asset.get("z_notes")
                existing.z_last_updated_date = datetime.now()
            
            # e. Create new record
            else:
                new = RSCITL9IntangibleAsset(
                    z_record_id = str(uuid.uuid4()),
                    z_return_sheet_record_id = return_sheet_record_id,
                    z_group_type = l9_intangible_asset.get("z_group_type"),
                    z_group_asset_type = l9_intangible_asset.get("z_group_asset_type"),
                    z_month_year_acquisition = parse_date(l9_intangible_asset.get("z_month_year_acquisition")),
                    z_acquisition_price = l9_intangible_asset.get("z_acquisition_price"),
                    z_remaining_beginning_value = l9_intangible_asset.get("z_remaining_beginning_value"),
                    z_method_commercial = l9_intangible_asset.get("z_method_commercial"),
                    z_method_fiscal = l9_intangible_asset.get("z_method_fiscal"),
                    z_fiscal_year_value = l9_intangible_asset.get("z_fiscal_year_value"),
                    z_notes = l9_intangible_asset.get("z_notes"),
                    z_is_deleted = l9_intangible_asset.get("z_is_deleted"),
                    z_is_manually = l9_intangible_asset.get("z_is_manually"),
                    z_last_updated_date = datetime.now(),
                    z_creation_date = datetime.now(),
                    z_is_migrated = l9_intangible_asset.get("z_is_migrated"),
                    z_is_migrated_and_updated = l9_intangible_asset.get("z_is_migrated_and_updated")
                )
                db.session.add(new)

        # f. Handle deletes (records in DB but not in payload)
        to_delete_l9_intangible_asset = [r for r in l9_intangible_asset_existing_records if r.z_record_id not in l9_intangible_asset_payload_ids]
        for record in to_delete_l9_intangible_asset:
            record.z_is_deleted = 1


        db.session.commit()

        return {"message": "Returnsheet saved successfully"}, 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
        
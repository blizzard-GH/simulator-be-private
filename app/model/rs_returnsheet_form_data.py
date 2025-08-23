import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT, TIMESTAMP
from sqlalchemy import text, DECIMAL, String
from app import db

class RSReturnsheetFormData(db.Model):
    __tablename__ = 'RS_RETURNSHEET_FORM_DATA'

    z_record_id = db.Column(String(55), primary_key=True)
    z_aggregate_identifier = db.Column(String(55))
    z_aggregate_version = db.Column(DECIMAL(19, 0))
    z_return_sheet_version_code = db.Column(String(50))
    z_form_data = db.Column(LONGTEXT)
    z_last_updated_date = db.Column(
        TIMESTAMP(fsp=6),
        nullable=False,
        server_default=text('current_timestamp(6) ON UPDATE current_timestamp(6)')
    )
    z_is_migrated = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_is_migrated_and_updated = db.Column(DECIMAL(1, 0), server_default=text('0'))
    z_creation_date = db.Column(
        TIMESTAMP(fsp=6),
        nullable=False,
        server_default=text('current_timestamp(6)')
    )

    def get_main_form_data(self):
        try:
            data = json.loads(self.z_form_data or '{}')
            return data.get('MainFormData', {})
        except json.JSONDecodeError:
            return {}
        
    @property
    def form_data(self):
        return json.loads(self.z_form_data) if self.z_form_data else {}

    @form_data.setter
    def form_data(self, value):
        self.z_form_data = json.dumps(value)

    def get_main_form_value(self, key, default=None):
        """Get a value from MainFormData safely"""
        return self.form_data.get("MainFormData", {}).get(key, default)

    def get_l1c_form_value(self, key, default=None):
        """Get a value from L1cFormData safely"""
        return self.form_data.get("L1cFormData", {}).get(key, default)
    
    def get_list_of_ownership_value(self, key, default=None):
        """Get a value from ListOfOwnership safely"""
        return self.form_data.get("ListOfOwnership", {}).get(key, default)
    
    def get_list_income_tax_withheld_by_other_parties_value(self, key, default=None):
        """Get a value from ListIncomeTaxWithheldByOtherParties safely"""
        return self.form_data.get("ListIncomeTaxWithheldByOtherParties", {}).get(key, default)
    
    def get_list_of_income_subject_to_final_tax_and_non_taxable_object_value(self, key, default=None):
        """Get a value from ListOfIncomeSubjectToFinalTaxAndNonTaxableObject safely"""
        return self.form_data.get("ListOfIncomeSubjectToFinalTaxAndNonTaxableObject", {}).get(key, default)
    
    def get_fiscal_year_income_tax_value(self, key, default=None):
        """Get a value from FiscalYearIncomeTax safely"""
        return self.form_data.get("FiscalYearIncomeTax", {}).get(key, default)
    
    def get_calculation_facilities_income_tax_rate_reduction_value(self, key, default=None):
        """Get a value from CalculationFacilitiesIncomeTaxRateReduction safely"""
        return self.form_data.get("CalculationFacilitiesIncomeTaxRateReduction", {}).get(key, default)
    
    def get_l11b_form_value(self, key, default=None):
        """Get a value from L11BFormData safely"""
        return self.form_data.get("L11BFormData", {}).get(key, default)
    
    def get_recapitulation_fiscal_depreciation_amortization_value(self, key, default=None):
        """Get a value from RecapitulationFiscalDepreciationAmortization safely"""
        return self.form_data.get("RecapitulationFiscalDepreciationAmortization", {}).get(key, default)
    
    def get_financial_statement_value(self, key, default=None):
        """Get a value from FinancialStatement safely"""
        return self.form_data.get("FinancialStatement", {}).get(key, default)
    
    def set_main_form_value(self, key, value):
        """Set a value inside MainFormData (create MainFormData if missing)"""
        data = self.form_data
        if "MainFormData" not in data:
            data["MainFormData"] = {}
        data["MainFormData"][key] = value
        self.form_data = data

    def set_l1c_form_value(self, key, value):
        """Set a value inside L1cFormData (create L1cFormData if missing)"""
        data = self.form_data
        if "L1cFormData" not in data:
            data["L1cFormData"] = {}
        data["L1cFormData"][key] = value
        self.form_data = data

    def set_list_of_ownership_value(self, key, value):
        """Set a value inside ListOfOwnership (create ListOfOwnership if missing)"""
        data = self.form_data
        if "ListOfOwnership" not in data:
            data["ListOfOwnership"] = {}
        data["ListOfOwnership"][key] = value
        self.form_data = data

    def set_list_income_tax_withheld_by_other_parties_value(self, key, value):
        """Set a value inside ListIncomeTaxWithheldByOtherParties (create ListIncomeTaxWithheldByOtherParties if missing)"""
        data = self.form_data
        if "ListIncomeTaxWithheldByOtherParties" not in data:
            data["ListIncomeTaxWithheldByOtherParties"] = {}
        data["ListIncomeTaxWithheldByOtherParties"][key] = value
        self.form_data = data

    def set_list_of_income_subject_to_final_tax_and_non_taxable_object_value(self, key, value):
        """Set a value inside ListOfIncomeSubjectToFinalTaxAndNonTaxableObject (create ListOfIncomeSubjectToFinalTaxAndNonTaxableObject if missing)"""
        data = self.form_data
        if "ListOfIncomeSubjectToFinalTaxAndNonTaxableObject" not in data:
            data["ListOfIncomeSubjectToFinalTaxAndNonTaxableObject"] = {}
        data["ListOfIncomeSubjectToFinalTaxAndNonTaxableObject"][key] = value
        self.form_data = data

    def set_fiscal_year_income_tax_value(self, key, value):
        """Set a value inside FiscalYearIncomeTax (create FiscalYearIncomeTax if missing)"""
        data = self.form_data
        if "FiscalYearIncomeTax" not in data:
            data["FiscalYearIncomeTax"] = {}
        data["FiscalYearIncomeTax"][key] = value
        self.form_data = data

    def set_calculation_facilities_income_tax_rate_reduction_value(self, key, value):
        """Set a value inside CalculationFacilitiesIncomeTaxRateReduction (create CalculationFacilitiesIncomeTaxRateReduction if missing)"""
        data = self.form_data
        if "CalculationFacilitiesIncomeTaxRateReduction" not in data:
            data["CalculationFacilitiesIncomeTaxRateReduction"] = {}
        data["CalculationFacilitiesIncomeTaxRateReduction"][key] = value
        self.form_data = data

    def set_l11b_form_value(self, key, value):
        """Set a value inside L11BFormData (create L11BFormData if missing)"""
        data = self.form_data
        if "L11BFormData" not in data:
            data["L11BFormData"] = {}
        data["L11BFormData"][key] = value
        self.form_data = data

    def set_recapitulation_fiscal_depreciation_amortization_value(self, key, value):
        """Set a value inside RecapitulationFiscalDepreciationAmortization (create RecapitulationFiscalDepreciationAmortization if missing)"""
        data = self.form_data
        if "RecapitulationFiscalDepreciationAmortization" not in data:
            data["RecapitulationFiscalDepreciationAmortization"] = {}
        data["RecapitulationFiscalDepreciationAmortization"][key] = value
        self.form_data = data

    def set_financial_statement_value(self, key, value):
        """Set a value inside FinancialStatement (create FinancialStatement if missing)"""
        data = self.form_data
        if "FinancialStatement" not in data:
            data["FinancialStatement"] = {}
        data["FinancialStatement"][key] = value
        self.form_data = data

    def set_financial_statement(self, value_list: list[dict]):
        """Set FinancialStatement as an array of objects"""
        data = self.form_data
        data["FinancialStatement"] = value_list
        self.form_data = data
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from uuid import UUID
from datetime import datetime


class CalculationFacilitiesIncomeTaxRateReduction(BaseModel):
    GrossTurnOver: Optional[int] = None
    TaxableIncomeShareOfGrossCirculationGrantedFacility: Optional[int] = None
    TaxableIncomeShareOfGrossCirculationNotGrantedFacility: Optional[int] = None
    IncomeTaxPayableFromTaxableIncomeShareOfGrossCirculationGrantedFacility: Optional[int] = None
    IncomeTaxPayableFromTaxableIncomeShareOfGrossCirculationNotGrantedFacility: Optional[int] = None
    TotalIncomeTax: Optional[int] = None


class FinancialStatement(BaseModel):
    DocumentAggregateIdentifier: Optional[UUID] = None
    DocumentId: Optional[str] = None
    FileName: Optional[str] = None
    DocumentType: Optional[str] = None


class FiscalYearIncomeTax(BaseModel):
    IncomeAsTheBasisOfInstallment: Optional[int] = None
    FiscalLossCompensation: Optional[int] = None
    TaxableIncome: Optional[int] = None
    IncomeTaxPayable: Optional[int] = None
    TaxCreditWitheld: Optional[int] = None
    IncomeTaxSelfpaid: Optional[int] = None
    FollowingFiscalYear: Optional[int] = None


class TotalBorrowingCosts(BaseModel):
    Name: Optional[str] = None
    AverageDebtBalances: Optional[int] = None
    BorrowingCostAmount: Optional[int] = None
    BorrowingCostThatCanBeDeducted: Optional[int] = None
    BorrowingCostThatAreNotDeductible: Optional[int] = None


class TotalDebtBalanceAverage(BaseModel):
    IsTinOrNik: Optional[bool] = None
    IdentityNumber: Optional[str] = None
    Name: Optional[str] = None
    Relationship: Optional[str] = None
    DebtMonth1: Optional[int] = None
    DebtMonth2: Optional[int] = None
    DebtMonth3: Optional[int] = None
    DebtMonth4: Optional[int] = None
    DebtMonth5: Optional[int] = None
    DebtMonth6: Optional[int] = None
    DebtMonth7: Optional[int] = None
    DebtMonth8: Optional[int] = None
    DebtMonth9: Optional[int] = None
    DebtMonth10: Optional[int] = None
    DebtMonth11: Optional[int] = None
    DebtMonth12: Optional[int] = None
    Average: Optional[int] = None


class L11BFormData(BaseModel):
    CommercialNettIncome: Optional[int] = None
    DepreciationAndAmortizationExpenses: Optional[int] = None
    IncomeTaxExpense: Optional[int] = None
    BorrowingCostExpense: Optional[int] = None
    Ebitda: Optional[int] = None
    Ebitda25: Optional[int] = None
    DebtBalanceAverage: Optional[int] = None
    TotalDebtBalanceAverage: Optional[TotalDebtBalanceAverage] = None # type: ignore
    EquityBalanceAverage: Optional[int] = None
    TotalEquityBalanceAverage: Optional[Dict[str, Optional[int]]] = None
    DebtToEquityRatio: Optional[int] = None
    BorrowingCosts: Optional[List[TotalBorrowingCosts]] = None
    TotalBorrowingCosts: Optional[TotalBorrowingCosts] = None # type: ignore
    IsDocumentListForm: Optional[bool] = None


class RowOptions(BaseModel):
    IsShowAdd: Optional[bool] = None
    IsShowDelete: Optional[bool] = None
    IsShowEdit: Optional[bool] = None


class L1CTree(BaseModel):
    AccountCode: Optional[str] = None
    Amount: Optional[int] = None
    CorrectionCode: Optional[str] = None
    Description: Optional[str] = None
    FinalAmount: Optional[int] = None
    NegativeFiscalCorrection: Optional[int] = None
    NonFinal: Optional[int] = None
    NonTaxableObject: Optional[int] = None
    PositiveFiscalCorrection: Optional[int] = None
    RowOptions: Optional[RowOptions] = None # type: ignore
    SubjectToFinalTax: Optional[int] = None


class L1CFormData(BaseModel):
    L1cTreeData: Optional[List[L1CTree]] = None
    L1cTreeTotalRow: Optional[L1CTree] = None
    L1cAssets: Optional[Dict[str, Optional[int]]] = None
    L1cLiabilitiesAndEquity: Optional[Dict[str, Optional[int]]] = None


class IncomeOversea(BaseModel):
    Name: Optional[str] = None
    CountryCode: Optional[str] = None
    DateOfTransaction: Optional[datetime] = None
    IncomeCode: Optional[int] = None
    NetIncome: Optional[int] = None
    PayableRupiah: Optional[int] = None
    PayableCurrency: Optional[str] = None
    AmountForeignCurrency: Optional[int] = None
    CreditCalculated: Optional[int] = None


class ListIncomeTaxWithheldByOtherParties(BaseModel):
    IncomeOverseas: Optional[List[IncomeOversea]] = None
    OverseasTotalNetIncome: Optional[int] = None
    OverseasTotalTaxPayable: Optional[int] = None
    OverseasTotalTaxCredit: Optional[int] = None
    OverseasRefundPreviousYear: Optional[int] = None
    OverseasTotalCalculatedCurrentYear: Optional[int] = None
    OtherPartiesTotalTaxBase: Optional[int] = None
    OtherPartiesIncomeTaxWithheld: Optional[int] = None
    OtherPartiesIncomeTaxWithheldUsd: Optional[float] = None
    OtherPartiesOverseasIncomeTax: Optional[int] = None
    OtherPartiesTotalCredit: Optional[int] = None
    OtherPartiesTotalCreditUsd: Optional[float] = None


class ListOfIncomeSubjectToFinalTaxAndNonTaxableObject(BaseModel):
    TotalTaxBase: Optional[int] = None
    TotalFinalIncomeTaxPayable: Optional[int] = None
    TotalFinalIncomeTaxPayableUsd: Optional[int] = None
    ListOfIncomeExcludedFromIncomeTax: None
    TotalGrossIncome: Optional[int] = None


class ListOfShareholder(BaseModel):
    Name: Optional[str] = None
    Address: Optional[str] = None
    CountryCode: Optional[str] = None
    TIN: Optional[str] = None
    Position: Optional[str] = None
    PaidInCapital: Optional[int] = None
    PaidInCapitalPercentage: Optional[int] = None
    Dividend: Optional[int] = None
    ValidTo: Optional[datetime] = None
    ValidFrom: Optional[datetime] = None


class ListOfOwnership(BaseModel):
    ListOfShareholders: Optional[List[ListOfShareholder]] = None
    TotalPaidInCapital: Optional[int] = None
    TotalPaidInCapitalPercentage: Optional[int] = None
    TotalDividend: Optional[int] = None
    InvestmentList: None
    TotalDebt: Optional[int] = None
    TotalReceivable: Optional[int] = None


class MainFormData(BaseModel):
    TaxYear: Optional[int] = None
    AccountingPeriodStart: Optional[int] = None
    AccountingPeriodEnd: Optional[int] = None
    Status: Optional[str] = None
    AccountingMethod: Optional[str] = None
    Tin: Optional[str] = None
    Name: Optional[str] = None
    EmailAddress: Optional[str] = None
    PhoneNumber: Optional[str] = None
    BusinessClassification: Optional[str] = None
    AuditedFinancialStatements: Optional[int] = None
    AuditorOpinion: Optional[str] = None
    TinAccountant: Optional[str] = None
    NameAccountant: Optional[str] = None
    IsIncomeUnder: Optional[int] = None
    IsIncomeSolely: Optional[int] = None
    IsIncomeSubject: Optional[int] = None
    TotalIncomeSubject: Optional[int] = None
    IsIncomeExcluded: Optional[int] = None
    TotalIncomeExcluded: Optional[int] = None
    NetIncomeBeforeTax: Optional[int] = None
    IsNetIncomeReduction: Optional[int] = None
    TotalNetIncomeReduction: Optional[int] = None
    IsGrossIncomeVocational: Optional[int] = None
    TotalGrossIncomeVocational: Optional[int] = None
    FiscalNetIncomeAfterTax: Optional[int] = None
    IsCarriedForward: Optional[int] = None
    TotalCarriedForward: Optional[int] = None
    TaxableIncome: Optional[int] = None
    IsGrossIncomeResearch: Optional[int] = None
    TotalGrossIncomeResearch: Optional[int] = None
    TaxRate: Optional[str] = None
    PercentageOfTaxRate: Optional[int] = None
    IncomeTaxInAYear: Optional[int] = None
    IsIncomeTaxOverseas: Optional[int] = None
    IsIncomeTaxOverseasWithholding: Optional[bool] = None
    TotalIncomeTaxOverseas: Optional[int] = None
    InstallmentOfIncome: Optional[int] = None
    NoticeOfCollection: Optional[int] = None
    IsIncomeTaxDeduction: Optional[int] = None
    TotalIncomeTaxDeduction: Optional[int] = None
    UnderpaymentIncomeTax: Optional[int] = None
    IsApprovalInstallment: Optional[int] = None
    TotalApprovalInstallment: Optional[int] = None
    IncomeTaxMustPaid: Optional[int] = None
    UnderpaymentIncomeInAmended: Optional[int] = None
    UnderpaymentIncomeDueAmended: Optional[int] = None
    OverpaymentIncomeTax: Optional[int] = None
    BankName: Optional[str] = None
    AccountNumber: Optional[str] = None
    AccountHolderName: Optional[str] = None
    BankAccount: Optional[str] = None
    BankCode: Optional[str] = None
    IsCriteriaObligatedSubmit: Optional[int] = None
    TotalCriteriaObligatedSubmit: Optional[int] = None
    IsUnderPSCGrossSplitScheme: Optional[int] = None
    IsTransactionWithRelated: Optional[int] = None
    IsObligationTransferPricing: Optional[int] = None
    IsCapitalInvestmentAffilated: Optional[int] = None
    IsDebtFromShareholders: Optional[int] = None
    IsDeclareFiscalDepreciation: Optional[int] = None
    IsDeclareEntertainmentExpense: Optional[int] = None
    IsInvestmentOtherIncome: Optional[int] = None
    IsRemainingExcess: Optional[int] = None
    IsReceiveDividendIncome: Optional[int] = None
    IsReceiveDividendIncomeNumber: Optional[int] = None
    FinancialStatementPdf: None
    FinancialStatementXls: None
    AuditOpinionPdf: None
    ConsolidatedFinancialPdf: None
    WithholdingSlipPdf: None
    ProofOfReinvestmentPdf: None
    CalculationCreditedIncomePdf: None
    FinancialForeignPdf: None
    IncomeTaxForeignPdf: None
    CalculationAfterTaxPdf: None
    ProofOfIncomePdf: None
    ProofOfZakatPdf: None
    MonthlyReportPdf: None
    ReportOfShareholderPdf: None
    ElectronicReceiptPdf: None
    OrderDocumentsPdf: None
    CheckboxDeclaration: None
    SignBy: Optional[int] = None
    DateOfSubmit: None
    SignerTin: Optional[str] = None
    SignerName: Optional[str] = None
    SignerPosition: Optional[str] = None
    AskForReplacement: Optional[str] = None
    ReplacementPrevious: Optional[bool] = None


class FormData(BaseModel):
    TaxType: Optional[str] = None
    IsDraft: Optional[bool] = None
    PeriodCode: Optional[str] = None
    CorporateType: Optional[str] = None
    ActualMonths: Optional[int] = None
    PrefillFromId: Optional[UUID] = None
    MainFormData: Optional[MainFormData] = None # type: ignore
    L1aFormData: Optional[str] = None
    L1bFormData: Optional[str] = None
    L1cFormData: Optional[L1CFormData] = None
    L1dFormData: Optional[str] = None
    L1eFormData: Optional[str] = None
    L1fFormData: Optional[str] = None
    L1gFormData: Optional[str] = None
    L1hFormData: Optional[str] = None
    L1iFormData: Optional[str] = None
    L1jFormData: Optional[str] = None
    L1kFormData: Optional[str] = None
    L1lFormData: Optional[str] = None
    ListOfOwnership: Optional[ListOfOwnership] = None # type: ignore
    ListIncomeTaxWithheldByOtherParties: Optional[ListIncomeTaxWithheldByOtherParties] = None # type: ignore
    ListOfIncomeSubjectToFinalTaxAndNonTaxableObject: Optional[ListOfIncomeSubjectToFinalTaxAndNonTaxableObject] = None # type: ignore
    ListOfGrossTurnover: Optional[str] = None
    FiscalYearIncomeTax: Optional[FiscalYearIncomeTax] = None # type: ignore
    CalculationOfFiscalLossCompensation: Optional[int] = None
    CalculationFacilitiesIncomeTaxRateReduction: Optional[CalculationFacilitiesIncomeTaxRateReduction] = None # type: ignore
    RecapitulationFiscalDepreciationAmortization: Optional[Dict[str, int]] = None
    L10bFormData: Optional[str] = None
    L10cFormData: Optional[str] = None
    L10dFormData: Optional[str] = None
    L11AFormData: Optional[str] = None
    L11BFormData: Optional[L11BFormData] = None # type: ignore
    L11CFormData: Optional[str] = None
    L12AFormData: Optional[str] = None
    L12BNotificationReinvestmentNetIncome: Optional[str] = None
    L13AListOfTaxFacilityInInvestment: Optional[str] = None
    L13BListOfAdditionalGrossIncomeDeduction: Optional[str] = None
    L13CListOfTaxFacilityOfCorporateIncomeTaxReduction: Optional[str] = None
    L14UtilizationOfRemainingExcess: Optional[str] = None
    FinancialStatement: Optional[List[FinancialStatement]] = None # type: ignore
    FinancialStatementXlsx: Optional[str] = None
    AuditOpinion: Optional[str] = None
    ConsolidatedFinancialStatement: Optional[str] = None
    WithholdingSlip: Optional[str] = None
    ProofOfReinvestment: Optional[str] = None
    CalculationLetterOfTheIncomeTax: Optional[int] = None
    FinancialStatementControlledForeignCompany: Optional[str] = None
    CopyOfIncomeTaxReturn: Optional[int] = None
    CalculationAfterTaxIncome5Years: Optional[int] = None
    ProofOfIncomeTax: Optional[str] = None
    ProofOfZakat: Optional[str] = None
    MonthlyReport: Optional[str] = None
    ReportOfShareholders: Optional[str] = None
    ElectronicReceiptOfCBCR: Optional[str] = None
    ElectronicReceiptSubmission: Optional[str] = None
    OtherDocuments: Optional[List[Any]] = None

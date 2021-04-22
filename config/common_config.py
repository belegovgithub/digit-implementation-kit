from .local import *
import pandas as pd

config.ROLE_CODE_MAP = {
  "CITIZEN": "Citizen",
  "EMPLOYEE": "Employee",
  "SUPERUSER": "Super User",
  "TL_CEMP": "TL Counter Employee",
  "TL_APPROVER": "TL Approver",
  "EGF_ADMINISTRATOR": "Finance Adminsitrator",
  "TL_FIELD_INSPECTOR": "TL Field Inspector",
  "TL_DOC_VERIFIER": "TL doc verifier",
  "UC_EMP": "Universal Collection Employee",
  "SYSTEM": "System user",
  "DGDE": "DGDE user",
  "CSR": "Customer Support Representative",
  "PGR-ADMIN": "PGR Administrator",
  "GRO": "Grievance Routing Officer",
  "RO": "Redressal Officer",
  "ANONYMOUS": "ANONYMOUS",
  "STADMIN": "State Administrator",
  "WS_CEMP": "WS Counter Employee",
  "WS_DOC_VERIFIER": "WS doc verifier",
  "WS_FIELD_INSPECTOR": "WS Field Inspector",
  "WS_APPROVER": "WS Approver",
  "WS_CLERK": "WS Clerk",
  "SW_CEMP": "SW Counter Employee",
  "SW_DOC_VERIFIER": "SW Document Verifier",
  "SW_FIELD_INSPECTOR": "SW Field Inspector",
  "SW_APPROVER": "SW Approver",
  "SW_CLERK": "SW Clerk",
  "PT_CEMP": "PT Counter Employee",
  "PT_DOC_VERIFIER": "PT Document Verifier",
  "PT_FIELD_INSPECTOR": "PT Field Inspector",
  "PT_APPROVER": "PT Approver",
  "LR_CEMP":"LR Counter Employee",
  "LR_APPROVER_CEO":"LR Approver CEO",
  "LR_APPROVER_DEO":"LR Approver DEO",
  "DEO_DELHI":"DEO Delhi",
  "DEO_KOLKATA":"DEO Kolkata",
  "DEO_SILIGURI":"DEO Siliguri",
  "DEO_AGRA":"DEO Agra",
  "DEO_ALLAHABAD":"DEO Allahbad",
  "DEO_BAREILLY":"DEO Bareilly",
  "DEO_DANAPUR":"DEO Danapur",
  "DEO_LUCKNOW":"DEO Lucknow",
  "DEO_MEERUT":"DEO Meerut",
  "DEO_MHOW":"DEO Mhow",
  "DEO_JABALPUR":"DEO Jabalpur",
  "DEO_AHMEDABAD":"DEO Ahmedabad",
  "DEO_BANGALORE":"DEO Bangalore",
  "DEO_BHOPAL":"DEO Bhopal",
  "DEO_CHENNAI":"DEO Chennai",
  "DEO_COCHIN":"DEO Cochin",
  "DEO_JODHPUR":"DEO Jodhpur",
  "DEO_MUMBAI":"DEO Mumbai",
  "DEO_PUNE":"DEO Pune",
  "DEO_SECUNDERABAD":"DEO Secundrabad",
  "DEO_AMBALA":"DEO Ambala",
  "DEO_JALANDHAR":"DEO Jalandhar",
  "DEO_JAMMU":"DEO Jammu",
  "DEO_PATHANKOT":"DEO Pathankot",
  "DEO_TESTING": "DEO Testing"
}


def load_config():
    config.INSERT_DATA =True
    config.isUpdateallowed = False
    config.ASSUME_YES = False
    config.GOOGLE_AUTH_CONFIG = config.BASE_PATH + '/SpreadSheetDBService-2be6caceda84.json'
    config.URL_LOGIN = config.HOST + "/user/oauth/token"
    config.URL_BILLING_SLAB_CREATE = config.HOST + "/pt-calculator-v2/billingslab/_create"

    config.URL_SEARCH_LOCALITIES_USED_IN_REVENUE = config.HOST + "/egov-searcher/rainmaker-pt-customsearch-punjab/searchLocalitiesUsedInRevenue/_get"
    config.URL_SEARCH_LOCALITIES_USED_IN_ADMIN = config.HOST + "/egov-searcher/rainmaker-pt-customsearch-punjab/searchLocalitiesUsedInAdmin/_get"

    config.BOUNDARY_DUPLICATE_CHECK = True
    config.BOUNDARY_USED_CHECK = True

    config.MDMS_DEPARTMENT_JSON = config.MDMS_LOCATION / "common-masters" / "Department.json"
    config.MDMS_DESIGNATION_JSON = config.MDMS_LOCATION / "common-masters" / "Designation.json"

    config.MDMS_ACTIONS_JSON = config.MDMS_LOCATION / "ACCESSCONTROL-ACTIONS-TEST" / "actions-test.json"
    config.MDMS_ROLEACTIONS_JSON = config.MDMS_LOCATION / "ACCESSCONTROL-ROLEACTIONS" / "roleactions.json"

    config.CITY_MODULES_JSON = config.MDMS_LOCATION / "tenant" / "citymodule.json"
    config.TENANT_JSON = config.MDMS_LOCATION / "tenant" / "tenants.json"
    config.TENANTINFO_JSON = config.MDMS_LOCATION / "tenant" / "tenantInfo.json"
    config.FOOTER_JSON = config.MDMS_LOCATION / "tenant" / "footer.json"
    config.CITY_MODULE_JSON = config.MDMS_LOCATION / "tenant" / "citymodule.json"
    config.HELP_JSON = config.MDMS_LOCATION / "common-masters" / "Help.json"
    config.BUSINESS_SERVICE_JSON = config.MDMS_LOCATION / "BillingService" / "BusinessService.json"
    config.DOCUMENT_TYPE_MASTER_JSON = config.MDMS_LOCATION / "common-masters" / "DocumentType.json"
    config.TAXHEADMASTER_JSON = config.MDMS_LOCATION / "BillingService" / "TaxHeadMaster.json"


    config.TENANT_ID = config.TENANT + "." + config.CITY_NAME.lower()

    config.SHEET_NAME = config.CITY_NAME.lower() + ".xlsx"
    config.SHEET = config.BOUNDARIES_FOLDER / config.SHEET_NAME
    config.TENANT_WORKBOOK=config.BOUNDARIES_FOLDER / "02-Common/Tenant Information Template.xlsx"
    config.BDY_WORKBOOK =config.BOUNDARIES_FOLDER / "02-Common/Boundary Or Jurisdiction_Template.xlsx"
    config.MCOLLECT_WORKBOOK =config.BOUNDARIES_FOLDER / "03-mCollect/mCollect.xlsx"
    config.DOCUMENT_TYPE_WORKBOOK = config.TL_FOLDER / "04-Trade License/TradeDocument.xlsx"
    config.TRADE_TYPE_WORKBOOK = config.TL_FOLDER / "04-Trade License/TradeCategoryFee.xlsx"
    config.TRADE_RATE_WORKBOOK = config.TL_FOLDER / "04-Trade License/Trade License Rate Template.xlsx"
    config.TRADE_DOC_TYPE_WORKBOOK = config.TL_FOLDER / "04-Trade License/Trade License DocumentsTemplate.xlsx"
    config.BANK_WORKBOOK=config.BOUNDARIES_FOLDER / "02-Common/Bank_Details_Template.xlsx"
    config.HRMS_WORKBOOK =config.BOUNDARIES_FOLDER / "02-Common/User_Role Mapping.xlsx"

    if not os.path.isfile(config.SHEET):
        config.SHEET_NAME = config.CITY_NAME.lower() + ".xls"
        config.SHEET = config.BOUNDARIES_FOLDER / config.SHEET_NAME

    config.SHEET_DEPARTMENTS = "Employee-Position"

    config.SHEET_DESIGNATION = config.SHEET_DEPARTMENTS
    config.SHEET_EMPLOYEE = config.SHEET_DEPARTMENTS
    config.SHEET_TENANT_DETAILS = "Tenant Detail"
    config.SHEET_MCOLLECT = "mCollect"
    config.SHEET_DOCLIST = "TL- Documents"
    config.SHEET_TRADETYPE_LIST = "TL- LicenseFee"
    config.SHEET_BANK_BRANCH = "Bank Branch"
    config.SHEET_BANK_ACCOUNT = "Bank Account"
    config.SHEET_ACCOUNT_CODE_PURPOSE = "Account Code Purpose"
    config.SHEET_CHART_ACCOUNT = "Chart of Account"
    config.SHEET_FUND = "Fund"
    config.SHEET_APPLFEE = "TL - ApplnFee"
    config.SHEET_TRADERATE = "TradeRates"
    config.SHEET_TRADEDOC="TradeDocuments"

    config.COLUMN_DESIGNATION = "Designation"
    config.COLUMN_DEPARTMENT = "Department"

    config.TRADETYPE_EATING = "EATING"
    config.TRADETYPE_MEDICAL=  "MEDICAL"
    config.TRADETYPE_VETERINARY = "VETERINARY"
    config.TRADETYPE_DANGEROUS = "DANGEROUS"
    config.TRADETYPE_GENERAL = "GENERAL"
    config.TRADETYPE_PRIVATE = "PRIVATE"
    config.TRADETYPE_MSME = "MSME"
    config.TRADETYPE_OTHERS = "OTHERS"
    config.PERSQFEET = "PER SQ FEET"
    config.UNIT = "PER UNIT"
    


def load_admin_boundary_config():
    config.SHEET_ZONES = "Admin Zone"
    config.SHEET_WARDS = "Admin Block"
    config.SHEET_LOCALITY = "Locality"

    config.COLUMN_WARD_CODE = "Block/Ward Code"
    config.COLUMN_WARD_NAME = "Block/Ward Name"
    config.COLUMN_WARD_ADMIN_ZONE_NAME = "Admin Zone Name"

    config.COLUMN_ZONE_CODE = "Zone Code"
    config.COLUMN_ZONE_NAME = "Zone Name"

    config.COLUMN_LOCALITY_CODE = "Locality Code"
    config.COLUMN_LOCALITY_NAME = "Locality Name"
    config.COLUMN_LOCALITY_ADMIN_BLOCK = "Admin Block/Ward Name"
    config.COLUMN_LOCALITY_AREA = "Area Name"


def load_revenue_boundary_config():
    config.SHEET_ZONES = "Zone"
    config.SHEET_WARDS = "Wards"
    config.SHEET_LOCALITY = "Mohalla"

    config.COLUMN_WARD_CODE = "Revenue_Ward_Code*"
    config.COLUMN_WARD_NAME = "Ward_name_English*"
    config.COLUMN_WARD_ADMIN_ZONE_NAME = "Zone Code"

    config.COLUMN_ZONE_CODE = "Zone Code*"
    config.COLUMN_ZONE_NAME = "Zone Name*"
    config.COLUMN_ZONE_NAME_HINDI = "Zone Name Hindi*"

    config.COLUMN_LOCALITY_CODE = "Locality Code*"
    config.COLUMN_LOCALITY_NAME = "Locality Name(English)*"
    config.COLUMN_LOCALITY_NAME_HINDI = "Locality Name(Hindi)*"
    config.COLUMN_LOCALITY_ADMIN_BLOCK = "Revenue Ward (Code)*"
    config.COLUMN_LOCALITY_AREA = "Zone Code"


def load_new_revenue_boundary_config():
    config.SHEET_LOCALITY = "RevenueBoundary"

    config.COLUMN_ZONE_CODE = "Rev Zone Code"
    config.COLUMN_ZONE_NAME = "Rev Zone Name"

    config.COLUMN_WARD_CODE = "Rev Block/Ward Code"
    config.COLUMN_WARD_NAME = "Rev Block/Ward Name"

    config.COLUMN_LOCALITY_CODE = "Locality Code"
    config.COLUMN_LOCALITY_NAME = "Locality Name"
    config.COLUMN_LOCALITY_AREA = "Area Name"


def load_new_admin_boundary_config():
    config.SHEET_LOCALITY = "RevenueBoundary"

    config.COLUMN_ZONE_CODE = "Zone Code"
    config.COLUMN_ZONE_NAME = "Zone Name"

    config.COLUMN_WARD_CODE = "Block/Ward Code"
    config.COLUMN_WARD_NAME = "Block/Ward Name"

    config.COLUMN_LOCALITY_CODE = "Locality Code"
    config.COLUMN_LOCALITY_NAME = "Locality Name"
    config.COLUMN_LOCALITY_AREA = "Area Name"

def load_tl_billing_slab_download_config():
    config.SHEET_TRADES ="Trades"
    config.SHEET_ACCESSORIES="Accessories item"

    config.TRADE_COLUMN_LICENSE_TYPE="License type"
    config.TRADE_COLUMN_STRUCTURE_TYPE="Structure Type"
    config.TRADE_COLUMN_STRUCTURE_SUB_TYPE="Structure sub type"
    config.TRADE_COLUMN_TRADE_CATEGORY="Trade Category"
    config.TRADE_COLUMN_TRADE_TYPE="Trade Type"
    config.TRADE_COLUMN_TRADE_SUB_TYPE="Trade Sub-Type"
    config.TRADE_COLUMN_CHARGE="Charge"
    config.TRADE_COLUMN_UOM_UNIT="UOM Unit"
    config.TRADE_COLUMN_UOM_FROM="UOM From"
    config.TRADE_COLUMN_UOM_TO = "UOM To"

def load_mCollect_config():
    config.COLUMN_SERVICE_CAT = "*Service Category"
    config.COLUMN_SERVICE_SUBCAT = "*Service Subcategory  (English)"
    config.COLUMN_GL_CODE = "*GLCODE"
    config.COLUMN_CB_NAME = "CB CODE"
    config.COLUMN_DEPT_CODE = "DEPT CODE"
    config.COLUMN_FUND_NAME = "FUND CODE"

def load_employee_creation_config() :
    config.HRMS_EXCEL_NAME= "User_Role Mapping.xlsx"
    config.HRMS_SHEET_NAME="User Role Mapping"
    config.HRMS_STADMIN_PHONE_NUMBER ="8197292570"
    config.HRMS_STADMIN_DOB ="03-04-1986" # DATE FORMAT should remain same
    config.HRMS_STADMIN_JOINING ="01-01-2001" # DATE FORMAT should remain same
    config.HRMS_DEF_DEPT ="Information Technology"
    config.HRMS_DEF_DESIG ="Programmer"  
    config.HRMS_CREATE_STADMIN=True
    config.HRMS_CREATE_DEV_USER=True
    config.HRMS_DEV_PHONE_NUMBER ="9900717640"
    config.HRMS_DEV_ROLES=  "mCollect Employee"#"TL Counter Employee|TL Doc Verifier|TL Field Inspector|TL Approver|mCollect Employee" # SEPERATED BY PIPE


def getValue(value,dataType,defValue="") :
    try:
        if(value == None or value == 'None' or pd.isna(value)): 
            return defValue    
        else : 
            if dataType ==str : 
                return dataType(value).strip()
            elif dataType == float:
                return round(value, 2)
            else : 
                return dataType(value)
    except: 
        return defValue


load_config()

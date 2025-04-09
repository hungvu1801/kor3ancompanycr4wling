import logging

from dataclasses import dataclass, field, InitVar
from datetime import date
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@dataclass
class Company:
    company_name_kor: str
    company_name_eng: str = None
    company_code: str = None
    representative: str = None
    market_listing: str = None
    corp_registration_no: str = None
    tax_id: str = None
    address: str = None
    website: str = None
    ir_website: str = None
    tel: str = None
    fax: str = None
    industry: str = None
    est_date_string: InitVar[str] = ''
    est_date: date = field(init=False)
    end_month_fy_string: InitVar[str] = ''
    end_month_fy: int = field(init=False)
    url_: str = None
    
    def __post_init__(self, est_date_string:str, end_month_fy_string:str):
        self.est_date = self.convert_est_date(est_date_string)
        self.end_month_fy = self.convert_end_month_fy(end_month_fy_string)

    def convert_est_date(self, est_date_string):
        if not est_date_string:
            return None
        try:
            return datetime.strptime(est_date_string, "%Y-%m-%d").date()
        except Exception as e:
            logger.info(f"Error >>>>> {e} <<<<<")
            return None
    
    def convert_end_month_fy(self, end_month_fy_string:str):
        if not end_month_fy_string:
            return None
        try:
            return int(end_month_fy_string)
        except Exception as e:
            logger.info(f"Error >>>>> {e} <<<<<")
            return None
        
@dataclass
class CompanyCodeStaging:
    corp_code: str
    company_name_kor: str = None
    company_name_eng: str = None
    stock_code: str = None
    modify_date: date = field(init=False)
    modify_date_string: InitVar[str] = ''
    
    def convert_est_date(self, modify_date_string):
        if not modify_date_string:
            return None
        try:
            return datetime.strptime(modify_date_string, "%Y-%m-%d").date()
        except Exception as e:
            logger.info(f"Error >>>>> {e} <<<<<")
            return None
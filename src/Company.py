from dataclasses import dataclass, field, InitVar

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
    est_date: str = None
    end_month_fy: str = None
    url_: str = None
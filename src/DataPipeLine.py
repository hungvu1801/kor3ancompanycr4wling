import os, csv, time, logging

from dataclasses import fields, asdict
from sqlalchemy import text

from src.Company import Company


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DataPipeLineCSV:
    def __init__(self, csv_filename, storage_queue_limit=20):
        self.csv_filename = csv_filename
        self.storage_queue_limit = storage_queue_limit
        self.storage_queue = list()
        self.csv_file_open = False

    def save_to_csv(self) -> None:
        self.csv_file_open = True
        company_to_save = self.storage_queue.copy()
        self.storage_queue.clear()

        if not company_to_save:
            self.csv_file_open = False
            return
        keys = [field.name for field in fields(company_to_save[0])]
        file_exist = os.path.isfile(self.csv_filename) \
        and os.path.getsize(self.csv_filename) > 0
        with open(self.csv_filename, mode="a", newline="", encoding="utf-8") as wf:
            writer = csv.DictWriter(wf, fieldnames=keys)
            if not file_exist:
                writer.writeheader()

            for company in company_to_save:
                writer.writerow(asdict(company))
        self.csv_file_open = False

    def add_company(self, scrape_data) -> None:
        company = Company(
            company_name_kor = scrape_data.get("company_name_kor"),
            company_name_eng = scrape_data.get("company_name_eng"),
            company_code = scrape_data.get("company_code"),
            representative = scrape_data.get("representative"),
            market_listing = scrape_data.get("market_listing"),
            corp_registration_no = scrape_data.get("corp_registration_no"),
            tax_id = scrape_data.get("tax_id"),
            address = scrape_data.get("address"),
            website = scrape_data.get("website"),
            ir_website = scrape_data.get("ir_website"),
            tel = scrape_data.get("tel"),
            fax = scrape_data.get("fax"),
            industry = scrape_data.get("industry"),
            est_date = scrape_data.get("est_date"),
            end_month_fy = scrape_data.get("end_month_fy"),
            url_ = scrape_data.get("url_"),
        )
        self.storage_queue.append(company)
        if len(self.storage_queue) >= self.storage_queue_limit:
            self.save_to_csv()

    def close_pipeline(self) -> None:
        if self.csv_file_open:
            time.sleep(4)
        if len(self.storage_queue) > 0:
            self.save_to_csv()
        
class DataPipeLineToDB:
    def __init__(self, engine, lock, storage_queue_limit=20):
        self.storage_queue_limit = storage_queue_limit
        self.storage_queue = list()
        self.engine = engine
        self.lock = lock

    def clean_company(self, scrape_data) -> Company:
        return Company(
            company_name_kor = scrape_data.get("company_name_kor"),
            company_name_eng = scrape_data.get("company_name_eng"),
            company_code = scrape_data.get("company_code"),
            representative = scrape_data.get("representative"),
            market_listing = scrape_data.get("market_listing"),
            corp_registration_no = scrape_data.get("corp_registration_no"),
            tax_id = scrape_data.get("tax_id"),
            address = scrape_data.get("address"),
            website = scrape_data.get("website"),
            ir_website = scrape_data.get("ir_website"),
            tel = scrape_data.get("tel"),
            fax = scrape_data.get("fax"),
            industry = scrape_data.get("industry"),
            est_date_string = scrape_data.get("est_date"),
            end_month_fy_string = scrape_data.get("end_month_fy"),
            url_ = scrape_data.get("url_"),
        )

    def add_company(self, scrape_data) -> None:
        company = self.clean_company(scrape_data)

        with self.lock:
            self.storage_queue.append(company)
            if len(self.storage_queue) >= self.storage_queue_limit:
                self.upsert_to_db()
    
    def upsert_to_db(self) -> None:
        keys = [field.name for field in fields(self.storage_queue[0])]
        data_to_upsert = [asdict(company) for company in self.storage_queue]
        self.storage_queue.clear()
        insert_columns = [f":{col}" for col in keys]
        update_columns = [f"{col} = VALUES({col})" for col in keys]

        query_upsert = text(
            f"INSERT INTO tbl_company_master ({', '.join(keys)})"
            f"VALUES ({', '.join(insert_columns)})"
            "ON DUPLICATE KEY UPDATE "
            f"{', '.join(update_columns)};"
        )

        with self.engine.begin() as conn:
            conn.execute(query_upsert, data_to_upsert)
        
    def close_pipeline(self) -> None:
        with self.lock:
            if len(self.storage_queue) > 0:
                self.upsert_to_db()
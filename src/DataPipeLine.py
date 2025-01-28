from src.Company import Company
from dataclasses import fields, asdict
import os, csv, time
class DataPipeLine():
    def __init__(self, csv_filename, storage_queue=20):
        self.csv_filename = csv_filename
        self.storage_queue = storage_queue
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

    def close_pipeline(self) -> None:
        if self.csv_file_open:
            time.sleep(4)
        if len(self.storage_queue) > 0:
            self.save_to_csv()
import re, time, logging, sys
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from config import material_list
from src.DataPipeLine import DataPipeLineCSV, DataPipeLineToDB
from src.models.schemas import create_table_company_deepsearch, create_table_company_master
from src.utility.open_driver import open_driver
from src.utility.db_engine_init import create_engine_mysql, create_session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CompanyDARTCrawling:
    def __init__(self, company_datapipeline, idx_alphabet_min=0, idx_alphabet_max=26, currpage=1, driver_headless=False) -> None:
        self.idx_alphabet_min = idx_alphabet_min
        self.idx_alphabet_max = idx_alphabet_max
        self.currpage = currpage
        self.url = "https://englishdart.fss.or.kr/dsbc001/main.do"
        self.company_datapipeline = company_datapipeline
        self.driver_headless = driver_headless
        self.driver = open_driver(headless=driver_headless)
        self.pattern_page = r"/(\d+)"

    def crawling_card(self) -> None:
        try:
            self.driver.get(url)
            time.sleep(3)

            while True:
                try:
                    if self.idx_alphabet_min > self.idx_alphabet_max:
                        break

                    func_call = f"searchIdx('{self.idx_alphabet_min}'); return false;" # Call to alphabet
                    self.driver.execute_script(func_call)
                    time.sleep(1)
                    logger.info(f"Current alphabet element index: {self.idx_alphabet_min}")
                    func_call_pagination = f"search1({self.currpage}); return false;" # Call to next page
                    logger.info(f"Current page: {self.currpage}")
                    self.driver.execute_script(func_call_pagination)
                    time.sleep(3)
                    # page = 0 # This will mark the current page
                    page_max_elem = self.driver.find_element(By.CSS_SELECTOR, "div.pageInfo").text
                    page_max_match = re.search(pattern=self.pattern_page, string=page_max_elem)
                    if page_max_match:
                        page_max = int(page_max_match.group(1))
                    logger.info(f"Page max of letter {self.idx_alphabet_min} : {page_max}")
                    while True:
                        time.sleep(2)
                        company_elems = self.driver.find_elements(By.XPATH, "//table[@id='corpTable']/tbody/tr")

                        for company_name in company_elems:

                            click_elem = company_name.find_element(By.XPATH, ".//a")
                            click_elem.click()
                            time.sleep(1)
                            company_detail_elems = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_all_elements_located(
                                    (By.XPATH,  "//table[@id='corpDetailTable']/tbody/tr")))

                            scraped_data = dict()

                            for key, value_elem in zip(material_list, company_detail_elems):
                                
                                value = value_elem.find_element(By.XPATH, ".//td").text
                                scraped_data[key] = value

                            url = company_name.find_element(By.XPATH, ".//a").get_attribute("href")
                            scraped_data["url_"] = url
                            self.company_datapipeline.add_company(scraped_data)
                        # pagination controls
                        if self.currpage >= page_max:
                            self.currpage = 1
                            break
                        self.currpage += 1
                        logger.info(f"Current page: {self.currpage}")
                        func_call_pagination = f"search1({self.currpage}); return false;" # Call to next page
                        self.driver.execute_script(func_call_pagination)
                        time.sleep(3)
                    self.idx_alphabet_min += 1
                except StaleElementReferenceException as e:
                    logger.info(f"Error : {e}")
                    self.driver.refresh()
        except Exception as e:
            logger.info(f"Error : {e}")
        finally:
            self.company_datapipeline.close_pipeline()

def card(datapipeline, idx_alphabet_min=0, idx_alphabet_max=26, currpage=1) -> None:
    # idx_alphabet_elems = 12
    url = "https://englishdart.fss.or.kr/dsbc001/main.do"
    driver = open_driver()
    driver.get(url)
    time.sleep(3)

    pattern_page = r"/(\d+)"

    while True:
        try:
            if idx_alphabet_min > idx_alphabet_max:
                break

            func_call = f"searchIdx('{idx_alphabet_min}'); return false;"
            driver.execute_script(func_call)
            time.sleep(1)
            logger.info(f"Current alphabet element index: {idx_alphabet_min}")
            func_call_pagination = f"search1({currpage}); return false;" # Call to next page
            logger.info(f"Current page: {currpage}")
            driver.execute_script(func_call_pagination)
            time.sleep(3)
            # page = 0 # This will mark the current page
            page_max_elem = driver.find_element(By.CSS_SELECTOR, "div.pageInfo").text
            page_max_match = re.search(pattern=pattern_page, string=page_max_elem)
            if page_max_match:
                page_max = int(page_max_match.group(1))
            logger.info(f"Page max of letter {idx_alphabet_min} : {page_max}")
            while True:
                time.sleep(2)
                company_elems = driver.find_elements(By.XPATH, "//table[@id='corpTable']/tbody/tr")

                for company_name in company_elems:
                    logger.info("Find company... ")
                    click_elem = company_name.find_element(By.XPATH, ".//a")
                    click_elem.click()
                    time.sleep(1)
                    company_detail_elems = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH,  "//table[@id='corpDetailTable']/tbody/tr")))

                    scraped_data = dict()

                    for key, value_elem in zip(material_list, company_detail_elems):
                        
                        value = value_elem.find_element(By.XPATH, ".//td").text
                        scraped_data[key] = value

                    url = company_name.find_element(By.XPATH, ".//a").get_attribute("href")
                    scraped_data["url_"] = url
                    datapipeline.add_company(scraped_data)
                # pagination controls
                if currpage >= page_max:
                    currpage = 1
                    break
                currpage += 1
                logger.info(f"Current page: {currpage}")
                func_call_pagination = f"search1({currpage}); return false;" # Call to next page
                driver.execute_script(func_call_pagination)
                time.sleep(3)
            idx_alphabet_min += 1
        except Exception as e:
            logger.info(f"Error : {e}")
            driver.refresh()
            time.sleep(15)

            
def detail() -> None:
    ...


def main_multi() -> None:
    try:
        ####################################################
        # This is get arguments from user
        save_type = "db"
        if len(sys.argv) == 2:
            save_type = sys.argv[1].lower()
            print(save_type)
        ####################################################

        engine = create_engine_mysql()
        _, metadata = create_session(engine)
        create_table_company_master(engine, metadata)
        create_table_company_deepsearch(engine, metadata)
        
        ####################################################
        lock = Lock()
        if save_type == "csv":
            company_datapipeline = DataPipeLineCSV(
                csv_filename=f"Download/company.csv", 
                storage_queue_limit=5)
        elif save_type == "db":
            company_datapipeline = DataPipeLineToDB(
                storage_queue_limit=10,
                engine=engine,
                lock=lock)
        else:
            return
        # card(company_datapipeline, 0, 15)
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(card, company_datapipeline, 0, 15)
            executor.submit(card, company_datapipeline, 16, 26)
        company_datapipeline.close_pipeline()
    except Exception as e:
        logger.info(f"CRITICAL > CHECK THIS {e}")
    finally:
        engine.dispose()
   
def main_single() -> None:
    try:
        ####################################################
        # This is get arguments from user
        idx_alphabet_elems = 0
        currpage = 1
        save_type = "db"
        if len(sys.argv) >= 2:
            idx_alphabet_elems = int(sys.argv[1])
            print(idx_alphabet_elems)
        if len(sys.argv) > 2:
            currpage = int(sys.argv[2])
            print(currpage)
        if len(sys.argv) == 4:
            save_type = sys.argv[3].lower()
            print(save_type)
        ####################################################
        lock = Lock()
        engine = create_engine_mysql()
        if save_type == "csv":
            company_datapipeline = DataPipeLineCSV(
                csv_filename=f"Download/company.csv", 
                storage_queue_limit=5)
        elif save_type == "db":
            company_datapipeline = DataPipeLineToDB(
                storage_queue_limit=10,
                engine=engine,
                lock=lock)
        else:
            return

        card(company_datapipeline, 0, 15)
        
    except Exception as e:
        logger.info(f"CRITICAL > CHECK THIS {e}")
    finally:
        engine.dispose()
        company_datapipeline.close_pipeline()
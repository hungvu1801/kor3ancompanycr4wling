from src.open_driver import open_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re, time
import logging, sys
from src.DataPipeLine import DataPipeLine
from config import material_list

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def card(idx_alphabet_elems=0, currpage=1) -> None:
    # idx_alphabet_elems = 12
    try:
        url = "https://englishdart.fss.or.kr/dsbc001/main.do"

        company_datapipeline = DataPipeLine(
            csv_filename=f"Download/company.csv", 
            storage_queue_limit=5)
        
        driver = open_driver()
        driver.get(url)
        time.sleep(3)

        pattern_page = r"/(\d+)"

        while True:
            if idx_alphabet_elems > 26:
                break

            func_call = f"searchIdx('{idx_alphabet_elems}'); return false;"
            driver.execute_script(func_call)
            time.sleep(1)
            logger.info(f"Current alphabet element index: {idx_alphabet_elems}")
            func_call_pagination = f"search1({currpage}); return false;" # Call to next page
            logger.info(f"Current page: {currpage}")
            driver.execute_script(func_call_pagination)
            time.sleep(3)
            # page = 0 # This will mark the current page
            page_max_elem = driver.find_element(By.CSS_SELECTOR, "div.pageInfo").text
            page_max_match = re.search(pattern=pattern_page, string=page_max_elem)
            if page_max_match:
                page_max = int(page_max_match.group(1))
            logger.info(f"Page max of letter {idx_alphabet_elems} : {page_max}")
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
                    company_datapipeline.add_company(scraped_data)
                # pagination controls
                if currpage >= page_max:
                    currpage = 1
                    break
                currpage += 1
                logger.info(f"Current page: {currpage}")
                func_call_pagination = f"search1({currpage}); return false;" # Call to next page
                driver.execute_script(func_call_pagination)
                time.sleep(3)
            idx_alphabet_elems += 1
    except Exception as e:
        logger.info(f"Error : {e}")
    finally:
        company_datapipeline.close_pipeline()
            
def detail() -> None:
    ...



def main() -> None:
    idx_alphabet_elems = 0
    currpage = 1
    if len(sys.argv) >= 2:
        idx_alphabet_elems = int(sys.argv[1])
        print(idx_alphabet_elems)
    if len(sys.argv) > 2:
        currpage = int(sys.argv[2])
        print(currpage)
    card(idx_alphabet_elems, currpage)
    # detail()
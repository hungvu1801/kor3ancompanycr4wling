from src.open_driver import open_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logging, sys


def card(currpage=0) -> None:
    
    url = "https://englishdart.fss.or.kr/dsbc001/main.do"
    driver = open_driver()
    driver.get(url)
    time.sleep(3)
    alphabet_elems = driver.find_elements(By.XPATH, "//div[@class='initialSearch']/ul/li")
    if not currpage:
        _ = input("Waiting ... ")
    for idx, letter in enumerate(alphabet_elems):
        func_call = f"searchIdx('{idx}'); return false;"
        driver.execute_script(func_call)
        _ = input()



def detail() -> None:
    ...



def main() -> None:
    currpage = 0
    if len(sys.argv) >= 2:
        currpage = int(sys.argv[1])
    card(currpage)
    # detail()
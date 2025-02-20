import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.assets import USER_AGENTS
import random
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def open_driver(headless=False):
    """
    Docstring:
    
    """
    options = Options()
    user_agent = random.choice(USER_AGENTS[0])

    try:
        service = Service(ChromeDriverManager().install())
        #### if using capture program, use these options ####
        if headless:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=service, options=options)
        #####################################################
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
        driver.maximize_window()
        logger.info("Create a Driver successfully.")
    except:
        logger.info("Error : Fail to create a Driver.")
        return None
    return driver
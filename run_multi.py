import logging
from datetime import datetime
from src.main import main_multi

today = datetime.today().strftime('%y%m%d')

logging.basicConfig(
    filename=f"log/{today}_filelog.log",
	level=logging.INFO, 
	format="%(asctime)s: %(levelname)s : %(message)s ")

if __name__ == "__main__":
    main_multi()
from src.main import main
import logging
from datetime import datetime

today = datetime.today().strftime('%y%m%d')

logging.basicConfig(
    filename=f"log/{today}_filelog.log",
	level=logging.INFO, 
	format="%(asctime)s: %(levelname)s : %(message)s ")

if __name__ == "__main__":
    main()
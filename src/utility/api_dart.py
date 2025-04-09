import os
import requests
from dotenv import load_dotenv

from src.assets import DART_CORP_CODE_URL

load_dotenv()

def download_company_code(saved_file):
    
    params = {
        "crtfc_key": os.getenv("DART_API_KEY")
        }
    
    response = requests(url=DART_CORP_CODE_URL, params=params, stream=True)

    with open(saved_file, "wb") as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)
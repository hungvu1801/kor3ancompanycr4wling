import zipfile


def extract_zip_file(file_path:str, extracted_path:str) -> None:
    with zipfile.ZipFile(file_path, zipfile.ZIP_DEFLATED) as zip_ref:
        zip_ref.extractall(extracted_path)
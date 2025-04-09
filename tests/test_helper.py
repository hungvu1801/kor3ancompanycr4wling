import unittest
import os
import zipfile
import tempfile

from src.utility.helper import extract_zip_file

class TestExtractZipFile(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.zip_file_path = os.path.join(self.test_dir.name, "test.zip")
        self.extracted_dir = os.path.join(self.test_dir.name, "extracted")
        with zipfile.ZipFile(self.zip_file_path, "w") as zip_ref:
            zip_ref.writestr("test_file.txt", "This is a test file.")
    
    def tearDown(self):
        self.test_dir.cleanup()

    def test_extract_zip_file(self):
        extract_zip_file(self.zip_file_path, self.extracted_dir)
        extracted_file = os.path.join(self.extracted_dir, "test_file.txt")
        self.assertTrue(os.path.exists(extracted_file))
        # Verify the contents of the extracted file
        with open(extracted_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, "This is a test file.")


if __name__ == "__main__":
    unittest.main()
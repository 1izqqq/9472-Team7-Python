import unittest
from unittest.mock import patch
from src.main import Main, FileReader
from util import printing_methods

class TestMain(unittest.TestCase):

    @patch.object(FileReader, 'load_json', return_value=[{"id": 1, "name": "Liza's Cambridge", "price_per_head": 100, "location": "Bareng Drive", "contact": "09762969444"}])
    @patch.object(FileReader, 'save_json')
    def test_run_success(self, mock_save_json, mock_load_json):

        main_app = Main('dummy_file.json')

        self.assertEqual(main_app.transients, [{"id": 1, "name": "Liza's Cambridge", "price_per_head": 100, "location": "Bareng Drive", "contact": "09762969444"}])

if __name__ == '__main__':
    unittest.main()

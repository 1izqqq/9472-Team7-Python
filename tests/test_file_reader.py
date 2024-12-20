import unittest
from unittest.mock import patch, mock_open
import json
import os
from main import FileReader


class TestFileReader(unittest.TestCase):

    def test_load_json_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = FileReader.load_json('non_existent_file.json')
            self.assertEqual(result, [])

    def test_load_json_invalid_json(self):
        with patch('builtins.open', mock_open(read_data='invalid json')):
            result = FileReader.load_json('invalid_file.json')
            self.assertEqual(result, [])

    def test_load_json_success(self):
        test_file_path = os.path.join(
            os.path.dirname(__file__), 'test_transient_list.json'
        )
        with open(test_file_path) as f:
            mock_data = json.load(f)

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
            result = FileReader.load_json('valid_file.json')
            self.assertEqual(result, mock_data)

    def test_save_json_success(self):
        mock_data = [
            {
                "id": "9",
                "name": "Liza's Cambridge",
                "description": "This is not my house.",
                "location": "Bareng Drive",
                "price_per_head": 100,
                "contact": "09762969444",
            }
        ]
        with patch('builtins.open', mock_open()) as mocked_file:
            FileReader.save_json(mock_data, 'output_file.json')
            handle = mocked_file()
            handle.write.assert_called()

            calls = handle.write.call_args_list
            written_data = ''.join(call[0][0] for call in calls)
            expected_data = json.dumps(mock_data, indent=4)
            self.assertEqual(written_data.strip(), expected_data.strip())

    def test_save_json_exception(self):
        mock_data = [{"name": "Liza", "price_per_head": 100}]
        with patch('builtins.open', side_effect=Exception('File error')):
            with self.assertRaises(Exception):
                FileReader.save_json(mock_data, 'output_file.json')

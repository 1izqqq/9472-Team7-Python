from unittest import TestCase
from unittest.mock import patch
from util.reservation import reserve_dates

class TestReservation(TestCase):
    def setUp(self):
        self.transient = {
            'id': 1,
            'name': 'Cozy Cabin',
            'description': 'A nice cabin in the woods',
            'price_per_head': 100,
            'location': '123 Mountain Road',
            'availability': {
                '2024-10-20': {'status': 'AVAILABLE'},
                '2024-10-21': {'status': 'AVAILABLE'}
            }
        }
        self.available_dates = {'2024-10-20', '2024-10-21'}
        self.transients = [self.transient]

    @patch('builtins.input', side_effect=['y', 'Liza', '1', '2', '2', '1', 'y']) # Mocking multiple inputs
    def test_reserve_dates_successful(self, mock_input):
        result = reserve_dates(self.transient, self.available_dates, self.transients)
        self.assertIsNotNone(result)

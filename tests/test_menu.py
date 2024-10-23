import unittest
from unittest.mock import patch
from util.menu import Menu

class TestMenu(unittest.TestCase):
    def setUp(self):
        # Sample transient data for testing
        self.transients = [
            {
                "id": 1,
                "name": "Vista De Pino Transient House",
                "description": "A beautiful house with a scenic view.",
                "location": "31 Upper QM Baguio City",
                "price_per_head": 500,
                "contact": "09293375472",
                "availability": {
                    "2024-09-01": {
                        "status": "AVAILABLE",
                        "client_name": "",
                        "date_from": "",
                        "date_to": "",
                        "number_of_people": 0
                    },
                    "2024-09-02": {
                        "status": "AVAILABLE",
                        "client_name": "",
                        "date_from": "",
                        "date_to": "",
                        "number_of_people": 0
                    }

                }
            },
            {
                "id": 2,
                "name": "Analyn's Transient House",
                "description": "A cozy house in the heart of the city.",
                "location": "15 Happy Homes Campo Sioco Baguio City",
                "price_per_head": 550,
                "contact": "09486591743",
                "availability": {
                    "2024-09-07": {
                        "status": "AVAILABLE",
                        "client_name": "",
                        "date_from": "",
                        "date_to": "",
                        "number_of_people": 0
                    },
                    "2024-09-08": {
                        "status": "AVAILABLE",
                        "client_name": "",
                        "date_from": "",
                        "date_to": "",
                        "number_of_people": 0
                    }
                }
            }
        ]
        self.menu = Menu(self.transients)

    @patch('builtins.print')
    def test_print_main_menu(self, mock_print):
        self.menu.print_main_menu()
        mock_print.assert_any_call("\nMain Menu")
        mock_print.assert_any_call("1. Select transient to book")
        mock_print.assert_any_call("2. Sort transient list")
        mock_print.assert_any_call("3. Filter transient list")
        mock_print.assert_any_call("4. Exit Cozy Cabin")

    @patch('builtins.input', side_effect=['1'])  # Simulate user input
    @patch('reservation.show_available_dates', return_value=['2023-10-01', '2023-10-02'])
    @patch('reservation.reserve_dates')
    @patch('util.printing_methods.show_transient_table')
    def test_select_transient(self, mock_show_transient_table, mock_reserve_dates, mock_show_available_dates,
                              mock_input):
        mock_show_transient_table(self.transients)
        self.menu.select_transient()
        mock_show_transient_table.assert_called_once_with(self.transients)
        mock_reserve_dates.assert_called_once()

    @patch('builtins.input', side_effect=['1', '2'])  # Simulate sorting
    @patch('util.sort_filter.sort_transients_price')
    @patch('util.printing_methods.show_transient_table')
    def test_sort_transients(self, mock_show_transient_table, mock_sort_transients_price, mock_input):
        mock_sort_transients_price.return_value = self.transients
        self.menu.sort_transients('asc')
        mock_sort_transients_price.assert_called_once_with(self.transients, 'asc')
        mock_show_transient_table.assert_called_once_with(self.transients)

    @patch('builtins.input', side_effect=['1'])  # Simulate filtering
    @patch('util.sort_filter.filter_transients')
    @patch('util.printing_methods.show_transient_table')
    def test_apply_filter(self, mock_show_transient_table, mock_filter_transients, mock_input):
        mock_filter_transients.return_value = self.transients
        self.menu.apply_filter(1)
        mock_filter_transients.assert_called_once()
        mock_show_transient_table.assert_called_once_with(self.transients)

    @patch('builtins.exit')
    def test_exit_program(self, mock_exit):
        self.menu.exit_program()
        mock_exit.assert_called_once()

    @patch('builtins.input', side_effect=['y'])  # Mocking input to return 'y'
    def test_select_transient(self, mock_input):
        self.menu.select_transient()

if __name__ == '__main__':
    unittest.main()
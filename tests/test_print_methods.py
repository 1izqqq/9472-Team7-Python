import unittest
from unittest.mock import patch
from io import StringIO

from util.printing_methods import show_reservation_details, show_transient_table


class TestReservationFunctions(unittest.TestCase):

    def setUp(self):
        self.transients = [
            {
                "id": 1,
                "name": "Cozy Cabin",
                "location": "123 Mountain Road",
                "price_per_head": 100,
                "contact": "09123456789",
            },
            {
                "id": 2,
                "name": "Seaside Villa",
                "location": "456 Ocean Drive",
                "price_per_head": 150,
                "contact": "09876543210",
            },
        ]

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_transient_table(self, mock_stdout):
        show_transient_table(self.transients)
        output = mock_stdout.getvalue().strip()

        expected_output = (
            "+----+---------------+-------------------+------------+-------------+\n"
            "| ID |      Name     |      Address      | Price/Head |   Contact   |\n"
            "+----+---------------+-------------------+------------+-------------+\n"
            "| 1  |   Cozy Cabin  | 123 Mountain Road |    ₱100    | 09123456789 |\n"
            "| 2  | Seaside Villa |  456 Ocean Drive  |    ₱150    | 09876543210 |\n"
            "+----+---------------+-------------------+------------+-------------+"
        ).strip()

        self.assertEqual(output, expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_reservation_details(self, mock_stdout):
        details = {
            "client_name": "John Doe",
            "date_from": "2024-10-20",
            "date_to": "2024-10-22",
            "pay_method": "Credit Card",
            "number_of_people": 2,
            "num_nights": 2,
            "price_per_head": 100,
            "total_cost": 400,
        }

        show_reservation_details(**details)
        output = mock_stdout.getvalue().strip()

        expected_output = (
            "\nReservation Details\n"
            f"Client Name: {details['client_name']}\n"
            f"Reservation From: {details['date_from']}\n"
            f"Reservation To: {details['date_to']}\n"
            f"Payment method: {details['pay_method']}\n"
            f"Number of People: {details['number_of_people']}\n"
            f"Calculating cost for {details['number_of_people']} "
            f"people staying {details['num_nights']} "
            f"night/s at ₱{details['price_per_head']} "
            f"per person...\n"
            f"Total cost: ₱{details['total_cost']}"
        ).strip()

        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()

import unittest
from util.sort_filter import sort_transients_price, filter_transients  # Adjust the import based on your actual file structure

class TestSortFilter(unittest.TestCase):

    def setUp(self):
        self.transients = [
            {
                "id": 1,
                "name": "Cozy Cabin",
                "location": "123 Mountain Road",
                "price_per_head": 100
            },
            {
                "id": 2,
                "name": "Seaside Villa",
                "location": "456 Ocean Drive",
                "price_per_head": 150
            },
            {
                "id": 3,
                "name": "Mountain Retreat",
                "location": "789 Hilltop Lane",
                "price_per_head": 120
            }
        ]

    def test_sort_transients_price_ascending(self):
        sorted_transients = sort_transients_price(self.transients, "asc")
        self.assertEqual(sorted_transients[0]["name"], "Cozy Cabin")
        self.assertEqual(sorted_transients[1]["name"], "Mountain Retreat")
        self.assertEqual(sorted_transients[2]["name"], "Seaside Villa")

    def test_sort_transients_price_descending(self):
        sorted_transients = sort_transients_price(self.transients, "desc")
        self.assertEqual(sorted_transients[0]["name"], "Seaside Villa")
        self.assertEqual(sorted_transients[1]["name"], "Mountain Retreat")
        self.assertEqual(sorted_transients[2]["name"], "Cozy Cabin")

    def test_filter_transients_by_name(self):
        filtered_transients = filter_transients(self.transients, 1, "Cabin")
        self.assertEqual(len(filtered_transients), 1)
        self.assertEqual(filtered_transients[0]["name"], "Cozy Cabin")

    def test_filter_transients_by_location(self):
        filtered_transients = filter_transients(self.transients, 2, "Ocean")
        self.assertEqual(len(filtered_transients), 1)
        self.assertEqual(filtered_transients[0]["name"], "Seaside Villa")

    def test_filter_transients_no_match(self):
        filtered_transients = filter_transients(self.transients, 1,
                                                "Nonexistent")
        self.assertEqual(len(filtered_transients), 0)

    def test_filter_transients_invalid_choice(self):
        filtered_transients = filter_transients(self.transients, 3,
                                                "Some Query")
        self.assertEqual(filtered_transients, self.transients)

if __name__ == '__main__':
    unittest.main()

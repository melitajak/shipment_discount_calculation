#Usage: python -m unittest test_calculator.py

import unittest
from unittest.mock import patch, mock_open
from collections import defaultdict
from calculations import parse_input_file, calculate_shipping_price
from utils import check_transaction
from discount_rules import match_lowest_S_price, free_L_shipment, check_discount_limit
from constants import PRICES, POSSIBLE_SIZES, POSSIBLE_PROVIDERS

class TestShipmentDiscountCalculator(unittest.TestCase):

    # Set up the variables to be used
    def setUp(self):
        self.possible_sizes = POSSIBLE_SIZES
        self.possible_providers = POSSIBLE_PROVIDERS
        self.prices = PRICES

    #Tests if the check_transaction correctly processes valid transactions
    def test_check_transaction_valid(self):
        result = check_transaction("2025-01-01 S LP", self.possible_sizes, self.possible_providers)
        self.assertEqual(result, ("2025", "01", "2025-01-01", "S", "LP"))

    #Tests if the parse_input_file function correctly parses a file and ignores invalid lines.
    def test_parse_input_file(self):
        mock_data = "2015-02-24 L LP\n2015-02-29 CUSPS"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = parse_input_file("input.txt", self.possible_sizes, self.possible_providers)
        expected = [("2015", "02", "2015-02-24", "L", "LP"), "2015-02-29 CUSPS Ignored"]
        self.assertEqual(result, expected)

    #Test Rule 1, check if discount is calculated correctly, base price is not checked, because it is calculated in another function
    def test_match_lowest_S_price(self):
        _, discount = match_lowest_S_price(2.00, "S", 1.50)
        self.assertEqual(discount, 0.50)

        _, discount = match_lowest_S_price(1.50, "S", 1.50)
        self.assertEqual(discount, 0)

    #Test Rule 2, check if discount is calculated correctly, base price is not checked, because it is calculated in another function
    def test_free_L_shipment(self):
        lp_L_counter = defaultdict(int)
        _, discount = free_L_shipment("2024-12", "LP", "L", 6.90, lp_L_counter)
        self.assertEqual(discount, 0)

        lp_L_counter["2024-12"] = 2
        _, discount = free_L_shipment("2024-12", "LP", "L", 6.90, lp_L_counter)
        self.assertEqual(discount, 6.90)

    #Test Rule 3
    def test_check_discount_limit(self):
        monthly_discounts = defaultdict(float)

        #First discount of 4€
        base_price, discount = check_discount_limit(4, monthly_discounts, "2025-02", 6.00)
        self.assertEqual(discount, 4.00)
        self.assertEqual(base_price, 2.00)

        #Second discount of 3€
        base_price, discount = check_discount_limit(3, monthly_discounts, "2025-02", 3.00)
        self.assertEqual(discount, 3.00)
        self.assertEqual(base_price, 0.00) 

        #Third discount of 4€, but 3€ is left
        base_price, discount = check_discount_limit(4, monthly_discounts, "2025-02", 5.00)
        self.assertEqual(discount, 3.00)
        self.assertEqual(base_price, 2.00) 

        #Forth discount of 3€, but none is left
        base_price, discount = check_discount_limit(3, monthly_discounts, "2025-02", 4.00)
        self.assertEqual(discount, 0.00)
        self.assertEqual(base_price, 4.00) 

    #Test the full discount calculation generally and also tests if third large LP shipment is free and its base price,
    #as well as if the remaining discount (if not enough to cover full) is calculated correctly for small shipment
    def test_calculate_shipping_price(self):
        transactions = [("2015", "02", "2015-02-01", "S", "MR"),
                        ("2015", "02", "2015-02-02", "S", "MR"), 
                        ("2015", "02", "2015-02-03", "L", "LP"), 
                        ("2015", "02", "2015-02-04", "L", "LP"),
                        ("2015", "02", "2015-02-05", "L", "LP"),
                        ("2015", "02", "2015-02-06", "S", "MR"),
                        ("2015", "02", "2015-02-06", "S", "MR"),
                        ("2015", "02", "2015-02-07", "S", "MR"),
                        ("2015", "02", "2015-02-08", "S", "MR"),
                        ("2015", "02", "2015-02-08", "S", "MR"),
                        "invalid line Ignored"]
        
        result = calculate_shipping_price(transactions)

        expected_result = [
            "2015-02-01 S MR 1.50 0.50",
            "2015-02-02 S MR 1.50 0.50",
            "2015-02-03 L LP 6.90 -",
            "2015-02-04 L LP 6.90 -",
            "2015-02-05 L LP 0.00 6.90",  #Third L package
            "2015-02-06 S MR 1.50 0.50",
            "2015-02-06 S MR 1.50 0.50",
            "2015-02-07 S MR 1.50 0.50",
            "2015-02-08 S MR 1.50 0.50",
            "2015-02-08 S MR 1.90 0.10", #The remaining discount is not enough to cover full shipping
            "invalid line Ignored" #Invalid line
        ]
        
        self.assertEqual(result, expected_result) 
        

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import mock_open, patch

# Updated imports from the new modular structure
from inventory_and_billing.models.base_models import Product, Electronics, Clothing, Food
from inventory_and_billing.models.exceptions import OutofStockError
from inventory_and_billing.services.order_processor import process_order
from inventory_and_billing.services.file_ops import load_products


# ------------------ Product Calculation Tests ------------------ #
class TestProductCalculations(unittest.TestCase):

    def test_base_product_total(self):
        p = Product("P001", "Generic", "Misc", 100, 10)
        self.assertEqual(p.calculate_total(2), 200)

    def test_electronics_total_with_tax(self):
        e = Electronics("E001", "Headphones", "Electronics", 100, 5)
        expected = 100 * 2 * 1.18
        self.assertAlmostEqual(e.calculate_total(2), expected, places=2)

    def test_clothing_total_with_discount(self):
        c = Clothing("C001", "T-Shirt", "Clothing", 50, 5)
        expected = 50 * 2 * 0.9
        self.assertAlmostEqual(c.calculate_total(2), expected, places=2)

    def test_food_total_with_tax(self):
        f = Food("F001", "Bread", "Food", 10, 10)
        expected = 10 * 3 * 1.05
        self.assertAlmostEqual(f.calculate_total(3), expected, places=2)


# ------------------ Order Processing Tests ------------------ #
class TestOrderProcessing(unittest.TestCase):

    def setUp(self):
        self.products = [
            Electronics("E001", "Mouse", "Electronics", 200, 5),
            Clothing("C001", "Shirt", "Clothing", 100, 10),
            Food("F001", "Milk", "Food", 50, 3)
        ]

    def test_successful_order_reduces_stock(self):
        order = {"Mouse": 2}
        grand_total = process_order(self.products, order)
        self.assertAlmostEqual(grand_total, 200 * 2 * 1.18, places=2)
        self.assertEqual(self.products[0].stock, 3)

    def test_out_of_stock_raises_exception(self):
        order = {"Milk": 5}  # only 3 in stock
        with self.assertRaises(OutofStockError):
            process_order(self.products, order)


# ------------------ File Operations Tests ------------------ #
class TestFileOperations(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="E001,Mouse,Electronics,200,5\n")
    def test_load_products_creates_correct_instance(self, mock_file):
        products = load_products("mock_products.txt")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Mouse")
        self.assertIsInstance(products[0], Electronics)


# ------------------ Bill Calculation Logic ------------------ #
class TestBillCalculation(unittest.TestCase):

    def test_grand_total_calculation(self):
        order = {"Mouse": 2, "Shirt": 1}
        products = [
            Electronics("E001", "Mouse", "Electronics", 200, 5),
            Clothing("C001", "Shirt", "Clothing", 100, 10),
        ]
        grand_total = process_order(products, order)
        expected_total = (200 * 2 * 1.18) + (100 * 1 * 0.9)
        self.assertAlmostEqual(grand_total, expected_total, places=2)


if __name__ == "__main__":
    unittest.main()

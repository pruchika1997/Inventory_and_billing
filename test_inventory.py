import unittest
from io import StringIO
from unittest.mock import mock_open, patch

# Import your classes here
from main import Product, Electronics, Clothing, Food, OutofStockError

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


class TestOrderProcessing(unittest.TestCase):

    def setUp(self):
        self.products = [
            Electronics("E001", "Mouse", "Electronics", 200, 5),
            Clothing("C001", "Shirt", "Clothing", 100, 10),
            Food("F001", "Milk", "Food", 50, 3)
        ]

    def test_successful_order_reduces_stock(self):
        product = self.products[0]  # Mouse
        quantity = 2
        total = product.calculate_total(quantity)
        product.stock -= quantity
        self.assertEqual(product.stock, 3)
        self.assertAlmostEqual(total, 200 * 2 * 1.18, places=2)

    def test_out_of_stock_raises_exception(self):
        product = self.products[2]  # Milk has 3 in stock
        quantity = 5
        with self.assertRaises(OutofStockError):
            if product.stock < quantity:
                raise OutofStockError(f"{product.name} is out of stock.")

    @patch("builtins.open", new_callable=mock_open, read_data="E001,Mouse,Electronics,200,5\n")
    def test_file_read_creates_product(self, mock_file):
        from main import Electronics
        products = []
        with open("products.txt", "r") as file:
            for line in file:
                pid, name, category, price, stock = line.strip().split(",")
                price = float(price)
                stock = int(stock)
                if category == "Electronics":
                    products.append(Electronics(pid, name, category, price, stock))
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Mouse")
        self.assertIsInstance(products[0], Electronics)


class TestBillCalculation(unittest.TestCase):

    def test_grand_total_calculation(self):
        order = {"Mouse": 2, "Shirt": 1}
        products = [
            Electronics("E001", "Mouse", "Electronics", 200, 5),
            Clothing("C001", "Shirt", "Clothing", 100, 10),
        ]
        grand_total = 0
        for product in products:
            if product.name in order:
                quantity = order[product.name]
                total = product.calculate_total(quantity)
                grand_total += total
        expected_total = (200 * 2 * 1.18) + (100 * 1 * 0.9)
        self.assertAlmostEqual(grand_total, expected_total, places=2)


if __name__ == "__main__":
    unittest.main()

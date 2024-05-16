import unittest
from bs4 import BeautifulSoup
from components.MonthlyRevenueModel import MonthlyRevenueModel


class TestMonthlyRevenueModel(unittest.TestCase):
    def test_queryData(self):
        monthlyRevenue = MonthlyRevenueModel()
        new_data = monthlyRevenue.queryData(113,1)
        self.assertIsInstance(new_data[0], [])

if __name__ == '__main__':
    unittest.main()
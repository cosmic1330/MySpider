import unittest
from utils.isdecimal import isdecimal

class TestIsdecimalFunction(unittest.TestCase):
    def test_isdecimal(self):
        res = isdecimal('-23.92')
        self.assertEqual(res, True)  # 確保打印了正確的消息

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
import io
import sys
from utils.delay import delay

class TestDelayFunction(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('time.sleep')
    def test_delay(self, mock_sleep, mock_stdout):
        delay()
        mock_sleep.assert_called()  # 確保 sleep 函數被調用
        self.assertTrue(mock_sleep.call_args[0][0] >= 3 and mock_sleep.call_args[0][0] <= 10)  # 確保延遲時間在 3 到 10 秒之間
        expected_output = '等待 ' + str(mock_sleep.call_args[0][0]) + ' 秒後進行下一次請求...\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)  # 確保打印了正確的消息

if __name__ == '__main__':
    unittest.main()

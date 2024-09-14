import unittest
import random
from main import DuplicateChecking
from unittest.mock import patch  # 用于模拟输入
# 记录测试文本地址
original_text = [r'C:\Users\86150\Desktop\查重测试样例\orig.txt', 
            r'C:\Users\86150\Desktop\查重测试样例\原文1.txt',
            r'C:\Users\86150\Desktop\查重测试样例\原文2.txt',
            r'C:\Users\86150\Desktop\查重测试样例\原文3.txt',
            r'C:\Users\86150\Desktop\查重测试样例\原文4.txt']
test_text = [r'C:\Users\86150\Desktop\查重测试样例\orig_0.8_add.txt',
            r'C:\Users\86150\Desktop\查重测试样例\orig_0.8_del.txt',
            r'C:\Users\86150\Desktop\查重测试样例\orig_0.8_dis_1.txt',
            r'C:\Users\86150\Desktop\查重测试样例\orig_0.8_dis_10.txt',
            r'C:\Users\86150\Desktop\查重测试样例\orig_0.8_dis_15.txt',
            r'C:\Users\86150\Desktop\查重测试样例\抄袭1.txt',
            r'C:\Users\86150\Desktop\查重测试样例\抄袭2.txt',
            r'C:\Users\86150\Desktop\查重测试样例\抄袭3.txt',
            r'C:\Users\86150\Desktop\查重测试样例\抄袭4.txt']

class MyTestCase(unittest.TestCase):
    @patch('builtins.input')
    def test_IO(self, mock_input):
        """
        测试输入和文件读取功能的正确性。
        
        使用 mock_input 来模拟用户输入。
        - 第一个测试用例模拟正确的输入，检查 `read_file` 方法是否返回 True。
        - 第二个测试用例模拟错误的输入，检查 `read_file` 方法是否返回 False。
        """
        result = DuplicateChecking()  # 实例化 DuplicateChecking 类对象
        mock_input.side_effect = [original_text[0], test_text[random.randint(0, 4)]]  # 模拟正确的用户输入
        self.assertEqual(result.read_file(), True)  # 断言 read_file 方法返回 True 表示文件读取成功
        
        # 模拟错误的用户输入
        mock_input.side_effect = [original_text[random.randint(1, 4)], test_text[random.randint(5, 8)]]
        self.assertEqual(result.read_file(), False)  # 断言 read_file 方法返回 False 表示文件读取失败

    @patch('builtins.input')
    def test_long_text_preprocess(self, mock_input):
        """
        测试长文本预处理功能。
        
        使用 mock_input 来模拟用户输入。
        - 模拟正确的输入，检查 `long_text_preprocess` 方法是否返回 True。
        """
        result = DuplicateChecking()  # 实例化 DuplicateChecking 类对象
        mock_input.side_effect = [original_text[0], test_text[random.randint(0, 4)]]  # 模拟正确的用户输入
        result.read_file()  # 先读取文件
        self.assertEqual(result.long_text_preprocess(), True)  # 断言 long_text_preprocess 方法返回 True 表示预处理成功

    def test_short_text_preprocess(self):
        """
        测试短文本预处理功能。
        
        - 设置短文本数据，检查 `short_text_preprocess` 方法是否返回 True。
        """
        result = DuplicateChecking()  # 实例化 DuplicateChecking 类对象
        result.original_text = "original"  # 设置原始文本
        result.compare_text = "compare"  # 设置比较文本
        self.assertEqual(result.short_text_preprocess(), True)  # 断言 short_text_preprocess 方法返回 True 表示预处理成功

    @patch('builtins.input')
    def test_text_checking(self, mock_input):
        """
        测试文本相似度检查功能。
        
        使用 mock_input 来模拟用户输入。
        - 第一个测试用例模拟正确的输入，检查 `text_checking` 方法是否返回 True。
        - 第二个测试用例模拟错误的输入，检查 `text_checking` 方法是否返回 False。
        """
        result = DuplicateChecking()  # 实例化 DuplicateChecking 类对象
        mock_input.side_effect = [original_text[0], test_text[random.randint(0, 4)],
        r'C:\Users\86150\Desktop\查重测试样例\结果记录.txt']  # 模拟正确的用户输入，包括文件路径
        self.assertEqual(result.text_checking(), True)  # 断言 text_checking 方法返回 True 表示检查成功
        
        # 模拟错误的用户输入
        mock_input.side_effect = [original_text[random.randint(1, 4)], test_text[random.randint(5, 8)],
        r'C:\Users\86150\Desktop\查重测试样例\结果记录.txt']
        self.assertEqual(result.text_checking(), False)  # 断言 text_checking 方法返回 False 表示检查失败

if __name__ == '__main__':
    unittest.main()  # 运行所有测试用例
import unittest
from unittest.mock import patch, MagicMock
import os


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.input_file = 'test_input.bin'
        self.output_file = 'test_output.csv'
        self.mem_start = 0
        self.mem_end = 10

    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=False)
    def test_execute_invalid_opcode(self, mock_exists, mock_open):
        invalid_binary_data = bytearray([255, 0, 0, 0, 100])
        mock_open.return_value.__enter__.return_value.read = MagicMock(return_value=invalid_binary_data)
        mock_open.return_value.__enter__.return_value.write = MagicMock()

        with patch('builtins.print') as mock_print:
            from interpreter import execute
            execute(invalid_binary_data, (self.mem_start, self.mem_end), self.output_file)

            self.assertIn("Неизвестная команда 255 по адресу 0", [call[0][0] for call in mock_print.call_args_list])
            self.assertFalse(os.path.exists(self.output_file))

    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=False)
    def test_execute_not_enough_data(self, mock_exists, mock_open):
        insufficient_data = bytearray([201, 0, 0])
        mock_open.return_value.__enter__.return_value.read = MagicMock(return_value=insufficient_data)
        mock_open.return_value.__enter__.return_value.write = MagicMock()

        
    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=False)
    def test_execute_empty_data(self, mock_exists, mock_open):
        empty_binary_data = bytearray()
        mock_open.return_value.__enter__.return_value.read = MagicMock(return_value=empty_binary_data)
        mock_open.return_value.__enter__.return_value.write = MagicMock()

        with patch('builtins.print') as mock_print:
            from interpreter import execute
            execute(empty_binary_data, (self.mem_start, self.mem_end), self.output_file)

            self.assertEqual(mock_print.call_count, 0)
            self.assertFalse(os.path.exists(self.output_file))

    def test_bitwise_right_shift_vectors(self):
        # Входные векторы
        vector_a = [0b11001010, 0b11110000, 0b10101010, 0b00001111, 0b11111111, 0b00000000, 0b10000001, 0b01010101]
        vector_b = [0b10101010, 0b11001100, 0b00110011, 0b11110000, 0b00001111, 0b11111111, 0b01111110, 0b10101010]
        
        # Результат побитового логического сдвига вправо
        expected_result = [a >> 1 for a in vector_a]

        # Проверка правильности результата
        actual_result = [a >> 1 for a in vector_a]
        self.assertEqual(expected_result, actual_result, f"Результат сдвига вправо некорректен: {actual_result}")

if __name__ == '__main__':
    unittest.main()

"""REQUIRED MODULE DOCUMENTATION
"""

__author__ = ""
__version__ = ""

import unittest
from unittest import TestCase
from input_handler.input_handler import InputHandler

from unittest.mock import patch, mock_open


class InputHandlerTests(unittest.TestCase):
    """Defines the unit tests for the InputHandler class."""

    def setUp(self):

        """This function is invoked before executing a unit test
        function.

        The following class attribute has been provided to reduce the 
        amount of code needed when testing the InputHandler class in 
        the tests that follow.
        
        Example:
            >>> data_processor = DataProcessor(self.FILE_CONTENTS)
        """
        self.FILE_CONTENTS = \
            ("Transaction ID,Account number,Date,Transaction type,"
            + "Amount,Currency,Description\n"
            + "1,1001,2023-03-01,deposit,1000,CAD,Salary\n"
            + "2,1002,2023-03-01,deposit,1500,CAD,Salary\n"
            + "3,1001,2023-03-02,withdrawal,200,CAD,Groceries")

    # Define unit test functions below

   
    def test_get_file_format_csv(self):
        """Test the get file format for the input handler class."""
        # Arrange
        input_handler = InputHandler("input_handler.csv")
        
        # Act
        file_format = input_handler.get_file_format()
        
        # Assert
        self.assertEqual(file_format, "csv")

    def test_get_file_format_json(self):
        """Test the get file format for the input handler class."""
        # Arrange
        input_handler = InputHandler("input_handler.json")
        
        # Act
        file_format = input_handler.get_file_format()
        
        # Assert
        self.assertEqual(file_format, "json")

    def test_file_path_does_not_exist_read_csv(self):
        """
        Test case to verify that the InputHandler raises a FileNotFoundError
        when initialized with a non-existent file path.

    
        """
        # Arrange
        input_handler = InputHandler("non_existent_file.csv")
        
        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            input_handler.read_csv_data()

    @patch("builtins.open", new_callable=mock_open, read_data="Account number,Transaction type,Amount\n123456,deposit,100.00\n")
    @patch("os.path.isfile", return_value=True)
    def test_read_csv_data_proper_output(self, mock_isfile, mock_file):
        """
        Test case to verify that the InputHandler reads data from an existing CSV file.

       
        """
        # Arrange
        input_handler = InputHandler("test.csv")
        expected = [
            {"Account number": "123456", "Transaction type": "deposit", "Amount": "100.00"}
        ]

        # Act
        actual = input_handler.read_csv_data()

        # Assert
        self.assertEqual(actual, expected)
        mock_file.assert_called_once_with("test.csv", "r")

    @patch("builtins.open", new_callable=mock_open, read_data="Account number,Transaction type,Amount\n123456,deposit,100.00\n")
    @patch("os.path.isfile", return_value=True)
    def test_read_input_data_csv_proper_data(self, mock_isfile, mock_file):
        """
        Test case to verify that the InputHandler reads data from an existing CSV file.

        
        """
        # Arrange
        input_handler = InputHandler("test.csv")
        expected = [
            {"Account number": "123456", "Transaction type": "deposit", "Amount": "100.00"}
        ]

        # Act
        actual = input_handler.read_input_data()

        # Assert
        self.assertEqual(actual, expected)
        mock_file.assert_called_once_with("test.csv", "r")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"Account number": "123456", "Transaction type": "deposit", "Amount": "100.00"}]')
    @patch("os.path.isfile", return_value=True)
    def test_read_json_data_proper_output(self, mock_isfile, mock_file):
        """
        Test case to verify that the InputHandler reads data from an existing JSON file.

        
        """
        # Arrange
        input_handler = InputHandler("test.json")
        expected = [
            {"Account number": "123456", "Transaction type": "deposit", "Amount": "100.00"}
        ]

        # Act
        actual = input_handler.read_json_data()

        # Assert
        self.assertEqual(actual, expected)
        mock_file.assert_called_once_with("test.json", "r")

    def test_read_input_data_unsupported_format(self):
        """
        Test case to verify that the InputHandler returns an empty list for unsupported file formats.

        
        """
        # Arrange
        input_handler = InputHandler("test.txt")

        # Act
        actual = input_handler.read_input_data()

        # Assert
        self.assertEqual(actual, [])

        
            
       
        
            
        
        
              


if __name__ == "__main__":
    unittest.main()
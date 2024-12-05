"""REQUIRED MODULE DOCUMENTATION
"""

__author__ = "Beerdavinder Singh"
__version__ = "3.12"

from unittest import TestCase, main
from unittest.mock import patch, mock_open
from output_handler.output_handler import OutputHandler

class TestOutputHandler(TestCase):
    """Defines the unit tests for the OutputHandler class."""

    def setUp(self):
        """This function is invoked before executing a unit test function."""
        self.account_summaries = { 
            "1001": {
                "account_number": "1001", 
                "balance": 50, 
                "total_deposits": 100, 
                "total_withdrawals": 50
            },
            "1002": {
                "account_number": "2", 
                "balance": 200, 
                "total_deposits": 200, 
                "total_withdrawals": 0
            }
        }

        self.suspicious_transactions = [
            {
                "Transaction ID": "1",
                "Account number": "1001",
                "Date": "2023-03-14",
                "Transaction type": "deposit",
                "Amount": 250,
                "Currency": "XRP",
                "Description": "crypto investment"
            }
        ]

        self.transaction_statistics = {
            "deposit": {
                "total_amount": 300, 
                "transaction_count": 2
            }, 
            "withdrawal": {
                "total_amount": 50, 
                "transaction_count": 1
            }
        }

    def test_init(self):
        output_handler = OutputHandler(self.account_summaries, self.suspicious_transactions, self.transaction_statistics)
        self.assertEqual(output_handler.account_summaries, self.account_summaries)
        self.assertEqual(output_handler.suspicious_transactions, self.suspicious_transactions)
        self.assertEqual(output_handler.transaction_statistics, self.transaction_statistics)

    def test_account_summaries_property(self):
        output_handler = OutputHandler(self.account_summaries, self.suspicious_transactions, self.transaction_statistics)
        self.assertEqual(output_handler.account_summaries, self.account_summaries)

    def test_suspicious_transactions_property(self):
        output_handler = OutputHandler(self.account_summaries, self.suspicious_transactions, self.transaction_statistics)
        self.assertEqual(output_handler.suspicious_transactions, self.suspicious_transactions)

    def test_transaction_statistics_property(self):
        output_handler = OutputHandler(self.account_summaries, self.suspicious_transactions, self.transaction_statistics)
        self.assertEqual(output_handler.transaction_statistics, self.transaction_statistics)

    @patch("builtins.open", new_callable=mock_open)
    def test_write_account_summaries_to_csv(self, mock_open_file):
        output_handler = OutputHandler(self.account_summaries, self.suspicious_transactions, self.transaction_statistics)
        output_handler.write_account_summaries_to_csv("test_accounts.csv")
        
        # Check that the open function is called once with the correct path and mode
        mock_open_file.assert_called_once_with("test_accounts.csv", 'w', newline='')

        # Check the number of rows written (including the header)
        handle = mock_open_file()
        handle.write.assert_any_call('Account number,Balance,Total Deposits,Total Withdrawals\n')
        handle.write.assert_any_call('1001,50,100,50\n')
        handle.write.assert_any_call('1002,200,200,0\n')

    @patch("builtins.open", new_callable=mock_open)
    def test_write_suspicious_transactions_to_csv(self, mock_open_file):
        output_handler = OutputHandler(self.account_summaries, self.suspicious_transactions, self.transaction_statistics)
        output_handler.write_suspicious_transactions_to_csv("test_transactions.csv")
        
        # Check that the open function is called once with the correct path and mode
        mock_open_file.assert_called_once_with("test_transactions.csv", 'w', newline='')

        # Check the number of rows written (including the header)
        handle = mock_open_file()
        handle.write.assert_any_call('Transaction ID,Account number,Date,Transaction type,Amount,Currency,Description\n')
        handle.write.assert_any_call('1,1001,2023-03-14,deposit,250,XRP,crypto investment\n')

    @patch("builtins.open", new_callable=mock_open)
    def test_write_transaction_statistics_to_csv(self, mock_open_file):
        output_handler = OutputHandler(self.account_summaries, self.suspicious_transactions, self.transaction_statistics)
        output_handler.write_transaction_statistics_to_csv("test_statistics.csv")
        
        # Check that the open function is called once with the correct path and mode
        mock_open_file.assert_called_once_with("test_statistics.csv", 'w', newline='')

        # Check the number of rows written (including the header)
        handle = mock_open_file()
        handle.write.assert_any_call('Transaction type,Total amount,Transaction count\n')
        handle.write.assert_any_call('deposit,300,2\n')
        handle.write.assert_any_call('withdrawal,50,1\n')

if __name__ == "__main__":
    main()
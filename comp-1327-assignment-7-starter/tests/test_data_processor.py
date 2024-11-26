"""REQUIRED MODULE DOCUMENTATION
"""

__author__ = ""
__version__ = ""

import unittest
from unittest import TestCase
from data_processor.data_processor import DataProcessor

class TestDataProcessor(TestCase):
    """Defines the unit tests for the DataProcessor class."""

    def setUp(self):
        """This function is invoked before executing a unit test
        function.

        The following class attribute has been provided to reduce the 
        amount of code needed when creating DataProcessor class objects 
        in the tests that follow.  
        
        Example:
            >>> data_processor = DataProcessor(self.transactions)
        """
        
        self.transactions = [
            {
                #for deposit (0)
                "Transaction ID": "1",
                "Account number": "1001",
                "Date": "2023-03-01",
                "Transaction type": "deposit",
                "Amount": 1000,
                "Currency": "CAD",
                "Description": "Salary"
            }, 
            {   #for withdrawal (1)
                "Transaction ID": "2",
                "Account number": "1002",
                "Date": "2023-03-01",
                "Transaction type": "withdrawal",
                "Amount": 1500,
                "Currency": "CAD",
                "Description": "Salary"
            },
            {   #passes the large transaction threshold (2)
                "Transaction ID": "3",
                "Account number": "1003",
                "Date": "2023-03-01",
                "Transaction type": "withdrawal",
                "Amount": 15000,
                "Currency": "CAD",
                "Description": "Salary"
            },
            {   #uncommon currency (3)
                "Transaction ID": "3",
                "Account number": "1003",
                "Date": "2023-03-01",
                "Transaction type": "withdrawal",
                "Amount": 1500,
                "Currency": "XRP",
                "Description": "Salary"
            }
        ]

#update account summary unit tests
    #tests that a deposit gets properly updated in the account summary
    def test_update_account_summary_deposit(self):
        self.setUp()
        
    #arrange
        test = DataProcessor(self.transactions)
        #saves the first transaction in transactions
        transaction = self.transactions[0]
        expected = {'account_number': '1001', 'balance': 1000, 'total_deposits': 1000, 'total_withdrawals': 0}
        
    #act
        test.update_account_summary(transaction)
        actual = test.account_summaries["1001"]
        
    #assert
        self.assertEqual(expected, actual)
    
    #tests that a withdrawal gets properly updated in the account summary
    def test_update_account_summary_withdrawal(self):
        self.setUp()
        
    #arrange
        test = DataProcessor(self.transactions)
        #saves the second transaction in transactions
        transaction = self.transactions[1]
        expected = {'account_number': '1002', 'balance': -1500, 'total_deposits': 0, 'total_withdrawals': 1500}
        
    #act
        test.update_account_summary(transaction)
        actual = test.account_summaries["1002"]
        
    #assert
        self.assertEqual(expected, actual)
        
#check suspicous transactions unit test
    #checks if a suspicious transaction is made when the amount passes 10000
    def test_suspicious_transactions_threshold(self):
        self.setUp()
    
    #arrange
        test = DataProcessor(self.transactions)
        #saves the third transaction in transactions
        expected = self.transactions[2]
        
    #act
        test.check_suspicious_transactions(expected)
        
    #assert
        self.assertTrue(expected in test.suspicious_transactions)
        
    #checks if a suspicious transaction is made when there is an uncommon currency
    def test_suspicious_transactions_uncommon(self):
        self.setUp()
    
    #arrange
        test = DataProcessor(self.transactions)
        #saves the fourth transaction in transactions
        expected = self.transactions[3]
        
    #act
        test.check_suspicious_transactions(expected)
        
    #assert
        self.assertTrue(expected in test.suspicious_transactions)
        
    #checks that a transaction is not added if it isnt suspicious
    def test_not_suspicious_transaction(self):
        self.setUp()
    
    #arrange
        test = DataProcessor(self.transactions)
        #saves the first transaction in transactions
        expected = self.transactions[0]
        
    #act
        test.check_suspicious_transactions(expected)
        
    #assert
        self.assertTrue(expected not in test.suspicious_transactions)

#test that the transaction statistics update properly
    def test_update_transaction_statistics(self):
        self.setUp()
        
    #arrange
        test = DataProcessor(self.transactions)
        #saves the first transaction in transactions
        transaction = self.transactions[0]
        expected = {'total_amount': 1000.0, 'transaction_count': 1}
        
    #act
        test.update_transaction_statistics(transaction)
        actual = test.transaction_statistics["deposit"]
        
    #assert
        self.assertEqual(expected, actual)
    
if __name__ == "__main__":
    unittest.main()

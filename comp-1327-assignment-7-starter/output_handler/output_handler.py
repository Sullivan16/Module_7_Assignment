"""REQUIRED MODULE DOCUMENTATION
"""

__author__ = "Beerdavinder Singh"
__version__ = "3.12"

import csv
 
class OutputHandler:
    """
    A class to handle output operations including writing data to CSV files.
    """
 
    def __init__(self, account_summaries: dict, 
                       suspicious_transactions: list, 
                       transaction_statistics: dict) -> None:
        """
        Initialize the OutputHandler with account summaries, suspicious transactions,
        and transaction statistics.
 
        Args:
            account_summaries (dict): A dictionary containing account summaries.
            suspicious_transactions (list): A list of suspicious transactions.
            transaction_statistics (dict): A dictionary containing transaction statistics.
        """
        self.__account_summaries = account_summaries
        self.__suspicious_transactions = suspicious_transactions
        self.__transaction_statistics = transaction_statistics

    @property
    def account_summaries(self):
        """
        Get the account summaries.
 
        Returns:
            dict: A dictionary containing account summaries.
        """
        return self.__account_summaries

    @property
    def suspicious_transactions(self):
        """
        Get the suspicious transactions.
 
        Returns:
            list: A list of suspicious transactions.
        """
        return self.__suspicious_transactions

    @property
    def transaction_statistics(self):
        """
        Get the transaction statistics.
 
        Returns:
            dict: A dictionary containing transaction statistics.
        """
        return self.__transaction_statistics
 
    def write_account_summaries_to_csv(self, file_path: str) -> None:
        """
        Write account summaries to a CSV file.
 
        Args:
            file_path (str): The file path where the CSV file will be saved.
        """
        with open(file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Account number', 'Balance', 'Total Deposits', 'Total Withdrawals'])
 
            for account_number, summary in self.__account_summaries.items():
                writer.writerow([
                    account_number,
                    summary['balance'],
                    summary['total_deposits'],
                    summary['total_withdrawals']
                ])
 
    def write_suspicious_transactions_to_csv(self, file_path: str) -> None:
        """
        Write suspicious transactions to a CSV file.
 
        Args:
            file_path (str): The file path where the CSV file will be saved.
        """
        with open(file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Transaction ID', 'Account number', 'Date', 'Transaction type', 'Amount', 'Currency', 'Description'])
 
            for transaction in self.__suspicious_transactions:
                writer.writerow([
                    transaction['Transaction ID'],
                    transaction['Account number'],
                    transaction['Date'],
                    transaction['Transaction type'],
                    transaction['Amount'],
                    transaction['Currency'],
                    transaction['Description']
                ])
 
    def write_transaction_statistics_to_csv(self, file_path: str) -> None:
        """
        Write transaction statistics to a CSV file.
 
        Args:
            file_path (str): The file path where the CSV file will be saved.
        """        
        with open(file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Transaction type', 'Total amount', 'Transaction count'])
 
            for transaction_type, statistic in self.__transaction_statistics.items():
                writer.writerow([
                    transaction_type,
                    statistic['total_amount'],
                    statistic['transaction_count']
                ])
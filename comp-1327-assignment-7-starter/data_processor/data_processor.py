"""
Includes the DataProcessor class, which processes the transactions using the transactions list
"""

__author__ = "D Synkiw"
__version__ = "1.0"

import logging

class DataProcessor:
    """
    Processes transactions, updates the account summary, processes suspicious transactions,
    updates the transaction statistics, and gets the average transaction amount
    """
    
    #the threshhold for what transactions are labelled as suspicious
    LARGE_TRANSACTION_THRESHOLD = 10000

    #if the currency is one of these labels the transaction will be flagged as suspicious
    UNCOMMON_CURRENCIES = ["XRP", "LTC"]


    def __init__(self, transactions: list, logging_level = "WARNING", logging_format = "%(asctime)s - %(levelname)s - %(message)s", logging_file = ""):
        """
        initializes the the class, takes a list of transactions as an argument, creating the variables for the class
        also sets the default parameters for logging.
        
        Args:
            transactions (list): list of all the transactions from a csv or json file 
            logging_level (str): the default logging level for the class (default: "WARNING")
            logging_format (str): the default logging format for the class (default: "%(asctime)s - %(levelname)s - %(message)s")
            logging_file (str): the default name for the logging file for the class (default: "")
            
        Returns: None
        
        Raises: None
        """
        
        logging.basicConfig(level  = logging_level,
                            format = logging_format,
                            filemode = "w",
                            filename = logging_file)
        
        self.logger = logging.getLogger(__name__)
        
        self.__transactions = transactions
        
        #dictionary of all of the accounts and their account number, balances, withdrawels, and deposits (see update_account_summary)
        self.__account_summaries = {}
        
        #list of any transactions that are labelled suspicious (see check_suspicious_transactions)
        self.__suspicious_transactions = []
        
        #saves a dictionary of all transactions under an account, keeping a total amount of money in an account
        #and how many transactions are made(see update_transaction_statistics)
        self.__transaction_statistics = {}

    @property
    def input_data(self) -> list:
        """
        accessor for the transactions list from the input data
        
        Args: None
        
        Returns: 
            list: a list of the transactions
            
        Raises: None
        """
        return self.__transactions
    
    @property
    def account_summaries(self) -> dict:
        """
        accessor for the account_summary
        
        Args: None
        
        Returns
            dict: a dictionary of the account summary(initialized as an empty dict)
            
        Raises: None
        
        """
        return self.__account_summaries
    
    @property
    def suspicious_transactions(self) -> list:
        """
        accessor for the suspicious transactions list
        
        Args: None
        
        Returns:
            list: list of suspicious transactions(initialized as an empty list)
            
        Raises: None
        """
        return self.__suspicious_transactions
    
    @property
    def transaction_statistics(self) -> dict:
        """
        accessor for the transactions statistics dictionary
        
        Args: None
        
        Returns:
            dict: dictionary of the transaction statistics(initailized as an empty dict)
        Raises: None
        """
        return self.__transaction_statistics

    def process_data(self) -> dict:
        """
        Processes the data by calling the other three instance methods in the class
        
        Args: None
        
        Returns:
            dict: returns account_summaries, suspicious_transactions, and transaction statistics as the keys 
                and the output of their respective methods as the values of a dictionary
        
        Raises: None
        """
        
        #runs these three methods for every transaction within the transactions list
        for transaction in self.__transactions:
            self.update_account_summary(transaction)
            self.check_suspicious_transactions(transaction)
            self.update_transaction_statistics(transaction)

        self.logger.info("Data Processing Complete")
        return {
            "account_summaries": self.__account_summaries,
            "suspicious_transactions": self.__suspicious_transactions,
            "transaction_statistics": self.__transaction_statistics
        }

    def update_account_summary(self, transaction: dict) -> None:
        """
        updates the acccount summary by using the data in the transaction dictionary, if the account is  already saved in account_summaries it updates it,
            if not, it creates a new one
            
        Args: 
            transaction (dict): a given transaction dictionary that contains the relevant data of the account number, transaction type, and amount
            
        Returns: None
        
        Raises: None
        """
        
        #takes the relevant info from the transaction and saves it to local variables
        account_number = transaction["Account number"]
        transaction_type = transaction["Transaction type"]
        amount = float(transaction["Amount"])

        #if a given account number hasnt been encountered yet it creates an account summary for that account
        if account_number not in self.__account_summaries:
            self.__account_summaries[account_number] = {
                "account_number": account_number,
                "balance": 0,
                "total_deposits": 0,
                "total_withdrawals": 0
            }

        #updates the balance and total deposits/withdrawels within the account summary depending on the transaction type
        if transaction_type == "deposit":
            self.__account_summaries[account_number]["balance"] += amount
            self.__account_summaries[account_number]["total_deposits"] += amount
        elif transaction_type == "withdrawal":
            self.__account_summaries[account_number]["balance"] -= amount
            self.__account_summaries[account_number]["total_withdrawals"] += amount
        self.logger.info(f"Account summary updated: {self.__account_summaries[account_number]}")

    def check_suspicious_transactions(self, transaction: dict) -> None:
        """
        checks for suspicious transactions using the LARGE_TRANSACTION_THRESHOLD and UNCOMMON_CURRENCIES constants, if it is flagged as suspicious,
            that transaction is appended to the suspicious_transactions list
        
        Args:
            transaction (dict): a given transaction dictionary that contains the relevant data of the amount of the transaction and its currency
            
        Returns: None
        
        Raises: None
        """
        
        #takes the relevant info from the transaction and saves it to local variables
        amount = float(transaction["Amount"])
        currency = transaction["Currency"]
        
        #flags a transaction as suspicious(thus saving it to suspicious transactions)
        if amount > self.LARGE_TRANSACTION_THRESHOLD \
            or currency in self.UNCOMMON_CURRENCIES:
            self.__suspicious_transactions.append(transaction)
            self.logger.warning(f"Suspicious transaction: {transaction}")

    def update_transaction_statistics(self, transaction: dict) -> None:
        """
        updates the transaction statistics by reading the transaction type and amount and updating the statistics grouped by their transaction type
        
        Args: transaction (dict): a given transaction dictionary that contains the relevant data of the transaction type and it's amount
        
        Returns: None
        
        Raises: None
        """
        
        #takes the relevant info from the transaction and saves it to local variables
        transaction_type = transaction["Transaction type"]
        amount = float(transaction["Amount"])

        #creates a new transaction type under transaction_statistics if it has not been previously created
        if transaction_type not in self.__transaction_statistics:
            self.__transaction_statistics[transaction_type] = {
                "total_amount": 0,
                "transaction_count": 0
            }

        #updates the transaction statistics by grouping them by transaction type and saving the amount and how many transactions have been made of that type
        self.__transaction_statistics[transaction_type]["total_amount"] += amount
        self.__transaction_statistics[transaction_type]["transaction_count"] += 1
        
        self.logger.info(f"Updated transaction statistics for: {transaction_type}")

    def get_average_transaction_amount(self, transaction_type: str) -> float:
        """
        calculates the average transaction amount using the data from the transaction statistics method
        
        Args:
            transaction_type (str): takes a given transaction type and calculates the average transaction amount for that type
            
        Returns:
            float: calculates the average transaction amount for a given transaction type and returns it
                returns 0 if there were no transactions of that type
        """
        
        #takes the relevant info from the transaction_statistics and saves it to local variables
        total_amount = self.__transaction_statistics[transaction_type]["total_amount"]
        transaction_count = self.__transaction_statistics[transaction_type]["transaction_count"]
    
        return 0 if transaction_count == 0 else total_amount / transaction_count

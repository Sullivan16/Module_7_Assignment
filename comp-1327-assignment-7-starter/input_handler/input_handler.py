"""Module that handles reading input data from a file
"""

__author__ = "Sullivan Lavoie"
__version__ = "1.0.0"

import csv
import json
from os import path

class InputHandler:
    """Class to handle input files and provide methods to read and process them.
    """

    def __init__(self, file_path: str):
        """Initialize the InputHandler with the path to the input file.

        Args:
            file_path (str): The path to the input file.
        """
        self.__file_path = file_path    # Store the file path

    @property
    def file_path(self) -> str:
        """Get the path of the input file.

        Returns:
            str: The path of the input file.
        """
        return self.__file_path     # Return the stored file path

    def get_file_format(self) -> str:
        """Get the format of the input file based on its extension.

        Returns:
            str: The file format (e.g., 'csv', 'json').
        """
        return self.__file_path.split(".")[-1]     # Extract and return the file extension

    def read_input_data(self) -> list:
        """Read the input data from the file.

        This method reads the input file based on its format (CSV or JSON) and returns the data as a list of dictionaries.

        Returns:
            list: The data read from the file, where each item is a dictionary representing a row of data.

        
        """
        transactions = []    # Initialize an empty list to store transactions
        file_format = self.get_file_format()   # Get the file format based on the file extension
        
        if file_format == "csv":
            transactions =  self.read_csv_data()    # Read data from CSV file
        elif file_format == "json":
            transactions = self.read_json_data()     # Read data from JSON file
        return transactions     # Return the list of transactions

    def read_csv_data(self) -> list:
        """Read the input data from the file.

        This method reads the input file based on its format (CSV or JSON) and returns the data as a list of dictionaries.

        Returns:
            list: The data read from the file, where each item is a dictionary representing a row of data.

        Raises:
            
            FileNotFoundError: If the file does not exist.
        """
        if not path.isfile(self.__file_path):
            raise FileNotFoundError(f"File: {self.__file_path} does not exist.")      # Check if the file exists

        transactions = []    # Initialize an empty list to store transactions

        
          # Open the CSV file and read its contents
        with open(self.__file_path, "r") as input_file:
            reader = csv.DictReader(input_file)     # Create a CSV reader object
            for row in reader:
                transactions.append(row)     # Append each row to the transactions list
            
        return transactions      # Return the list of transactions
            
    def read_json_data(self) -> list:
        """Read the input data from a JSON file.

    This method reads the input file assuming it is in JSON 
    format and returns the data as a list of dictionaries.

    Returns:
        list: The data read from the JSON file, where 
        each item is a dictionary representing a data entry.

    Raises:
        FileNotFoundError: If the file does not exist.
        
        """
        # Research the json.load function so that you 
        # understand the format of the data once it is
        # placed into input_data

          # Check if the file exists
        if not path.isfile(self.__file_path):
            raise FileNotFoundError(f"File: {self.__file_path} does not exist.")
        # Open the JSON file and read its contents
        with open(self.__file_path, "r") as input_file:
            transactions = json.load(input_file)

        return transactions     # Return the list of transactions

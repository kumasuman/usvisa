import os
import sys

import numpy as np
import dill  # Used for serializing and deserializing Python objects
import yaml  # For reading and writing YAML files
from pandas import DataFrame  # For handling pandas DataFrame operations

from us_visa.exception import USvisaException  # Custom exception class for handling errors
from us_visa.logger import logging  # Custom logging for tracking information


# Function to read data from a YAML file and return it as a dictionary
def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns the data as a dictionary.
    
    :param file_path: Path to the YAML file
    :return: Parsed YAML data as a dictionary
    """
    try:
        # Open the file in binary mode and read the YAML content
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)  # Load YAML safely
    except Exception as e:
        # Raise a custom exception if an error occurs
        raise USvisaException(e, sys) from e


# Function to write content to a YAML file
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes content to a YAML file.
    
    :param file_path: Path to save the YAML file
    :param content: The content to write into the YAML file
    :param replace: If True, replace the existing file
    """
    try:
        # If replace is True and file exists, delete the existing file
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        # Create directories if they do not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Open the file in write mode and dump the content into the file as YAML
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        # Raise a custom exception if an error occurs
        raise USvisaException(e, sys) from e


# Function to load a serialized object using dill
def load_object(file_path: str) -> object:
    logging.info("Entered the load_object method of utils")  # Log entry into method

    try:
        # Open the file in binary mode and load the serialized object
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)  # Use dill to deserialize the object

        logging.info("Exited the load_object method of utils")  # Log exit from method

        return obj  # Return the deserialized object
    except Exception as e:
        # Raise a custom exception if an error occurs
        raise USvisaException(e, sys) from e


# Function to save a numpy array to a file
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to a specified file.
    
    :param file_path: The path where the numpy array will be saved
    :param array: The numpy array data to save
    """
    try:
        # Create the directory if it does not exist
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        # Open the file in binary write mode and save the numpy array
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        # Raise a custom exception if an error occurs
        raise USvisaException(e, sys) from e


# Function to load a numpy array from a file
def load_numpy_array_data(file_path: str) -> np.array:
    """
    Load numpy array data from a file.
    
    :param file_path: Path to the file containing the numpy array
    :return: Loaded numpy array data
    """
    try:
        # Open the file in binary read mode and load the numpy array
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        # Raise a custom exception if an error occurs
        raise USvisaException(e, sys) from e


# Function to save a Python object using dill
def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of utils")  # Log entry into method

    try:
        # Create directories if they do not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Open the file in binary write mode and save the object using dill
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Exited the save_object method of utils")  # Log exit from method
    except Exception as e:
        # Raise a custom exception if an error occurs
        raise USvisaException(e, sys) from e


# Function to drop specified columns from a pandas DataFrame
def drop_columns(df: DataFrame, cols: list) -> DataFrame:
    """
    Drops specified columns from a pandas DataFrame.
    
    :param df: The pandas DataFrame to modify
    :param cols: A list of column names to drop from the DataFrame
    :return: Modified DataFrame with the specified columns removed
    """
    logging.info("Entered drop_columns method of utils")  # Log entry into method

    try:
        # Drop the specified columns from the DataFrame
        df = df.drop(columns=cols, axis=1)

        logging.info("Exited the drop_columns method of utils")  # Log exit from method

        return df  # Return the modified DataFrame
    except Exception as e:
        # Raise a custom exception if an error occurs
        raise USvisaException(e, sys) from e

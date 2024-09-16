import os
import sys

# Function to capture and format detailed error information
def error_message_detail(error, error_detail: sys):
    """
    This function captures detailed information about an error, including:
    - The file where the error occurred
    - The line number where the error happened
    - The error message itself
    
    :param error: The error object that was raised
    :param error_detail: The sys module used to get error details
    :return: A formatted string with the error details
    """
    
    # Extract exception information using sys.exc_info()
    _, _, exc_tb = error_detail.exc_info()  # exc_tb is the traceback object
    
    # Get the filename where the error occurred
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Construct a detailed error message with file name, line number, and the error message
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)  # tb_lineno gets the line number where the error occurred
    )

    return error_message  # Return the formatted error message

# Custom exception class to handle US visa-related exceptions
class USvisaException(Exception):
    def __init__(self, error_message, error_detail):
        """
        Initialize the custom exception by providing a detailed error message.
        This class inherits from the built-in Exception class.
        
        :param error_message: A custom error message
        :param error_detail: The sys module to get error details
        """
        super().__init__(error_message)  # Call the base class constructor with the error message
        
        # Format and store the detailed error message using the error_message_detail function
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    # Override the __str__ method to return the custom error message
    def __str__(self):
        return self.error_message  # Return the detailed error message when the exception is printed

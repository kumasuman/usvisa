import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

# Importing custom exception, logging, and data access utilities
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import USvisaData

# Class responsible for the process of data ingestion
class DataIngestion:
    
    # Constructor method to initialize the class with a configuration object
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        :param data_ingestion_config: Configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config  # Storing configuration
        except Exception as e:
            # Handling exceptions by logging and raising a custom exception
            raise USvisaException(e, sys)
    
    # Method to export data from MongoDB to a CSV file and return the data as a pandas DataFrame
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from MongoDB to a CSV file
        
        Output      :   Data is returned as a DataFrame and saved as a CSV file
        On Failure  :   Logs the error and raises a custom exception
        """
        try:
            logging.info(f"Exporting data from MongoDB")
            
            # Fetching the data from MongoDB using a custom data access class
            usvisa_data = USvisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(collection_name=
                                                                   self.data_ingestion_config.collection_name)
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            
            # Saving the data to the specified file path
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)  # Creating directory if it doesn't exist
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            
            # Writing the DataFrame to a CSV file
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise USvisaException(e, sys)  # Raising a custom exception if any error occurs

    # Method to split the data into training and testing sets and save them as CSV files
    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train and test sets based on a split ratio
        
        Output      :   Train and test sets are saved as CSV files
        On Failure  :   Logs the error and raises a custom exception
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            # Splitting the data into training and testing sets
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train-test split on the dataframe")
            
            # Creating directories for saving the train and test files if they don't exist
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            # Saving the train and test sets as CSV files
            logging.info(f"Exporting train and test data to file paths.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Exported train and test data successfully.")
        except Exception as e:
            raise USvisaException(e, sys)  # Handling and raising any exceptions

    # Main method that orchestrates the data ingestion process
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion process by:
                        - Exporting data from MongoDB
                        - Splitting it into train and test sets
                        
        Output      :   Returns the file paths of the train and test datasets as an artifact
        On Failure  :   Logs the error and raises a custom exception
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            # Step 1: Exporting data from MongoDB into a DataFrame
            dataframe = self.export_data_into_feature_store()
            logging.info("Data successfully exported from MongoDB")

            # Step 2: Splitting the DataFrame into training and testing datasets
            self.split_data_as_train_test(dataframe)
            logging.info("Train-test split completed")

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")

            # Creating a DataIngestionArtifact object to store file paths of train and test data
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            
            logging.info(f"Data ingestion artifact created: {data_ingestion_artifact}")
            return data_ingestion_artifact  # Returning the artifact
        except Exception as e:
            raise USvisaException(e, sys)  # Handling any exceptions that occur

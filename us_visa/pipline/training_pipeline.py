import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging

# Importing all pipeline components responsible for different stages of the ML pipeline
from us_visa.components.data_ingestion import DataIngestion

from us_visa.components.data_validation import DataValidation

# Importing configuration and artifact classes used to manage pipeline processes
from us_visa.entity.config_entity import (DataIngestionConfig, DataValidationConfig)
                                         

from us_visa.entity.artifact_entity import  (DataIngestionArtifact, DataValidationArtifact)



# This class orchestrates the entire machine learning training pipeline by combining different components
class TrainPipeline:
    
    def __init__(self):
        """
        Initializes the TrainPipeline class with necessary configuration objects for each pipeline stage.
        """
        # Configuration objects for each step of the pipeline
        self.data_ingestion_config = DataIngestionConfig()  # Data ingestion configuration
        
        self.data_validation_config = DataValidationConfig()

    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method starts the data ingestion component.
        It retrieves data from MongoDB, processes it, and returns an artifact containing train and test sets.
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from MongoDB")
            
            # Create an instance of the DataIngestion class and initiate data ingestion
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            logging.info("Got the train_set and test_set from MongoDB")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            
            # Returning data ingestion results (train and test set paths)
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e  # Raising a custom exception if an error occurs

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data validation component
        """
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config
                                             )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise USvisaException(e, sys) from e


    def run_pipeline(self) -> None:
        """
        This method orchestrates the entire pipeline by running each component in sequence:
        - Data Ingestion
        - Data Validation
        - Data Transformation
        - Model Training
        - Model Evaluation
        - Model Pushing (if the model is accepted)
        """
        try:
            # Step 1: Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            
        except Exception as e:
            raise USvisaException(e, sys)  # Handling any exceptions that occur in the pipeline

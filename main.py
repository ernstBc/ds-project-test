from src.ds_project import logger
from src.ds_project.pipeline.data_ingestion_step import DataIngestionComponent
from src.ds_project.pipeline.data_validation_step import DataValidationComponent
from src.ds_project.pipeline.data_transformation_step import DataTransformationPipeline
from src.ds_project.pipeline.model_training_step import ModelTrainingComponent
from src.ds_project.pipeline.model_validator_step import ModelValidatorPipeline

import argparse


def main():
    # Argument parsing
    argparser = argparse.ArgumentParser(description="Data Science Project Pipeline")
    argparser.add_argument("--model_type", type=str, default="LOGISTIC_REGRESSION", help="Type of model to train")
    
    # Data Ingestion Step
    try:
        logger.info("----------------Starting data ingestion process...-----------------")
        data_ingestion_component = DataIngestionComponent()
        data_ingestion_component.initialize_component()
        logger.info("----------------Data ingestion completed successfully.----------------")

    except Exception as e:
        logger.error(f"An error occurred in data ingestion process: {e}")
        raise e
    
    # Data Validation Step
    try:
        logger.info("----------------Starting data validation process...-----------------")
        data_validation_component = DataValidationComponent()
        validation_error = data_validation_component.initialize_component()
        if validation_error:
            logger.error("Data validation failed. Please check the logs for details.")
            raise Exception("Data validation failed.")
        else:
            logger.info("----------------Data validation completed successfully.----------------")
    except Exception as e:
        logger.error(f"An error occurred in data validation process: {e}")
        raise e

    # Data Tranformation Step
    try:
        logger.info("----------------Starting data tranformation process...-----------------")
        transformation_component=DataTransformationPipeline()
        transformation_component.initialize_component()
        logger.info("----------------Data tranformation completed successfully.----------------")

    except Exception as e:
        logger.error(f"An error occurred in data transformation process: {e}")
        raise e

    # Model Training Step
    try:
        logger.info("----------------Starting model training process...-----------------")
        model_training_component = ModelTrainingComponent()
        model_name, model_type = model_training_component.initialize_component()
        logger.info("----------------Model training completed successfully.----------------")

    except Exception as e:
        logger.error(f"An error occurred in model training process: {e}")
        raise e
    
    # Model Validation Step
    try:
        logger.info("----------------Starting model validation process...-----------------")
        model_validation_component = ModelValidatorPipeline()
        model_validation_component.initialize_component(model_name=model_name, model_type=model_type)
        logger.info("----------------Model validation completed successfully.----------------")

    except Exception as e:
        logger.error(f"An error in model validation process: {e}")
        raise e

if __name__ == "__main__":
    main()

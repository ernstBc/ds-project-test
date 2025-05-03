from src.ds_project import logger
from src.ds_project.pipeline.data_ingestion_step import DataIngestionComponent
from src.ds_project.pipeline.data_validation_step import DataValidationComponent
from src.ds_project.pipeline.data_transformation_step import DataTransformationPipeline


if __name__ == "__main__":
    try:
        logger.info("----------------Starting data ingestion process...-----------------")
        data_ingestion_component = DataIngestionComponent()
        data_ingestion_component.initialize_component()
        logger.info("----------------Data ingestion completed successfully.----------------")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
    
    
    try:
        logger.info("----------------Starting data validation process...-----------------")
        data_validation_component = DataValidationComponent()
        validation_error = data_validation_component.initialize_component()
        if validation_error:
            logger.error("Data validation failed. Please check the logs for details.")
        else:
            logger.info("----------------Data validation completed successfully.----------------")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
    

    # Data Tranformation Step
    try:
        logger.info("----------------Starting data tranformation process...-----------------")
        transformation_component=DataTransformationPipeline()
        transformation_component.initialize_component()
        logger.info("----------------Data tranformation completed successfully.----------------")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e

    


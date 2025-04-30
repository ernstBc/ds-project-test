from src.ds_project import logger
from src.ds_project.pipeline.data_ingestion_step import DataIngestionComponent


if __name__ == "__main__":
    try:
        logger.info("----------------Starting data ingestion process...-----------------")
        data_ingestion_component = DataIngestionComponent()
        data_ingestion_component.initialize_component()
        logger.info("----------------Data ingestion completed successfully.----------------")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
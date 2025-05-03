from src.ds_project.components.data_ingestion import DataIngestion
from src.ds_project.config.config import ConfigurationManager
from src.ds_project import logger


class DataIngestionComponent:
    def __init__(self):
        pass
    
    
    def initialize_component(self):
        config_data_ingestion_manager=ConfigurationManager()
        data_ingestion_config=config_data_ingestion_manager.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_data()
        data_ingestion.setup_data()




if __name__ == "__main__":
    try:
        data_ingestion_component = DataIngestionComponent()
        data_ingestion_component.initialize_component()
        logger.info("Data ingestion completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred in data ingestion component: {e}")
        raise e
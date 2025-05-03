from src.ds_project.components.data_validation import DataValidation
from src.ds_project.config.config import ValidationConfigurationManager
from src.ds_project import logger


class DataValidationComponent:
    def __init__(self):
        pass
    
    
    def initialize_component(self):
        config_validation_manager=ValidationConfigurationManager()
        data_validation_config=config_validation_manager.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        validation_error = data_validation.validate_data_schema()
        return validation_error


if __name__ == "__main__":
    try:
        # Initialize the data validation component
        logger.info("Initializing data validation component...")
        data_validation_component = DataValidationComponent()
        data_validation_component.initialize_component()
        logger.info("Data validation completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
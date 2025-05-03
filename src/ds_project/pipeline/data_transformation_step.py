from src.ds_project.components.data_transformation import DataTransformation
from src.ds_project.config.config import DataTransformationManager
from src.ds_project import logger



class DataTransformationPipeline:
    def __init__(self):
        pass

    def initialize_component(self):
        try:
            logger.info("Initializing data tranformation component...")
            manager= DataTransformationManager()
            config = manager.create_data_transformation_config()
            transformer= DataTransformation(config=config)
            transformer.transform()
            logger.info("Data tranformation completed successfully.")
        except Exception as e:
            logger.error(f"An error occurred in data transformation component: {e}")
            raise e
    

if __name__=='__main__':
    data_transformer=DataTransformationPipeline()
    data_transformer.initialize_component()


from src.ds_project.components.data_transformation import DataTransformation
from src.ds_project.config.config import DataTransformationManager


class DataTransformationPipeline:
    def __init__(self):
        pass

    def initialize_component(self):
            manager= DataTransformationManager()
            config = manager.create_data_transformation_config()
            transformer= DataTransformation(config=config)
            transformer.transform()
    

if __name__=='__main__':
    data_transformer=DataTransformationPipeline()
    data_transformer.initialize_component()


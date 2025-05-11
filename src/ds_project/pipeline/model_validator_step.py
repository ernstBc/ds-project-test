from src.ds_project.components.model_validator import ModelValidator
from src.ds_project.config.config import ModelValidatorManager


class ModelValidatorPipeline:
    def __init__(self):
        pass

    def initialize_component(self, model_name:str, model_type:str):

        config_manager=ModelValidatorManager()
        config=config_manager.get_model_validator_config(model_name=model_name, model_type=model_type)

        validator_component=ModelValidator(config)
        validator_component.validate_model()

        
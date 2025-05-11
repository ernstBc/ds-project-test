from src.ds_project.config.config import ModelTrainingManager
from src.ds_project.components.model_training import ModelTrainer



class ModelTrainingComponent:
    def __init__(self):
        pass


    def initialize_component(self):
            config_training = ModelTrainingManager()
            config = config_training.get_model_training_config()
            model_trainer = ModelTrainer(config)
            model_name, model_type = model_trainer.train_model()

            return model_name, model_type
        
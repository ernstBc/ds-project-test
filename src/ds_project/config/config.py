import os
from src.ds_project.utils.utils import read_yaml, create_directories
from src.ds_project import logger
from pathlib import Path
from datetime import datetime
from src.ds_project.entity.entity_config import (DataIngestionConfig, 
                                                 DataValidationConfig, 
                                                 DataTransformationConfig,
                                                 ModelTrainingConfig,
                                                 ModelValidatorConfig,
                                                 ExplainerConfig)
from src.ds_project.constants import (CONFIG_FILE_PATH, 
                                      PARAMS_FILE_PATH, 
                                      SCHEMA_FILE_PATH,)


class ConfigurationManager:
    def __init__(self, 
                 config_path=CONFIG_FILE_PATH, 
                 params_path = PARAMS_FILE_PATH, 
                 schema_path = SCHEMA_FILE_PATH):
        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)
        self.schema = read_yaml(schema_path)
        
        # Create artifact directories if they don't exist
        if not Path(self.config['artifacts_dir']).exists():
            create_directories([self.config['artifacts_dir']])
            logger.info(f"Created artifacts directory at {self.config['artifacts_dir']}")
        else:
            logger.info(f"Artifacts directory already exists at {self.config['artifacts_dir']}")


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config= self.config['data_ingestion']
        create_directories([config['directory'], config['raw_data_path'], config['train_data_path'], config['test_data_path']], True)

        data_ingestion_config = DataIngestionConfig(
            directory_path= Path(config['directory']),
            source_url= config['source_url'],
            local_data_file= Path(config['local_data_file']),
            raw_data_path= Path(config['raw_data_path']),
            train_data_path= Path(config['train_data_path']),
            test_data_path= Path(config['test_data_path'])
        )
        return data_ingestion_config
    

class ValidationConfigurationManager:
    def __init__(self,
                 config_filepath = CONFIG_FILE_PATH,
                 schema_filepath = SCHEMA_FILE_PATH,
                 ):
        self.config = read_yaml(config_filepath)
        self.schema = read_yaml(schema_filepath)
    
    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Get Data Validation Configuration
        """
        
        data_validation_config = DataValidationConfig(
            validation_directory=self.config['data_validation']['directory'],
            data_path=self.config['data_validation']['local_csv_file'],
            STATUS_FILE=self.config['data_validation']['status'],
            schema_file=self.schema
        )

        return data_validation_config
    


class DataTransformationManager:
    def __init__(self, config_path: str = CONFIG_FILE_PATH, params_path: str = PARAMS_FILE_PATH) -> DataTransformationConfig:
        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)


    def create_data_transformation_config(self) -> DataTransformationConfig:
        config = DataTransformationConfig(
            data_dir=self.config['data_ingestion']['local_data_file'],
            training_csv_dir=self.config['data_transformation']['training_csv_dir'],
            testing_csv_dir=self.config['data_transformation']['testing_csv_dir'],
            preprocessor_dir=self.config['data_transformation']['preprocessor_file_path'],
            params=self.params['transform_data']
        )
        create_directories([self.config['data_transformation']['directory']])
        create_directories([self.config['data_transformation']['transformation_artifacts']])
        
        return config
    

class ModelTrainingManager:
    def __init__(self, 
                 config_path: str=CONFIG_FILE_PATH, 
                 params_file_path: str = PARAMS_FILE_PATH):

        self.config = read_yaml(config_path)
        self.params = read_yaml(params_file_path)
        self.model_type = self.params.training.DEFAULT_MODEL

    def get_model_training_config(self) -> ModelTrainingConfig:

        config= ModelTrainingConfig(
            model_name=datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
            model_type=self.model_type,
            model_dir=Path(self.config['model_trainer']['directory']),
            training_data_path=Path(self.config['model_trainer']['training_csv_dir']),
            test_data_path=Path(self.config['model_trainer']['testing_csv_dir']),
            params=self.params
        )

        create_directories([self.config['model_trainer']['directory']])

        return config
    

class ModelValidatorManager:
    def __init__(self,
                 config_path: str = CONFIG_FILE_PATH,
                 params_path: str = PARAMS_FILE_PATH):
        
        self.config= read_yaml(config_path)
        self.params = read_yaml(params_path)

        create_directories([self.config.model_validator['directory'], 
                            self.config.model_validator['best_model_path'],
                            self.config.model_validator['best_model_artifacts_path']])
        
    def get_model_validator_config(self, model_name:str, model_type:str):
        model_path = os.path.join(self.config.model_trainer['directory'], model_name)
        config=ModelValidatorConfig(
            model_path=Path(model_path),
            model_name=model_name,
            model_type=model_type,
            test_data_path=self.config.model_trainer['testing_csv_dir'],
            best_model_path=self.config.model_validator['best_model_path'],
            best_model_artifacts=self.config.model_validator['best_model_artifacts_path'],
            model_registry_path=self.config.model_validator['model_registry'],
            params=self.params
        )

        return config
    

class ExplainerManager:
    def __init__(self,
                 config_path = CONFIG_FILE_PATH,
                 params_path=PARAMS_FILE_PATH
                 ):
        self.config=read_yaml(config_path)
        self.params = read_yaml(params_path)


        create_directories([self.config.explainer.directory])


    def get_explainer_config(self):
        config = ExplainerConfig(
            explainer_path=Path(self.config.explainer['explainer_path']),
            model_type=self.params.training['DEFAULT_MODEL'],
            best_model_path=Path(self.config.serving['serving_model'])
        )

        return config
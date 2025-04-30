
from src.ds_project.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.ds_project.utils.utils import read_yaml, create_directories
from src.ds_project import logger
from urllib.request import urlretrieve
from pathlib import Path
from src.ds_project.entity.entity_config import DataIngestionConfig
import shutil


class ConfigurationManager:
    def __init__(self, 
                 config_path=CONFIG_FILE_PATH, 
                 params_path = PARAMS_FILE_PATH, 
                 schema_path = SCHEMA_FILE_PATH):
        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)
        self.schema = read_yaml(schema_path)
        print(self.config)
        print(self.config['artifacts_dir'])
        
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
    
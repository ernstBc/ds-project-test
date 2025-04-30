from src.ds_project import logger
from src.ds_project.config.config import DataIngestionConfig
from urllib.request import urlretrieve
import os
import zipfile
import shutil


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    def download_data(self):
        if not os.path.exists(self.config.local_data_file):
            logger.info(f"Downloading data from {self.config.source_url} to {self.config.local_data_file}")
            filename, headers = urlretrieve(url=self.config.source_url, 
                                            filename=self.config.local_data_file)
            logger.info(f"Data downloaded to {self.config.local_data_file}")
        else:
            logger.info(f"Data already exists at {self.config.local_data_file}. Skipping download.")
    

    def extract_data(self):
        with zipfile.ZipFile(self.config.raw_data_file, 'r') as zip_ref:
            zip_ref.extractall(self.config.raw_data_path)
        logger.info(f"Data extracted to {self.config.raw_data_path}")

    def setup_data(self):
        # move the data to the raw data path
        if not self.config.local_data_file in os.listdir(self.config.raw_data_path):
            shutil.move(self.config.local_data_file, self.config.raw_data_path)
            logger.info(f'Data moved to {self.config.raw_data_path}')
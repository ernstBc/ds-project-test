from dataclasses import dataclass
import os
import streamlit as st
from pathlib import Path
from src.ds_project.constants import CONFIG_FILE_PATH
from src.ds_project.utils.utils import read_yaml
from src.app_utils.utils import get_uri_images_prediction

@dataclass
class AppConfig:
    registry_artifact_path: Path
    metrics_image_path: Path
    report_artifact_path: Path
    url_images: dict


class AppManager:
    def __init__(self, config_path = CONFIG_FILE_PATH):
        self.config = read_yaml(config_path)

    
    def get_app_config(self):
        images = [Path(os.path.join(self.config.model_validator['best_model_artifacts_path'], image)) 
                  for image in os.listdir(self.config.model_validator['best_model_artifacts_path'] )
                  if image.split('.')[1] =='png']
        report_path = [Path(os.path.join(self.config.model_validator['best_model_artifacts_path'], report))
                       for report in os.listdir(self.config.model_validator['best_model_artifacts_path'])
                       if report.split('.')[1] =='json']
        config = AppConfig(
            registry_artifact_path=Path(self.config.model_validator['model_registry']),
            metrics_image_path = images,
            report_artifact_path=report_path[0],
            url_images = get_uri_images_prediction()
        )

        return config
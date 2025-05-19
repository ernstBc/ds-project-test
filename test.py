import os 
from src.app_utils.config import AppManager


config = AppManager().get_app_config()

print(config)
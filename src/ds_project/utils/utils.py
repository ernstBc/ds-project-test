import os
import yaml
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from src.ds_project import logger
from typing import Any
from pathlib import Path
from box.exceptions import BoxValueError
import pickle


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.
    
    Args:
        path_to_yaml (str): Path to the YAML file.
        
    Returns:
        ConfigBox: Contents of the YAML file as a ConfigBox object.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {path_to_yaml} loaded successfully.")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"Error in YAML file structure: {path_to_yaml}. Please check the file.")
    except Exception as e:
        raise e
    


def create_directories(path_to_directories: list, verbose: bool = True) -> None:
    """
    Creates directories if they do not exist.
    
    Args:
        path_to_directories (list): List of directory paths to create.
        verbose (bool): If True, prints the status of directory creation.
    """
    for directory in path_to_directories:
        os.makedirs(directory, exist_ok=True)
        if verbose:
            logger.info(f"Directory {directory} created.")
        

@ensure_annotations
def save_json(path: Path, data: dict) -> None:
    """
    Saves a dictionary as a JSON file.
    
    Args:
        path (str): Path to save the JSON file.
        data (dict): Dictionary to save as JSON.
    """
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        logger.info(f"JSON file {path} saved successfully.")


@ensure_annotations
def load_json(path: Path) -> dict:
    """
    Loads a JSON file and returns its contents as a dictionary.
    
    Args:
        path (str): Path to the JSON file.
        
    Returns:
        dict: Contents of the JSON file.
    """
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        logger.info(f"JSON file {path} loaded successfully.")
        return data
    


def save_binary_data(path: Path, data: Any, as_pickle: bool) -> None:
    """
    Saves data as a binary file using joblib.
    
    Args:
        path (str): Path to save the binary file.
        data (Any): Data to save as binary.
        as_pickle(bool): Save as a pickle file
    """
    if as_pickle:
        with open(path, 'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
            logger.info(f"Binary file {path} saved successfully.")
    else:
        joblib.dump(data, path)
        logger.info(f"Binary file {path} saved successfully.")


@ensure_annotations
def load_binary_data(path: Path, is_pickle=True) -> Any:
    """
    Loads a binary file and returns its contents.
    
    Args:
        path (str): Path to the binary file.
        
    Returns:
        Any: Contents of the binary file.
    """
    if is_pickle:
        with open(path, 'rb') as file:
            data = pickle.load(file)
            logger.info(f"Binary file {path} loaded successfully.")
    # If not pickle, use joblib
    else:
        data = joblib.load(path)
        logger.info(f"Binary file {path} loaded successfully.")
    return data
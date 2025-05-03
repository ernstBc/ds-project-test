from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

@dataclass
class DataIngestionConfig:
    directory_path: Path
    source_url: str
    local_data_file: Path
    raw_data_path: Path
    train_data_path: Path
    test_data_path: Path


@dataclass
class DataValidationConfig:
    """
    Data Validation Configuration
    """
    validation_directory: Path
    data_path: Path
    STATUS_FILE: str
    schema_file: Dict


@dataclass
class DataTransformationConfig:
    """Data Transformation Configuration"""
    data_dir : Path
    training_csv_dir : Path
    testing_csv_dir : Path
    preprocessor_dir : Path
    params: Dict
    
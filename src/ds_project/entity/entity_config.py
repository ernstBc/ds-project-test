from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    directory_path: Path
    source_url: str
    local_data_file: Path
    raw_data_path: Path
    train_data_path: Path
    test_data_path: Path
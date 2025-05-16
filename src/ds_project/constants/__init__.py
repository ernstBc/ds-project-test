from pathlib import Path


CONFIG_FILE_PATH = Path("config/config.yaml")
CONFIG_TRAINING_FILE_PATH = Path("config/training_config.yaml")
PARAMS_FILE_PATH = Path("parameters.yaml")
SCHEMA_FILE_PATH = Path("schema.yaml")
DEFAULT_MODEL="LOGISTIC_REGRESSION"

DEFAULT_PARAMS_FILE_PATH = Path("default_parameters.yaml")
# model validator threshold
VALIDATOR_THRESHOLD=0.001
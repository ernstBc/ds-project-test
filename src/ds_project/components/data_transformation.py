from src.ds_project import logger
from src.ds_project.utils.utils import save_binary_data
from src.ds_project.entity.entity_config import DataTransformationConfig
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from typing import List, Dict, Any
from pathlib import Path


def save_data(data: pd.DataFrame, file_path: str) -> None:
    """
    Save the transformed data to a CSV file.
    data (Dataframe): A pandas Dataframe 
    file_path(str): The file directory where the data will be store 
                    (must include a .csv at tne end of the path name)
    """
    try:
        data.to_csv(file_path, index=False)
        logger.info(f"Data saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise e


def feature_selection(data: pd.DataFrame, features_to_drop: List[str]) -> pd.DataFrame:
    """
    Select relevant features from the dataset dropping irrelevant features.
    Arguments:
        data (Dataframe): A pandas DataFrame
        features_to_drop(list): A list with the name of the columns to drop

    Returns:
        A pandas DataFrame without the dropped columns
    """
    data = data.drop(columns=features_to_drop, errors='ignore')

    return data


def create_prepocessor(data: pd.DataFrame):
    """
    Creates a preprocessor object where the needed data transformations are applied.
    Arguments:
    Arguments:
        data(DataFrame): A pandas DataFrame
    Returns:
        preprocessor(ColumnTranform): A sklearn.ColumnTransform object
    """
    numeric_features = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = data.select_dtypes(include=['object']).columns.tolist()


    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    preprocessor.fit(data)
    logger.info("Preprocessor created successfully.")
    return preprocessor


class DataTransformation:
    def __init__(self, config: DataTransformationConfig) -> None:
        self.config = config

    def load_data(self) -> pd.DataFrame:
        """Load data from the specified directory."""
        try:
            data = pd.read_csv(self.config.data_dir)
            logger.info("Data loaded successfully.")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise e
    

    def transform(self) -> None:
        """Transform data by applying preprocessing steps."""
        data = self.load_data()
        try:
            # Feature selection
            data = feature_selection(data, features_to_drop=self.config.params['DROPPED_COLUMNS'])

            # Split data into training and testing sets
            training_data, testing_data = train_test_split(data, 
                                                           test_size=self.config.params['TEST_SIZE'],
                                                           random_state=self.config.params['RANDOM_SEED'])
            logger.info("Data split into training and testing sets.")
            logger.info(f"Training data shape: {training_data.shape}")
            logger.info(f"Testing data shape: {testing_data.shape}")

            # Create preprocessor
            preprocessor = create_prepocessor(training_data.drop(columns=['Survived']))

            # Transform data using the preprocessor
            transformed_training = preprocessor.transform(training_data.drop(columns=['Survived']))
            transformed_training = pd.DataFrame(transformed_training, columns=preprocessor.get_feature_names_out())
            transformed_training['Survived'] = training_data['Survived'].values

            transformed_testing = preprocessor.transform(testing_data.drop(columns=['Survived']))
            transformed_testing = pd.DataFrame(transformed_testing, columns=preprocessor.get_feature_names_out())
            transformed_testing['Survived'] = testing_data['Survived'].values

            logger.info("Data transformation completed successfully.")

            # Save transformed data
            save_data(transformed_training, self.config.training_csv_dir)
            save_data(transformed_testing, self.config.testing_csv_dir)

            # Save preprocessor
            save_binary_data(Path(self.config.preprocessor_dir), preprocessor, as_pickle=True)

        except Exception as e:
            logger.error(f"Error during data transformation: {e}")
            raise e
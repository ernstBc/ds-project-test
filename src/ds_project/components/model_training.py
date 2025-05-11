
import os
import pandas as pd
import mlflow
from mlflow import log_params, log_metrics, log_text
from src.ds_project import logger
from src.ds_project.config.config import ModelTrainingConfig
from src.ds_project import logger
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, 
                             f1_score, 
                             precision_score, 
                             recall_score, 
                             confusion_matrix, 
                             classification_report
                             )


class ModelTrainer:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config

    def train_model(self):

        try:
            # load model usig ModelsConfig class
            model = ModelsConfig(self.config).get_model()

            # load transformed data
            training_data = pd.read_csv(self.config.training_data_path)
            test_data = pd.read_csv(self.config.test_data_path)

            # train model
            # get target column
            target_column = self.config.params.training.TARGET_COLUMN
            if target_column not in training_data.columns:
                raise ValueError(f"Target column '{target_column}' not found in training data.")
            
            X_train = training_data.drop(columns=[target_column])
            y_train = training_data[target_column]
            X_test = test_data.drop(columns=[target_column])
            y_test = test_data[target_column]

            # fit the model and register it with mlflow
            for algorithm_type, model_instance in model.items():
                with mlflow.start_run() as run:
                    logger.info(f"Training {algorithm_type}...")
                    model_instance.fit(X_train, y_train)

                    logger.info(f"Model {algorithm_type} trained successfully.")


                    metrics = {
                        "accuracy": accuracy_score(y_test, model_instance.predict(X_test)),
                        "f1_score": f1_score(y_test, model_instance.predict(X_test), average='weighted'),
                        "precision": precision_score(y_test, model_instance.predict(X_test), average='weighted'),
                        "recall": recall_score(y_test, model_instance.predict(X_test), average='weighted')
                    }
                    report = classification_report(y_test, model_instance.predict(X_test), output_dict=True)
                    cm = confusion_matrix(y_test, model_instance.predict(X_test))


                    # Log parameters and metrics
                    log_params(self.config.params.training.MODELS[algorithm_type.upper()])
                    log_params({"model_name": algorithm_type})
                    log_metrics(metrics)
                    log_text(str(report), "classification_report.txt")
                    log_text(str(cm), "confusion_matrix.txt")

                    # Log the model
                    mlflow.sklearn.save_model(model_instance, 
                                              os.path.join(self.config.model_dir, self.config.model_name)
                                              )
            return self.config.model_name, self.config.model_type
        
        except Exception as e:
            logger.error(f"Error in training model: {e}")
            raise e


class ModelsConfig:
    def __init__(self, config: ModelTrainingConfig):
        """
        Initialize the ModelsConfig with the model training configuration.
        :param config: ModelTrainingConfig object containing model training parameters.
        :param model_type: Type of the model to be trained 
            (supported:
                'Logistic_Regression', 
                'Random_Forest',
                'Gradient_Boosting').
        """
        self.config = config

    def get_model(self):
        try:
            model_type = self.config.model_type
            params = self.config.params.training.MODELS

            if model_type == 'Logistic_Regression' or model_type == 'Logistic_Regression'.upper():
                model = {'Logistic_Regression': LogisticRegression(**params['LOGISTIC_REGRESSION'])}
            elif model_type == 'Random_Forest' or model_type == 'Random_Forest'.upper():
                model = {'Random_Forest': RandomForestClassifier(**params['RANDOM_FOREST'])}
            elif model_type == 'Gradient_Boosting' or model_type == 'Gradient_Boosting'.upper():
                model = {'Gradient_Boosting': GradientBoostingClassifier(**params['GRADIENT_BOOSTING'])}
            else:
                raise ValueError(f"Model type '{model_type}' is not supported. "
                                "Please choose from 'Logistic_Regression', 'Random_Forest', or 'Gradient_Boosting'.")
        except KeyError as e:
            logger.error(f"Key error: {e}. Please check the configuration file.")
            raise e
        
        return model
        
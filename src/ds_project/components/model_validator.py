import os
import pandas as pd
import matplotlib.pyplot as plt
from src.ds_project import logger
from src.ds_project.constants import VALIDATOR_THRESHOLD
from src.ds_project.config.config import ModelValidatorConfig
from pathlib import Path
from sklearn.metrics import (f1_score, 
                             accuracy_score,
                             recall_score,
                             precision_score,
                             classification_report, 
                             ConfusionMatrixDisplay, 
                             RocCurveDisplay,
                             PrecisionRecallDisplay)
from src.ds_project.utils.utils import (load_binary_data, 
                                        save_json,
                                        save_binary_data)


class ModelValidator:
    def __init__(self, config: ModelValidatorConfig, threshold:float = VALIDATOR_THRESHOLD):
        self.config=config
        self.threshold=threshold


    def validate_model(self):

        target_column = self.config.params.training['TARGET_COLUMN']
        model_dir = Path(os.path.join(self.config.model_path, 'model.pkl'))
        model = load_binary_data(model_dir)
        old_model_path=Path(os.path.join(self.config.best_model_path, 'model.pkl'))

        # load data
        data_test = pd.read_csv(self.config.test_data_path)
        x_test, y_test = data_test.drop([target_column], axis=1), data_test[target_column]

        if 'model.pkl' not in os.listdir(self.config.best_model_path):
            logger.info(f'Current model is the best model')
            
            # save the model as the best model
            save_binary_data(old_model_path, data=model, as_pickle=True)

            # calculate predictions and get metrics
            preds = model.predict(x_test)

            # log metrics and registry the model
            metrics=save_metrics_image(y_test, preds, self.config.best_model_artifacts)
            register_model(self.config.model_registry_path, 
                           model_name=self.config.model_name,
                           model_type=self.config.model_type,
                           metrics=metrics,
                           params=self.config.params.training.MODELS[self.config.model_type])

        else:
            old_model=load_binary_data(old_model_path)
            old_preds=old_model.predict(x_test)
            
            new_preds=model.predict(x_test)

            f1_old = f1_score(y_test, old_preds)
            f1_new = f1_score(y_test, new_preds)

            if (f1_new) > (f1_old + self.threshold):

                logger.info(f'Current model replace the lastest best model')
                # save the model as the best model
                save_binary_data(old_model_path,
                                data=model,
                                as_pickle=True)
                # log metrics and model
                metrics=save_metrics_image(y_test, preds, self.config.best_model_artifacts)
                register_model(self.config.model_registry_path, 
                                model_name=self.config.model_name,
                                model_type=self.config.model_type,
                                metrics=metrics,
                                params=self.config.params.training.MODELS[self.config.model_type])
            else:
                logger.info("Model doesn't beat the current best model")
            


def save_metrics_image(y_real: pd.Series, y_pred:pd.Series, path_dir:str):
    # report
    report = classification_report(y_real, y_pred, output_dict=True)
    report_path = Path(os.path.join(path_dir, 'report.json'))
    save_json(report_path, report)

    # plots 
    cm = ConfusionMatrixDisplay.from_predictions(y_real, y_pred)
    plt.title('Confusion Matrix')
    plt.savefig(os.path.join(path_dir, 'confusion_matrix.png'))    
    plt.clf()

    roc = RocCurveDisplay.from_predictions(y_real, y_pred)
    plt.title('ROC Curve')
    plt.savefig(os.path.join(path_dir,'roc_curve.png'))
    plt.clf()

    rp_curve=PrecisionRecallDisplay.from_predictions(y_real, y_pred)
    plt.title('Precision Recall Curve')
    plt.savefig(os.path.join(path_dir,'precision_recall.png'))    
    plt.clf()      

    accuracy = accuracy_score(y_real, y_pred)
    f1 = f1_score(y_real, y_pred)
    precision=precision_score(y_real, y_pred)
    recall = recall_score(y_real, y_pred)

    metrics = {
        'accuracy':accuracy,
        'f1':f1,
        "precision":precision,
        "recall":recall
    }
    return metrics



def register_model(model_registory_path:str, 
                   model_name:str, 
                   model_type:str,
                   metrics: dict, 
                   params:dict):
    
    format_text = f"""
    {'--'*150}
    Model: {model_name}
        Type: {model_type}
            Metrics:
                {metrics}
            Params: 
                {params}
    {'--'*150}

"""
    
    with open(model_registory_path, 'a') as file:
        file.write(format_text)

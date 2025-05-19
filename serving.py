import pandas as pd
from pathlib import Path
from src.ds_project import logger
from src.ds_project.utils.utils import load_binary_data, read_yaml
from src.ds_project.constants import CONFIG_FILE_PATH


class Serving:
    def __init__(self):
        config = read_yaml(CONFIG_FILE_PATH)

        self.preprocessor=load_binary_data(Path(config.data_transformation.preprocessor_file_path))
        self.model = load_binary_data(Path(config.serving.serving_model))
        self.explainer=load_binary_data(Path(config.explainer.explainer_path))


    def serve(self, data:dict, ):
        logger.info('serving operation: ')
        logger.info(f'logging data: {data}')

        data=pd.DataFrame(data)
        data_tranformed=self.preprocessor.transform(data)
        data_tranformed=pd.DataFrame(data_tranformed, columns=self.preprocessor.get_feature_names_out())

        prediction=self.model.predict(data_tranformed)
        logger.info(f'logging prediction: {prediction}')

        return prediction
    
    
    def serve_with_explaination(self, data:dict, batch:bool=False):
        logger.info('serving operation: ')
        data_original=data.copy()
        if isinstance(data, dict):
            data=pd.DataFrame(data)
            data=self.preprocessor.transform(data)
            data=pd.DataFrame(data, columns=self.preprocessor.get_feature_names_out())

        prediction=self.model.predict(data)
        explaination=self.explainer(data, check_additivity=False)

        if batch is False:
            logger.info(f'logging data: {data_original}')
            logger.info(f'logging prediction: {prediction}')

        return prediction, explaination



if __name__=='__main__':
    example = {
        'Pclass':[1],
        'Sex': ['male'],
        'Age': [20],
        'SibSp':[0],
        'Parch':[0],
        'Fare':[7.25],
        'Embarked':['Q']
    }

    server=Serving()
    pred = server.serve(example)
    print(pred)
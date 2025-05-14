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


    def serve(self, data:dict):
        logger.info('serving operation: ')
        logger.info(f'logging data: {data}')
        data=pd.DataFrame(data)
        data_tranformed=self.preprocessor.transform(data)
        data_tranformed=pd.DataFrame(data_tranformed, columns=self.preprocessor.get_feature_names_out())
        pred=self.model.predict(data_tranformed)
        logger.info(f'logging prediction: {pred}')

        return pred


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
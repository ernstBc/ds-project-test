import shap
from src.ds_project import logger
from src.ds_project.entity.entity_config import ExplainerConfig
from src.ds_project.utils.utils import save_binary_data, load_binary_data


class Explainer:
    def __init__(self,config: ExplainerConfig):
        self.config=config
        self.explainer = None

    def create_explainer(self, x_train, model=None):
        # create a Explainer Object
        x_train=x_train.sample(frac=0.2)

        explainer_config = ExplainerModel(self.config)
        explainer = explainer_config.get_explainer(x=x_train,model=model)
        
        #save explainer
        self.explainer=explainer
        logger.info('Model explainer created')
    
    def create_and_save_explainer(self, x):
        if self.explainer is None:
            self.create_explainer(x)
        
        save_binary_data(self.config.explainer_path, self.explainer, as_pickle=True)
        logger.info(f'Explainer saved at {self.config.explainer_path}')


class ExplainerModel:
    def __init__(self, config:ExplainerConfig):
        self.config=config

    def get_explainer(self,x, model=None):
        if model is None:
            model=load_binary_data(self.config.best_model_path)

        if self.config.model_type =='LOGISTIC_REGRESSION':
            explainer=shap.LinearExplainer(model, x)
        elif self.config.model_type == 'GRADIENT_BOOSTING':
            explainer=shap.TreeExplainer(model, x)
        else:
            explainer = shap.KernelExplainer(model.predict, x)
        
        return explainer
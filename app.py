import shap
import streamlit as st
import pandas as pd
from pathlib import Path
from serving import Serving
from src.app_utils.config import AppManager
from src.ds_project.utils.utils import (load_json, 
                                        update_yaml, 
                                        read_yaml, 
                                        reset_parameters)
from src.ds_project.constants import (PARAMS_FILE_PATH, 
                                      DEFAULT_PARAMS_FILE_PATH)
from src.app_utils.utils import (show_training_message, 
                                 to_categorical_prediction, 
                                 load_sample_data)

            

def init_session_states():
    st.session_state['explaination_button_pushed']=False
    st.session_state['show_logger_button_pushed']=False


# start session states
try:
    st.session_state['serving']=Serving()
except:
    show_training_message('Its needed to train a model before start using this app')

if 'sample_data' not in st.session_state:
    st.session_state['sample_data'] = load_sample_data(fraction=0.3)


app_config=AppManager().get_app_config()
# init states
if not 'explaination_button_pushed' in st.session_state:
    init_session_states()


params_project=read_yaml(PARAMS_FILE_PATH, as_config=False)
params_models=params_project['training']['MODELS']

# Init main Page
st.title('Prediction App')

with st.sidebar:
    st.write('Variables')
    pclass=st.selectbox('Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)', [1,2,3])
    age=st.select_slider('Age of the passenger in years.', options=list(range(0,100)))
    embarket=st.selectbox('Port of embarkation', options={"Southampton":'S', 
                                                          "Cherbourg":'C', 
                                                          "Queenstown":'Q'})
    sibsp=st.select_slider('Number of siblings or spouses aboard the Titanic', options=list(range(0,9)))
    sex=st.selectbox('Sex of the passenger', options=['female', 'male'])
    parch=st.select_slider('Number of parents or children aboard the Titanic.', options=list(range(0,7)))
    fare=st.number_input('Passenger fare.', min_value=0.0, max_value=550.0, step=0.1, format="%.2f")

    embarket = 'S' if embarket == 'Southampton' else ('C' if embarket == 'Cherbourg' else 'Q')

    if st.button('Predict', use_container_width=True):
        example = {
            'Pclass':[pclass],
            'Sex': [sex],
            'Age': [age],
            'SibSp':[sibsp],
            'Parch':[parch],
            'Fare':[fare],
            'Embarked':[embarket]
        }

        prediction=st.session_state['serving'].serve(example)
        st.session_state['prediction'] = to_categorical_prediction(prediction=prediction)
        st.session_state['data']=example
        init_session_states()



    st.write('')
    st.write('Training')
    with st.popover("Training Settings"):
        choice = st.radio("Pick one type of model to train", ['LOGISTIC_REGRESSION','GRADIENT_BOOSTING', 'RANDOM_FOREST'])
        params=pd.Series(params_models[choice])
        s = st.data_editor(params)

        if st.button('Apply Changes', use_container_width=True, type='primary'):
            
            params_models[choice] = s.to_dict()
            params_project['training']['DEFAULT_MODEL']=choice

            # update default params before training
            update_yaml(PARAMS_FILE_PATH, dict(params_project))

            # display a message to confirm starting a new training
            show_training_message('Do you want to train a new model? (this could take a few minutes)')
            
        if st.button('Reset Configuration', use_container_width=True, type="secondary"):
            reset_parameters(PARAMS_FILE_PATH, DEFAULT_PARAMS_FILE_PATH)
    

# diplay prediction results
if 'prediction' in st.session_state:
    st.subheader(st.session_state['prediction'])
    if st.session_state['prediction'] == 'Survived':
        st.markdown(f"![Alt Text]({app_config.url_images['positive_pred_image']})")
    else:
        st.markdown(f"![Alt Text]({app_config.url_images['negative_pred_image']})")



# model explainability
show_explaination_button=st.button('Explaine Prediction')
st.session_state['explaination_button_pushed'] = show_explaination_button
if st.session_state['explaination_button_pushed']:
    if st.session_state['data'] is None:
        st.write('Pos Nomas')
    else:
        explain_col1, explain_col2 = st.columns(2)
        with st.status('Computing explaination'):
            prediction, shap_values=st.session_state['serving'].serve_with_explaination(st.session_state['data'])
            _, shap_values_sample=st.session_state['serving'].serve_with_explaination(st.session_state['sample_data'], batch=True)
            ax= shap.plots.waterfall(shap_values[0])
            explain_col1.pyplot(ax, use_container_width=True, clear_figure=True)

            xa = shap.plots.beeswarm(shap_values_sample)
            explain_col2.pyplot(xa)


# Model Validation segment
st.subheader('Model Evaluation')
#individual metrics
# replace this path to a CONSTANT FILE PATH
metrics_best_model=load_json(app_config.report_artifact_path)
st.metric('Accuracy', round(metrics_best_model['accuracy'], 4), )


# plots
columns_images = st.columns(3)
list_images = app_config.metrics_image_path
for i, col in enumerate(columns_images):
    col.image(list_images[i])

st.write('')
col1,col2,col3=st.columns(3)
col1.metric('F1', round(metrics_best_model["macro avg"]["f1-score"], 4))
col2.metric('Precision', round(metrics_best_model["macro avg"]["precision"], 4))
col3.metric('Recall', round(metrics_best_model["macro avg"]["recall"], 4))
          


# show the model registry
show_model_history_button=st.button('Show models history')
st.session_state['show_logger_button_pushed'] = show_model_history_button
if st.session_state['show_logger_button_pushed']:
    with open(app_config.registry_artifact_path,'r') as file:
        text=file.read()
    st.text(text)
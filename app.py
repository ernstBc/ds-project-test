import os
import streamlit as st
import time
import pandas as pd
from pathlib import Path
from serving import Serving
from src.ds_project.utils.utils import load_json, update_yaml, read_yaml, reset_parameters
from src.ds_project.constants import PARAMS_FILE_PATH, DEFAULT_PARAMS_FILE_PATH
from main import main as train
from streamlit_js_eval import streamlit_js_eval


def do_something_slow():
    time.sleep(5)

def reset_page():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

@st.dialog("Warning")
def show_training_message(train_message:str):
    st.write(train_message)
    if st.button('Train', use_container_width=True, type='primary'):
        with st.status('Training'):
            train()
            reset_page()


st.title('Prediction App')

try:
    serving=Serving()
except:
    show_training_message('No model founded. To use the app its necessary to train a model')
    with st.status('Setting configurations'):
        time.sleep(5)
        reset_page()

params_project=read_yaml(PARAMS_FILE_PATH, as_config=False)
params_models=params_project['training']['MODELS']

# Init main Page


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

        prediction=serving.serve(example)

        if prediction == 0:
            st.session_state['prediction']='Died'
        elif prediction == 1:
            st.session_state['prediction']='Survived'
        else:
            st.session_state['prediction'] = None

        print('--------------------------------', prediction)
        print('---------------------------------', st.session_state['prediction'])
        #reset_page()

        


    st.write('')
    st.write('Training')
    with st.popover("Training Settings"):
        choice = st.radio("Pick one type of model to train", ['LOGISTIC_REGRESSION','GRADIENT_BOOSTING', 'RANDOM_FOREST'])
        params=pd.Series(params_models[choice])
        s = st.data_editor(params)

        if st.button('Apply Changes', use_container_width=True, type='primary'):
            
            params_models[choice] = s.to_dict()
            params_project['training']['DEFAULT_MODEL']=choice
            update_yaml(PARAMS_FILE_PATH, dict(params_project))
            show_training_message('Do you want to train a new model? (this could take a few minutes)')
            
        if st.button('Reset Configuration', use_container_width=True, type="secondary"):
            reset_parameters(PARAMS_FILE_PATH, DEFAULT_PARAMS_FILE_PATH)
    

# diplay prediction results
if 'prediction' in st.session_state:
    st.write(st.session_state['prediction'])
    if st.session_state['prediction'] == 'Survived':
        st.markdown("![Alt Text](https://images3.memedroid.com/images/UPLOADED528/6670df782ede4.webp)")
    else:
        st.markdown("![Alt Text](https://images7.memedroid.com/images/UPLOADED918/65b6ed14e4a83.webp)")
else:
    st.markdown("![Alt Text](https://i.pinimg.com/736x/86/4a/1c/864a1ce66d2b479317396950aaf03694.jpg)")



# model explainability
if st.button('Explaine Prediction'):
    st.write('Pos Nomas')


# Model Validation segment
st.subheader('Model Evaluation')
#individual metrics
# replace this path to a CONSTANT FILE PATH
metrics_best_model=load_json(Path('artifact/model_validator/best_model/artifacts/report.json'))
st.metric('Accuracy', round(metrics_best_model['accuracy'], 4), )


# plots
columns_images = st.columns(3)
list_images = [os.path.join(r'artifact\model_validator\best_model\artifacts', image_url) for image_url in os.listdir(r'artifact\model_validator\best_model\artifacts') if image_url.split('.')[1] == 'png']
for i, col in enumerate(columns_images):
    col.image(list_images[i])

st.write('')
col1,col2,col3=st.columns(3)
col1.metric('F1', round(metrics_best_model["macro avg"]["f1-score"], 4))
col2.metric('Precision', round(metrics_best_model["macro avg"]["precision"], 4))
col3.metric('Recall', round(metrics_best_model["macro avg"]["recall"], 4))
          
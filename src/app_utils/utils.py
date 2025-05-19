import streamlit as st
import time
import pandas as pd
from streamlit_js_eval import streamlit_js_eval
from main import main as train
from src.ds_project.utils.utils import read_yaml
from src.ds_project.constants import CONFIG_FILE_PATH


def to_categorical_prediction(prediction):
    """
    Convert numerical prediction to categorical
    
    """
    
    if prediction == 0:
        cat_pred='Died'
    else:
        cat_pred = 'Survived'

    return cat_pred


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
            time.sleep(5)
            reset_page()


def load_sample_data(fraction:float=0.1):
    directories=read_yaml(CONFIG_FILE_PATH)
    x_train_path=directories.data_transformation['testing_csv_dir']
    train_data=pd.read_csv(x_train_path)
    x_train = train_data.drop(['Survived'], axis=1)
    x_train = x_train.sample(frac=fraction)

    return x_train


def get_uri_images_prediction():
    images_uri= {
        'positive_pred_image':'https://images3.memedroid.com/images/UPLOADED528/6670df782ede4.webp',
        'negative_pred_image':'https://images7.memedroid.com/images/UPLOADED918/65b6ed14e4a83.webp'
    }

    return images_uri
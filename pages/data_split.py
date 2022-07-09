import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split

# Load Css file
def load_css(path):
    with open(path, mode='r') as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


# loading the css file 
load_css("style.css")

st.markdown("# Data Split")

for data_name in st.session_state:
    if 'train' in data_name:
        # Get the train dataset
        datasets = st.session_state[data_name]

        st.markdown(f"<h3 class='sub-title'>{data_name.capitalize()}</h3>", unsafe_allow_html=True)
        # Insert the target feature
        target = st.selectbox("Target(Response) variable(Feature)", options=datasets.columns)
        
        train_rows = st.number_input("Train split samples(Rows)", min_value=0.0, max_value=1.0, value=.75)
        valid_rows = st.number_input("Validation split samples(Rows)", min_value=0.0, max_value=1.0, value=.25)
        random_state = st.number_input("Random state", value=0)

        if st.button("Split"):
            X = datasets.drop(target, axis=1)
            y = datasets[target]
            train_X, valid_X, train_y,  valid_y = train_test_split(X, y, train_size=train_rows, test_size=valid_rows, random_state=random_state)

            # Add datasets to the session
            st.session_state['train_X'] = train_X
            st.session_state['valid_X'] = valid_X
            st.session_state['train_y'] = train_y
            st.session_state['valid_y'] = valid_y

            st.info(f"""
            Train_X:\n
    
            \tRows: {train_X.shape[0]}\n
            \tColumns:{train_X.shape[1]}\n
            Valid_X:\n
            \tRows: {valid_X.shape[0]}\n
            \tColumns:{valid_X.shape[1]}\n
            Train_y:\n
            \tRows: {train_y.shape[0]}\n
            valid_y:\n
            \tRows: {valid_y.shape[0]}\n
            """)

            st.write(st.session_state)

if 'train' not in st.session_state:
    st.write("""
    The csv file name must be train.csv in order to split the dataset
    into train and validation data
    """)






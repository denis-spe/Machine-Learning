import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split

from pages import load_data

def split_datasets(
    datasets: pd.DataFrame,
    target: str,
    train_size: float,
    test_size: float,
    random_state: int
):
    X = datasets[0][0].drop(target, axis=1)
    y = datasets[0][0][target]
    X_train, X_valid, train_y,  valid_y = train_test_split(X, y, train_size=train_size, test_size=test_size, random_state=random_state)
    return X_train, X_valid, train_y,  valid_y


def app():
    # Instance a list with tuple of dataset with it's name
    datasets = load_data.all_dataset
    
    st.markdown("""
    <h2 class='sub-title'>Data Split</h2>
    """, unsafe_allow_html=True)

    if len(datasets) != 0:
        for dataset, name in datasets:
            if "train" in name:
                st.markdown(f"<h3 class='sub-title'>{datasets[0][1].capitalize()}</h3>", unsafe_allow_html=True)
                # Insert the target feature
                target = st.selectbox("Target(Response) variable(Feature)", options=datasets[0][0].columns)
                
                train_rows = st.number_input("Train split samples(Rows)", min_value=0.0, max_value=1.0, value=.75)
                valid_rows = st.number_input("Validation split samples(Rows)", min_value=0.0, max_value=1.0, value=.25)
                random_state = st.number_input("Random state", value=0)

                if st.button("Split"):
                    X = datasets[0][0].drop(target, axis=1)
                    y = datasets[0][0][target]
                    train_X, valid_X, train_y,  valid_y = train_test_split(X, y, train_size=train_rows, test_size=valid_rows, random_state=random_state)

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
            else:
                st.write("""
                The csv file name must have train in it's name
                like train.csv or mtcars_train.csv
        """)
    else:
        st.write("Go Back To Dataset Load Page")

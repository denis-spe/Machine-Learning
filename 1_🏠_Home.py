# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
from typing import List

# Set the page main title
st.set_page_config(
    page_title="ML",
    layout='wide'
)

# Gathering Data
# Preparing that data
# Choosing a model
# Training 
# Evaluation
# Hyperparameter Tuning
# Predication

st.title("Machine learning")
st.sidebar.title("Machine learning")


# Load Css file
def load_css(path):
    with open(path, mode='r') as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def convert_dtype(data, dtypes: List = None):
    _columns = data.columns

    for column in _columns:
        if dtypes:
            for dtype in dtypes:
                if str(data[column].dtype).startswith('int'):
                    if dtype == 'int8':
                        data[column] = data[column].astype("int8")
                    if dtype == 'int16':
                        data[column] = data[column].astype("int16")
                    if dtype == 'int32':
                        data[column] = data[column].astype("int32")
                    if dtype == 'int64':
                        data[column] = data[column].astype("int64")

                if str(data[column].dtype).startswith('float'):
                    if dtype == 'float16':
                        data[column] = data[column].astype(np.float16)
                    if dtype == 'float32':
                        data[column] = data[column].astype(np.float32)
                    if dtype == 'float64':
                        data[column] = data[column].astype(np.float64)

    return data


def info(data):
    _columns = data.columns
    dtypes = [
        data[column].dtypes
        for column in _columns
    ]

    # Create a data frame.
    df = pd.DataFrame({
        'columns': _columns,
        'dtype': dtypes
    })

    df.set_index('columns')

    return df


# loading the css file 
load_css("style.css")

# Setting Screen layout
sidebar = st.sidebar
col1, col2 = st.columns(2)
col3 = st.columns(1)

sidebar.markdown("""
<h2 class='sub-title'>Files</h2>
""", unsafe_allow_html=True)

# Upload files -------------------------------------------
upload_file = sidebar.file_uploader("Please upload the csv file", accept_multiple_files=True)

select_dtype = sidebar.multiselect(
    'Change numeric precision',
    options=['int8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float32', 'float64'],
    help="Select one or two different numeric data type for the columns"
)

if upload_file:
    try:
        # ********* Data Descriptive Analysis **********
        with col1:
            df_1 = pd.read_csv(upload_file[0])
            # Convert the dtype.
            df_1 = convert_dtype(df_1, select_dtype)
            data_name_1 = upload_file[0].name.split('.')[0]

            st.markdown(f"<h3 class='sub-title'>{data_name_1.capitalize()}</h3>", unsafe_allow_html=True)
            # ****** Show the data shape *****
            shape = df_1.shape
            st.markdown(f"""
            **Shape: <br>{shape[0]}-rows**<br>**{shape[1]}-columns**
            """, unsafe_allow_html=True)

            # ***** show the DataFrame ******
            with st.expander("DataFrame"):
                rows = list(range(10, 110, 5))
                rows.append('all')
                n_row = st.selectbox(f'{data_name_1}_rows', options=rows)
                if n_row == 'all':
                    st.write(df_1)
                else:
                    st.write(df_1.head(n_row))

                # Set column as index
                columns = list(df_1.columns)
                columns.insert(0, None)
                set_index_col = st.selectbox('Set column as index', options=columns)
                if set_index_col:
                    df_1 = df_1.set_index(set_index_col)

            # Add dataset to the session 
            st.session_state[data_name_1] = df_1

            # Display all dataframe column names
            with st.expander("columns"):
                st.write(", ".join([col for col in df_1.columns]))

            # View the data description
            with st.expander('Data Information'):
                st.write(info(df_1))

            # View the data description
            with st.expander('Data Description'):
                description_type = st.radio(label="Description type", options=["continuous", "categorical"])
                if description_type == "continuous":
                    st.write(df_1.describe())
                if description_type == "categorical":
                    st.write(df_1.describe(exclude=["int", "float"]))

        if len(upload_file) == 2:
            df_2 = pd.read_csv(upload_file[1])
            # Convert the dtype.
            df_2 = convert_dtype(df_2, select_dtype)
            with col2:
                data_name_2 = upload_file[1].name.split('.')[0]
                st.markdown(f"<h3 class='sub-title'>{data_name_2.capitalize()}</h3>", unsafe_allow_html=True)

                # ****** Show the data shape *****
                shape = df_2.shape
                st.markdown(f"""
                **Shape: <br>{shape[0]}-rows**<br>**{shape[1]}-columns**
                """, unsafe_allow_html=True)

                # ***** show the DataFrame ******
                with st.expander("DataFrame"):
                    rows = list(range(10, 110, 5))
                    rows.append('all')
                    n_row = st.selectbox(f'{data_name_2}_rows', options=rows)
                    if n_row == 'all':
                        st.write(df_2)
                    else:
                        st.write(df_2.head(n_row))

                    # Set column as index
                    columns = list(df_2.columns)
                    columns.insert(0, None)

                    if set_index_col is not None:
                        try:
                            index = columns.index(set_index_col)
                        except ValueError:
                            index = 0
                    else:
                        index = 0

                    set_index_col = st.selectbox('Set column as index', options=columns, index=index)
                    if set_index_col:
                        df_2 = df_2.set_index(set_index_col)

                # Add Dataset in the session
                st.session_state[data_name_2] = df_2

                # Display all dataframe column names
                with st.expander("columns"):
                    st.write(", ".join([col for col in df_2.columns]))

                # View the data description
                with st.expander('Data Information'):
                    st.write(info(df_2))

                # View the data description
                with st.expander('Data Description'):
                    description_type = st.radio(label="Description type ", options=["continuous", "categorical"])
                    if description_type == "continuous":
                        st.write(df_2.describe())
                    if description_type == "categorical":
                        st.write(df_2.describe(exclude=["int", "float"]))

    except IndexError:
        st.error("Too many file have been insert")

else:
    st.markdown(
        """
            ## **Please Insert A Files**
            **Insert one or two csv files from the sidebar**
            
            """
    )
    st.image("add_file_image_s4qf.svg")

    st.write("")
    st.write("")
# Make a page title
sidebar.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
sidebar.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
st.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)

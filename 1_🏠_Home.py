# Import libraries
from types import NoneType
from matplotlib.pylab import noncentral_f
import streamlit as st
import numpy as np
import pandas as pd
from typing import List, Literal, Any, Tuple
from helper.dataclass import Dataclass
from helper.load_css import load_css

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


def info(data):
    _columns = data.columns
    dtypes = [
        data[column].dtypes
        for column in _columns
    ]

    # Create a data frame.
    df = pd.DataFrame({
        'columns': _columns,
        'data_type': dtypes
    })

    df.set_index('columns')

    return df


# loading the css file 
load_css("resources/styles/style.css")

# Setting Screen layout
sidebar = st.sidebar
col1, col2 = st.columns(2)
col3 = st.columns(1)

sidebar.markdown("""
<h2 class='sub-title'>Files</h2>
""", unsafe_allow_html=True)

# Upload files -------------------------------------------
upload_file = sidebar.file_uploader("Please upload the csv file", accept_multiple_files=True)


if upload_file:
    if len(upload_file) > 2:
        st.error('Too many file were uploaded', icon="🚨")
    else:
        try:
            # ********* Data Descriptive Analysis **********
            with col1:
                file = upload_file[0]
                df_1 = pd.read_csv(file)

                data_name_1 = file.name.split('.')[0]

                st.markdown(f"<h3 class='sub-title'>{data_name_1.capitalize()}</h3>", unsafe_allow_html=True)

                # ****** Show the data shape *****
                shape = df_1.shape
                st.markdown(f"""
                **Shape: <br>{shape[0]}-rows**<br>**{shape[1]}-columns**
                """, unsafe_allow_html=True)

                # ***** show the DataFrame ******
                with st.expander("DataFrame"):
                    rows = [*[str(val) for val in range(10, 110, 5)], "all"]
                    n_row = st.selectbox(f'{data_name_1}_rows', options=rows)
                    if n_row == 'all':
                        st.write(df_1)
                    else:
                        st.write(df_1.head(int(n_row if n_row is not None else 0)))

                    # Set column as index
                    columns = list(df_1.columns)
                    columns.insert(0, None)

                # Add dataset to the session 
                Dataclass.SESSION[file.name] = df_1

                # Display all data frame column names
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
                file = upload_file[1]
                df_2 = pd.read_csv(file)

                with col2:

                    data_name_2 = file.name.split('.')[0]
                    st.markdown(f"<h3 class='sub-title'>{data_name_2.capitalize()}</h3>", unsafe_allow_html=True)

                    # ****** Show the data shape *****
                    shape = df_2.shape
                    st.markdown(f"""
                    **Shape: <br>{shape[0]}-rows**<br>**{shape[1]}-columns**
                    """, unsafe_allow_html=True)

                    # ***** show the DataFrame ******
                    with st.expander("DataFrame"):
                        rows = [*[str(val) for val in range(10, 110, 5)], "all"]
                        n_row = st.selectbox(f'{data_name_2}_rows', options=rows)
                        if n_row == 'all':
                            st.write(df_2)
                        else:
                            st.write(df_2.head(int(n_row if n_row is not None else 0)))

                        # Set column as index
                        columns: List[str|None] = list(df_2.columns)
                        columns.insert(0, None)


                    # # Add Dataset in the session
                    st.session_state[file.name] = df_2

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
            
            # Switch to the data split page
            if st.button("Data split"):
                st.switch_page("pages/1_✃_Data_Split.py")

        except IndexError:
            st.error("Too many file have been insert")

else:
    st.markdown(
        """
            ## **Please Insert A Files**
            **Insert one or two csv files from the sidebar**
            
            """
    )
    st.image("resources/images/add_file_image_s4qf.svg")

    st.write("")
    st.write("")
# Make a page title
sidebar.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
sidebar.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
st.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)

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

st.title("Machine learing")
st.sidebar.title("Machine learing")

# Load Css file
def load_css(path):
    with open(path, mode='r') as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def convert_dtype(data, dtypes: List = None):
    columns = data.columns

    for column in columns:
        if dtypes:
            for dtype in dtypes:
                if str(data[column].dtype).startswith('int'):
                    if dtype == 'int8':
                        data[column] = data[column].astype(np.int8)
                    if dtype == 'int16':
                        data[column] = data[column].astype(np.int16)
                    if dtype == 'int32':
                        data[column] = data[column].astype(np.int32)
                    if dtype == 'int64':
                        data[column] = data[column].astype(np.int64)
                
                if str(data[column].dtype).startswith('float'):
                    if dtype == 'float16':
                        data[column] = data[column].astype(np.float16)
                    if dtype == 'float32':
                        data[column] = data[column].astype(np.float32)
                    if dtype == 'float64':
                        data[column] = data[column].astype(np.float64)

    
    return data


def info(data):
    columns = data.columns
    dtypes = [
        data[column].dtypes
        for column in columns
        ]
    
    # Create a data frame.
    df = pd.DataFrame({
        'columns': columns,
        'dtype': dtypes
    })

    df.set_index('columns')

    return df
            


# loading the css file 
load_css("style.css")


# Setting  Screen layout
asidebar = st.sidebar
col1, col2 = st.columns(2)
col3 = st.columns(1)

asidebar.markdown("""
<h2 class='sub-title'>Files</h2>
""", unsafe_allow_html=True)

# Upload files -------------------------------------------
upload_file = asidebar.file_uploader("Please upload the csv file", accept_multiple_files=True)

select_dtype = asidebar.multiselect(
    'Data type Selection', 
    options=['int8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float32', 'float64'])

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
                st.write(df_1.describe())

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
                st.session_state[data_name_2] =  df_2

                # Display all dataframe column names
                with st.expander("columns"):
                    st.write(", ".join([col for col in df_2.columns]))

                # View the data description
                with st.expander('Data Information'):
                    st.write(info(df_2))

                # View the data description
                with st.expander('Data Description'):
                    st.write(df_2.describe())
                    
    except IndexError:
        st.error("Too many file have been insert")

else:
    st.markdown(
            """
            ## **Please Insert A Files**
            **Insert one or two csv files from the sidebar**
            
            """
            )
    st.image("undraw_add_file_re_s4qf.svg")

    st.write("")
    st.write("")
# Make a page title
asidebar.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
asidebar.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
st.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)

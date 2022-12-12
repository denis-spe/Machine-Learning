# import libraries ------------------------------------
from matplotlib import pyplot as plt
from matplotlib.style import use
import numpy as np
import streamlit as st
import altair as alt
import pandas as pd
import seaborn as sns
import plotly.express as px

use('ggplot')

# Set the page main title .............
st.set_page_config(
    page_title="ML | Data Exploratory",
)

# Load Css file ...........
def load_css(path):
    with open(path, mode='r') as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

# loading the css file .............
load_css("style.css")

# Initialize the session ..............
session = st.session_state

# Make a page title ...............
st.markdown("# Data Exploratory")

# Initialize the sidebar ...................
SIDEBAR = st.sidebar
SIDEBAR.markdown("# Data Exploratory")

# Instantiate the session_state ........
session = st.session_state

if len(session) != 0:
    # Change the session to dictonary ......
    df_dict = dict(session)

    # Data names .....
    data_names = list(filter(
        lambda x: x in ["train", "test"], 
        df_dict.keys())
        )    
    # Data name selection .......
    data_selector = SIDEBAR.selectbox(
        'Datasets', 
        options=data_names,
        index=len(data_names) - 1
        )
    
    # Get the data from selected data name.....
    data = session[data_selector]

    # Data columns .....
    columns = list(data.columns)

    try:
        # Target name ....
        target_name = df_dict['target_name']
    except KeyError:
        pass

    # -------- Create sidebar tabs ------------
    relative_sidebar, categorical_sidebar, continuous_sidebar = SIDEBAR.tabs(tabs=[
        "ralative",
        "categorical",
        "continuous"
        ])

    # Relative sidebar ........
    with relative_sidebar:
        # Relative chart type.
        relative_chart = st.selectbox("Ralative charts", options=["scatter matrix", "heatmap"])

        # Mapping color.
        try:
            relative_map_color = st.selectbox("Map color", options=columns, index=columns.index(target_name))
        except ValueError:
            relative_map_color = st.selectbox("Map color", options=columns)


    # Categorical sidebar .......
    with categorical_sidebar:
        # Add input box to sidebar .
        cat_chart = st.selectbox("Charts", options=['Bar', 'Histogram', 'Line', 'Scatter'])

        if cat_chart == 'Bar':
            bar_type = st.selectbox('Bar Type', options=['Bar', 'Col Bar', 'Stacked Bar'])
    

    # -------- Create tabs ------------
    relative, categorical, continuous = st.tabs(tabs=[
        "ralative",
        "categorical",
        "continuous"
        ])
    
    # Relative .......
    with relative:
        # Make a copy from the data.
        data_copy = data.copy()
        if data_copy[relative_map_color].nunique() < 16:
            data_copy[relative_map_color] = data_copy[relative_map_color].astype("str")

        numeric_col = [
            col
            for col in data_copy.columns
            if data_copy[col].dtype != 'object'
        ]

        if relative_chart == "scatter matrix":
            scatter_mat = alt.Chart(data_copy).mark_circle().encode(
                        alt.X(alt.repeat("column"), type='quantitative'),
                        alt.Y(alt.repeat("row"), type='quantitative'),
                        color=relative_map_color,
                        tooltip=numeric_col + [target_name]
                        ).properties(
                            width=150,
                            height=150
                        ).repeat(
                            row=numeric_col,
                            column=numeric_col
                        ).interactive()
            
            st.altair_chart(scatter_mat)

        if relative_chart == 'heatmap':
            # Data correlation matrix.
            corr: pd.DataFrame = data_copy.corr()

            fig = px.imshow(corr, text_auto=True)
            st.plotly_chart(fig)

    

    SIDEBAR.write("")
    SIDEBAR.write("")
    # Make a page title
    SIDEBAR.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
    SIDEBAR.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)
    SIDEBAR.write('')

    
else:
    # Display this if there is no data found .......
    SIDEBAR.write("Data is missing from this session")
    st.write('**Insert Data First, To Explorer Yo\' Data**')
    st.image('visual_img.png', caption='No Data Was Found', width=300)

st.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
st.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)
st.write('')
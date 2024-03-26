# import libraries ------------------------------------
import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
from helper.charts import plots
from typing import Dict
from matplotlib.style import use
from helper.load_css import load_css
import time
from helper.data_type import separate_columns_by_threshold

use('ggplot')

# Set the page main title .............
st.set_page_config(
    page_title="ML | Data Exploratory",
)


def combine_data(session: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    # Get the target name
    _target_name = str(session["target_name"])

    # Combine train data with its target
    train: pd.DataFrame = session["train_X"]
    train[_target_name] = session["train_y"]

    # Combine validation data with its target
    valid: pd.DataFrame = session["valid_X"]
    valid[_target_name] = session["valid_y"]

    train = pd.concat([train, valid])

    return train


# loading the css file .............
load_css("resources/styles/style.css")

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
    # Change the session to dictionary ......
    df_dict = dict(session)

    # Data names .....
    data_names = list(filter(
        lambda x: x in ["train", "test"],
        df_dict.keys())
    )

    data_names.append("combined train valid data")
    # Data name selection .......
    data_selector = SIDEBAR.selectbox(
        'Datasets',
        options=data_names,
        index=len(data_names) - 1
    )

    if data_selector == "combined train valid data":
        data = combine_data(session)
    else:
        # Get the data from selected data name .....
        data = session[data_selector]

    # Data columns .....
    columns = list(data.columns)

    try:
        # Target name ....
        target_name = df_dict['target_name']
    except KeyError:
        pass

    # --------- Make a copy from the data. ------
    data_copy = data.copy()

    # Separate columns by threshold
    column_sep_threshold = SIDEBAR.slider("Column separate threshold", max_value=30, min_value=10)
    columns_dict = separate_columns_by_threshold(data_copy, column_sep_threshold)
    categorical_columns = columns_dict["categorical_columns"]
    continuous_columns = columns_dict["continuous_columns"]

    # -------- Create sidebar tabs ------------
    categorical_sidebar, continuous_sidebar, relative_sidebar = SIDEBAR.tabs(tabs=[
        "categorical",
        "continuous",
        "relative",
    ])

    # Relative sidebar ........
    with relative_sidebar:
        # Relative chart type.
        relative_chart = st.selectbox("Relative charts", options=["scatter matrix", "heatmap"])

        # Mapping color.
        try:
            relative_map_color = st.selectbox("color by", options=columns, index=columns.index(target_name))
        except ValueError:
            relative_map_color = st.selectbox("color by", options=columns)

    # Categorical sidebar .......
    with categorical_sidebar:
        # Add input box to the sidebar.
        cat_chart = st.selectbox("Charts", options=['Bar', 'Pie chart'])

        if cat_chart == 'Bar':
            bar_type = st.selectbox('Bar Type', options=[
                'Bar',
                'Highlighted Bar'
            ])

        if cat_chart == 'Pie chart':
            bar_type = st.selectbox('Pie chart Type', options=['Pie chart', 'Donut chart'])

    # -------- Create tabs ------------
    categorical, continuous, relative = st.tabs(tabs=[
        "categorical",
        "continuous",
        "relative"
    ])

    with categorical:
        if cat_chart == 'Bar':
            if bar_type == 'Bar':
                # x, y and color map inputs
                x = SIDEBAR.selectbox("X", options=categorical_columns, index=0)
                plots.bar_chart(data, x=x)

            if bar_type == 'Highlighted Bar':
                # x, y and color map inputs
                x = SIDEBAR.selectbox("X", options=continuous_columns, index=0)
                y = SIDEBAR.selectbox("y", options=continuous_columns, index=1)
                highlight = SIDEBAR.selectbox("highlight", options=["max", "min"], index=1)

                plots.highlighted_bar(
                    data,
                    x,
                    y,
                    highlight_type=highlight
                )

    # Relative .......
    with relative:
        if data_copy[relative_map_color].nunique() < 16:
            data_copy[relative_map_color] = data_copy[relative_map_color].astype(str)

        numeric_col = [
            col
            for col in data_copy.columns
            if data_copy[col].dtype != 'object'
        ]

        if relative_chart == "scatter matrix" and len(numeric_col) <= 10:
            with st.progress(value=1.0, text="Loading wait please"):
                scatter_mat = alt.Chart(data_copy[numeric_col]).mark_circle().encode(
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

                time.sleep(5)
    

        elif relative_chart == 'heatmap':
                with st.progress(value=1.0, text="Loading wait plesse"):

                    # Data correlation matrix.
                    corr: pd.DataFrame = data_copy.select_dtypes(exclude=["object"]).corr(numeric_only=False)
                    fig = px.imshow(corr, text_auto=True, width=900, height=800)
                    fig.update_layout(
                        title=("Correlation of %s" % (
                            data_selector 
                            if data_selector.endswith("data") 
                            else data_selector + " data")).title(),
                    )
                    st.plotly_chart(fig)

                    time.sleep(3)
        else:
            st.write("Too Many Column To Show Scatter Matrix")

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
    st.image('resources/images/visual_img.png', caption='No Data Was Found', width=300)

st.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
st.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)
st.write('')

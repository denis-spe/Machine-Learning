# import libraries ------------------------------------
import streamlit as st

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

    data = SIDEBAR.selectbox('Datasets', options=df_dict.keys())

    # Add input box to sidebar .......
    chart = SIDEBAR.selectbox("Graph Type", options=['Bar', 'Histogram', 'Line', 'Scatter'])

    if chart == 'Bar':
        bar_type = SIDEBAR.selectbox('Bar Type', options=['Bar', 'Col Bar', 'Stacked Bar', 'Correlation Bar'])

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
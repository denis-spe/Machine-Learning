# import libraries ------------------------------------
import streamlit as st

# Set the page main title
st.set_page_config(
    page_title="ML | Data Exploratory",
)

# Load Css file
def load_css(path):
    with open(path, mode='r') as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

# loading the css file 
load_css("style.css")

# Initialize the session
session = st.session_state

# Make a page title
st.markdown("# Data Exploratory")

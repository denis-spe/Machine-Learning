# Import libraries
import streamlit as st
import pandas as pd
from my_multipage import Pages
from pages import data_cleaning, data_split, load_data


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


# loading the css file 
load_css("style.css")


# Call pages 
load_dataset = load_data.load
data_spliter = data_split.app
clean_data = data_cleaning.app

# Initialize the Page instance
app = Pages(navigation_name='Machine learning steps')

# Register the pages
app.add_app("Load Dataset", load_dataset)
app.add_app("Data Split", data_spliter)
app.add_app("Data cleaning", clean_data)

app.run()


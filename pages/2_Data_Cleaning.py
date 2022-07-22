# import libraries ------------------------------------
import streamlit as st

# Set the page main title
st.set_page_config(
    page_title="ML | Data Cleaning",
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
st.markdown("# Data Cleaning")

# Seperate the page into two
col3 = st.columns(2)
col1, col2, col4 = st.columns(3)

if "train_X" in session:
    col3[0].markdown("**Here are the columns with missing value**")

    with col1.expander("Train Data"):
        # Instantiate the validation data
        train_X = session["train_X"]
        train_y = session["train_y"]

        # Display the dataframe with number of missing values
        st.write(train_X.isna().sum().rename("N_NaN"))

        # Check if the target variable contains missing values
        st.write(f"Number of NaN in {session.target_name}: {train_y.isna().sum()}")

    with col2.expander("Validation Data"):
        # Instantiate the validation data
        valid_X = session["valid_X"]
        valid_y = session["valid_y"]

        # Display the dataframe with number of missing values
        st.write(valid_X.isna().sum().rename("N_NaN"))

        # Check if the target variable contains missing values
        st.write(f"Number of NaN in {session.target_name}: {valid_y.isna().sum()}")

    if "test" in session:
        with col4.expander("Test Data"):
            # Instantiate the validation data
            test = session["test"]

            # Display the dataframe with number of missing values
            st.write(test.isna().sum().rename("N_NaN"))
else:
    st.write("First split the data from the data split page to continue")
    st.write("cleaning your data.")



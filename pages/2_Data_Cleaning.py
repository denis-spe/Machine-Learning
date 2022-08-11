# import libraries ------------------------------------
from cmath import nan
import streamlit as st
import pandas as pd
import numpy as np

# Set the page main title
st.set_page_config(
    page_title="ML | Data Cleaning",
)

# Load Css file
def load_css(path):
    with open(path, mode='r') as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def nan_check(data: pd.DataFrame):
    """
    Check for missing values in the data frame.
    
    # Parameter:

        data: (pd.DataFrame)  data to check for missing values.

    # Return:  
        
        data_missing_df: Dataframe with number of missing data and precent.
    """
    # Get the missing values with 'isna' method.
    data_missing = data.isna().sum()

    # Calculate the precentage of missing values.
    precent = np.array(list(
        map(lambda x: str(x) + "%", list(np.round(data_missing / data.shape[0], 3) * 100))
        ))

    # Construct a missing values data frame.
    data_missing_df = pd.DataFrame({
        "Col": data.columns,
        "N_Missing_Values": data_missing,
        "Percent": precent
        }).reset_index(drop=True)
    
    return data_missing_df


# loading the css file 
load_css("style.css")

# Initialize the session
session = st.session_state

# Make a page title
st.markdown("# Data Cleaning")

# Seperate into pages.
SIDEBAR = st.sidebar
col3 = st.columns(2)
col1, col2, col4 = st.columns(3)

if "train_X" in session:
    col3[0].markdown("**Here are the columns with missing value**")

    # Instantiate the validation data.
    train_X: pd.DataFrame = session["train_X"]
    train_y: pd.Series = session["train_y"]

    # Instantiate the validation data.
    valid_X: pd.DataFrame = session["valid_X"]
    valid_y: pd.Series = session["valid_y"]

    try:
        # Instantiate the validation data.
        test: pd.DataFrame = session["test"]
    except KeyError:
        pass



    # Create options to handle missing values in the data .................

    # Add a subtitle in the sidebar.
    SIDEBAR.header('Options To Handle NaN')

    # Constructing a multiselector for columns to drop.
    drop_col = SIDEBAR.multiselect(
        label="Select columns to drop", 
        options=train_X.columns, 
        help="Choose columns to drop"
        )
    
    # Drop the columns in all dataset.
    train_X = train_X.drop(drop_col, axis=1)
    valid_X = valid_X.drop(drop_col, axis=1)

    try:
        # Catch the name error since test is optianal.
        test = test.drop(drop_col, axis=1)
    except NameError:
        pass

    SIDEBAR.write('---')

    # Make a select box to select columns to fill.
    col_to_fill = SIDEBAR.multiselect(
        label="Select columns to fill", 
        options=train_X.columns,
        )

    methods = [0, 'mean', 'median', 'mode', 'unknown'] * len(train_X.columns)

    def add_back_opt(x):
        methods.append(x)
        return x

    # A Select box to be used to fill missing values in the column.
    fill_options = SIDEBAR.multiselect(
        label="Options to be used to fill", 
        options= methods,
        )


    # Loop over a zip of col_to_fill with fill_options
    for col, fill in zip(col_to_fill, fill_options):
        if fill == 0 or fill == 'unknown':
            train_X = train_X.fillna({col: fill})
            valid_X = valid_X.fillna({col: fill})

            try:
                # Catch the name error since test is optianal.
                test = test.fillna({col: fill})
            except NameError:
                pass
        
        elif fill == 'mean':
            train_X = train_X.fillna({col: train_X[col].mean()})
            valid_X = valid_X.fillna({col: valid_X[col].mean()})

            try:
                # Catch the name error since test is optianal.
                test = test.fillna({col: test[col].mean()})
            except NameError:
                pass

        elif fill == 'median':
            train_X = train_X.fillna({col: train_X[col].median()})
            valid_X = valid_X.fillna({col: valid_X[col].median()})

            try:
                # Catch the name error since test is optianal.
                test = test.fillna({col: test[col].median()})
            except NameError:
                pass

        elif fill == 'mode':
            train_X = train_X.fillna({col: train_X[col].mode()[0]})
            valid_X = valid_X.fillna({col: valid_X[col].mode()[0]})

            try:
                # Catch the name error since test is optianal.
                test = test.fillna({col: test[col].mode()[0]})
            except NameError:
                pass
        
    # Create bar chart from showing the number missing values in each column .........
    col1.bar_chart(train_X.isna().sum())
    col2.bar_chart(valid_X.isna().sum())
    try:
        col4.bar_chart(test.isna().sum())
    except NameError:
        pass

    # Display dataframes .......................
    with col1.expander("Train Data"):

        # Construct a missing values data frame.
        train_X_missing_df = nan_check(train_X)

        # Display the dataframe with number of missing values.
        st.write(train_X_missing_df)

        # Check if the target variable contains missing values.
        st.write(f"Number of NaN in {session.target_name}: {train_y.isna().sum()}")

        # Add a dataframe for inspection
        st.write('---')
        st.write('## Train_X DataFrame')
        st.write(train_X)

    with col2.expander("Validation Data"):

        # Construct a missing values data frame.
        valid_X_missing_df = nan_check(valid_X)

        # Display the dataframe with number of missing values.
        st.write(valid_X_missing_df)

        # Check if the target variable contains missing values.
        st.write(f"Number of NaN in {session.target_name}: {valid_y.isna().sum()}")

        # Add a dataframe for inspection
        st.write('---')
        st.write('## Validation_X DataFrame')
        st.write(valid_X)

    if "test" in session:
        with col4.expander("Test Data"):

            # Construct a missing values data frame.
            test_X_missing_df = nan_check(test)

            # Display the dataframe with number of missing values.
            st.write(test_X_missing_df)

            # Add a dataframe for inspection
            st.write('---')
            st.write('## Test_X DataFrame')
            st.write(test)
else:
    st.write("First split the data from the data split page to continue")
    st.write("cleaning your data.")



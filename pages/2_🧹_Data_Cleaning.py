# Bless The Lord --- God ---

# import libraries ------------------------------------
from cmath import nan
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the page main title
st.set_page_config(
    page_title="ML | Data Cleaning",
    layout='wide'
    
)

# Load Css file
def load_css(path):
    with open(path, mode='r') as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def outliers(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Represent outliers in data
    
    # Parameter:

        data: (pd.Series) Data to check for outliner.
        column: (str) Column name.
    
    # Return:

        A DataFrame with outliner
    """

    q1 = np.percentile(data[column], 25)
    q3 = np.percentile(data[column], 75)

    # Calculate the interquartile range
    interquartile_range = q3 - q1

    # Initialize the lower threshold.
    lower_threshold = q1 - 1.5 * interquartile_range

    # Initialize the upper threshold.
    upper_threshold = q3 + 1.5 * interquartile_range

    # FIlter out outlinear values.
    filter_outlier_values = (data[column] < lower_threshold) | (data[column] > upper_threshold)
    filter_out_outlier = np.logical_not(filter_outlier_values)
    return {"no_outliers": filter_out_outlier, "outliers": filter_outlier_values}


def outliersChecker(data: pd.DataFrame) -> pd.DataFrame:
    """
    Represents a dataframe with column name of the data
    with number of outliers
    Parameter
    ----------
        data: pandas dataframe to check for outliers

    Return
    --------
        Dataframe with data column name with number of outliers
    """
    # Exclude all object columns
    columns = data.select_dtypes(exclude="object").columns
    
    outliers_data = [
        outliers(data, column)["outliers"].sum()
        for column in columns
    ]

    outliers_df = pd.DataFrame({
        "column": columns, 
        "num_outliers": outliers_data})

    return outliers_df.sort_values(by="num_outliers", ascending=False)


def drop_outliers(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Drops outliers in a columns if it has outliers values
    # Parameter
    ----------
        data: pandas data frame to remove outlier values
    
    # Return
    --------
        A new data frame without outlier
    """
    # slices for values without outliers
    no_outliers = outliers(data, column)["no_outliers"]

    # Select value which are not outliers
    data = data[no_outliers]
        
    return data

def drop_all_outliers(data: pd.DataFrame, columns) -> pd.DataFrame:
    for col in columns:
        data = drop_outliers(data, col)
        

    return data






def nan_check(data: pd.DataFrame) -> pd.DataFrame:
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

    # Adding column type column.
    data_missing_df['col_dtype'] = [
        str(data[column].dtypes)
        for column in data_missing_df['Col']
    ]

    # Sort the dataframe with N_Missing_Values.
    data_missing_df = data_missing_df.sort_values(by='N_Missing_Values', ascending=False)

    # Set the column as index
    data_missing_df = data_missing_df.set_index("Col")
    
    return data_missing_df


# loading the css file 
load_css("style.css")

# Initialize the session
session = st.session_state

# Make a page title
st.markdown("# Data Cleaning")

# Seperate into pages.
SIDEBAR = st.sidebar
SIDEBAR.markdown("# Data Cleaning")
col3 = st.columns(2)
col1, col2, col4 = st.columns(3)

if "train_X" in session:
    col3[0].markdown("**Here are the columns with missing value**")

    # Adding subtitles to the train sample and test data.
    col1.markdown("**Train Data Sample**")
    col2.markdown("**Validation Data Sample**")
    col4.markdown("**Test Data**")


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
    SIDEBAR.header('Options To Handle Missing Values(NaN)')

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
    
    # Drop columns with drop percentage greater than or e
    conditional_drop = SIDEBAR.number_input(
        label='Drop with percentage',
        help=('Drop all columns with number of missing\
            percentage greater than or equal to number of percent')
    )

    if conditional_drop > 0:
        # Check for missing values.
        train_X_check = nan_check(train_X)

        # Replace the % with ''.
        train_X_check['Percent'] = (
            train_X_check['Percent'].str
            .replace('%', '')
            .astype(float))

        # Get the columns with missing values
        train_col = train_X_check[
            train_X_check['Percent'] >= conditional_drop
            ]['Col']
        
        drop_col_list = train_col.tolist()

        # Drop the columns in all dataset.
        train_X = train_X.drop(drop_col_list, axis=1)
        valid_X = valid_X.drop(drop_col_list, axis=1)

        try:
            # Catch the name error since test is optianal.
            test = test.drop(drop_col_list, axis=1)
        except NameError:
            pass


    # Make a select box to select columns to fill.
    auto_methods = [
        "None",
        "mode to all", 
        "mode to only categorical",
        "mode to only numerical",
        "numerical median", 
        "numerical mean"
        ]
    
    auto_fill = SIDEBAR.selectbox(
        label='Auto fill all',
        options=auto_methods,
        help="Auto fill all categorical or numerical column"
    )


    # Make a select box to select columns to fill.
    col_to_fill = SIDEBAR.multiselect(
        label="Select columns to fill", 
        options=train_X.columns,
        help="while selecting make sure to select the option to use to fill your selected column."
        )

    methods = [0, 'mean', 'median', 'mode', 'unknown'] * len(train_X.columns)

    # A Select box to be used to fill missing values in the column.
    fill_options = SIDEBAR.multiselect(
        label="Options to be used to fill", 
        options= methods,
        help="After selecting the column, choose the option to use to fill your column."
        )

    SIDEBAR.write('---')

    # Add a subtitle in the sidebar.
    SIDEBAR.header('Handle Duplicates In Data')

    # Row to keep ducing check for duplicate.
    keep = SIDEBAR.selectbox(
        label="Keep", 
        options=["last", False, True],
        help="first : Drop duplicates except for the first occurrence.\
            last : Drop duplicates except for the last occurrence.\
            False : Drop all duplicates. inplace : bool, default False Whether \
            to drop duplicates in place or to return a copy. ignore_index : bool,"
        )

    # Subset for check or drop duplicate.
    subset_columns = list(train_X.columns)
    subset_columns.insert(0, None)
    subset = SIDEBAR.selectbox(
        label="Subset", 
        options=subset_columns,
        help="column label or sequence of labels, optional\
            Only consider certain columns for identifying duplicates,\
            by default use all of the columns."
        )


    # Drop duplicate
    drop_duplicate = SIDEBAR.selectbox(
        label="Drop Duplicates", 
        options=[False, True], 
        help="True: drop all duplicates. False: Don't drop duplicates."
        )

    # ** Dealing with outliers **
    SIDEBAR.write("-----")

    # Select the data frame to handlw for outliers
    SIDEBAR.write("Dataset To Drop Outliers") 

    # Get only the numeric data
    numeric_df = train_X.select_dtypes(exclude='object')

    # Select numeric columns
    train_numeric_selection = SIDEBAR.multiselect(
                label="Select Column To Drop Outliers In Train Data",
                options=numeric_df.columns,
                help="""Drop outlier values in the selected column, 
                Note: That dropping value will lead to loss of data"""
            )
    # Drop outliers values
    train_X = drop_all_outliers(train_X, train_numeric_selection)

    # Select numeric columns
    valid_numeric_selection = SIDEBAR.multiselect(
                label="Select Column To Drop Outliers In Validation Data",
                options=numeric_df.columns,
                help="""Drop outlier values in the selected column, 
                Note: That dropping value will lead to loss of data"""
    )
    # Drop outliers values
    valid_X = drop_all_outliers(valid_X, valid_numeric_selection)

    if 'test' in session:
        # Select numeric columns
        test_numeric_selection = SIDEBAR.multiselect(
                    label="Select Column To Drop Outliers In Test Data",
                    options=numeric_df.columns,
                    help="""Drop outlier values in the selected column, 
                    Note: That dropping value will lead to loss of data"""
                )
        # Drop outliers values
        test = drop_all_outliers(test, test_numeric_selection)
    
    


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

    
    for col in train_X.columns:
        if auto_fill == "mode to all":
            train_X = train_X.fillna({col: train_X[col].mode()[0]})
            valid_X = valid_X.fillna({col: valid_X[col].mode()[0]})

            try:
                # Catch the name error since test is optianal.
                test = test.fillna({col: test[col].mode()[0]})
            except NameError:
                pass
            except KeyError:
                continue

        if auto_fill == "mode to only categorical":
            if str(train_X[col].dtypes).startswith('object'):
                train_X = train_X.fillna({col: train_X[col].mode()[0]})
                valid_X = valid_X.fillna({col: valid_X[col].mode()[0]})

                try:
                    # Catch the name error since test is optianal.
                    test = test.fillna({col: test[col].mode()[0]})
                except NameError:
                    pass
            
        if auto_fill == "numerical median":
            if str(train_X[col].dtypes).startswith('int') or str(train_X[col].dtype).startswith('float'):
                train_X = train_X.fillna({col: train_X[col].median()})
                valid_X = valid_X.fillna({col: valid_X[col].median()})

                try:
                    # Catch the name error since test is optianal.
                    test = test.fillna({col: test[col].median()})
                except NameError:
                    pass
        
        if  auto_fill == "numerical mean":
            if str(train_X[col].dtypes).startswith('int') or str(train_X[col].dtype).startswith('float'):
                train_X = train_X.fillna({col: train_X[col].mean()})
                valid_X = valid_X.fillna({col: valid_X[col].mean()})

                try:
                    # Catch the name error since test is optianal.
                    test = test.fillna({col: test[col].mean()})
                except NameError:
                    pass
        
        if auto_fill == "mode to only numerical":
            if str(train_X[col].dtypes).startswith('int') or str(train_X[col].dtype).startswith('float'):
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

    # Drop the duplicates
    if drop_duplicate:
        if subset:
            train_X = train_X.drop_duplicates(subset=[subset])
            valid_X = valid_X.drop_duplicates(subset=[subset])
            try:
                test = test.drop_duplicates(subset=[subset])
            except NameError:
                    pass
        else:
            train_X = train_X.drop_duplicates(keep=keep)
            valid_X = valid_X.drop_duplicates(keep=keep)
            try:
                test = test.drop_duplicates(keep=keep)
            except NameError:
                    pass


    # Display dataframes .......................
    with col1.expander("Train Data"):

        st.write("## **Missing Values In Train X**")
        # Construct a missing values data frame.
        train_X_missing_df = nan_check(train_X)

        # Filter out the columns with missing values.
        train_missing_df = train_X_missing_df[train_X_missing_df['N_Missing_Values'] > 0]

        st.write("**Number of columns with missing values: {}**".format(train_missing_df.shape[0]))

        # Display the dataframe with number of missing values.
        st.write(train_X_missing_df)

        # Check if the target variable contains missing values.
        st.write(f"Number of NaN in {session.target_name}: {train_y.isna().sum()}")

        # Check for duplicate
        st.write("## **Duplicates In The Dataset**")
        if subset:
            st.write(f"Number of duplicates in {subset} column:  {train_X.duplicated(subset=[subset]).sum()}")
        else:
            st.write(f"Number of duplicates in rows:  {train_X.duplicated(keep=keep).sum()}")

        # **** Handling outlies ***
        st.write("## **Outliers In The Dataset**")
        st.write("Columns containing outlier values in train data")

        # Check for outliers
        checker = outliersChecker(train_X)
        st.write(checker)


        # Add a dataframe for inspection
        st.write('---')
        st.write('## Train_X DataFrame')
        st.write(train_X)

        # Data shape
        train_shape = train_X.shape
        st.info("""
        Train shape
        rows: {}
        columns: {}
        """.format(train_shape[0], train_shape[1])
        )

    with col2.expander("Validation Data"):

        st.write("## **Missing Values In Valid X**")

        # Construct a missing values data frame.
        valid_X_missing_df = nan_check(valid_X)

        # Filter out the columns with missing values.
        valid_missing_df = valid_X_missing_df[valid_X_missing_df['N_Missing_Values'] > 0]

        st.write("**Number of columns with missing values: {}**".format(valid_missing_df.shape[0]))

        # Display the dataframe with number of missing values.
        st.write(valid_X_missing_df)

        # Check if the target variable contains missing values.
        st.write(f"Number of NaN in {session.target_name}: {valid_y.isna().sum()}")

        # Check for duplicate
        st.write("## **Duplicates**")
        if subset:
            st.write(f"Number of duplicates in {subset} column:  {valid_X.duplicated(subset=[subset]).sum()}")
        else:
            st.write(f"Number of duplicates in row:  {valid_X.duplicated(keep=keep).sum()}")

        # **** Handling outlies ***
        st.write("## **Outliers In The Dataset**")
        st.write("Columns containing outlier values in validation data")

        # Check for outliers
        checker = outliersChecker(valid_X)
        st.write(checker)

        # Add a dataframe for inspection
        st.write('---')
        st.write('## Validation_X DataFrame')
        st.write(valid_X)

        # Data shape
        valid_shape = valid_X.shape
        st.info("""
        Valid shape
        rows: {}
        columns: {}
        """.format(valid_shape[0], valid_shape[1])
        )

    if "test" in session:
        with col4.expander("Test Data"):

            st.write("## **Missing Values In Test data**")

            # Construct a missing values data frame.
            test_X_missing_df = nan_check(test)

            # Filter out the columns with missing values.
            test_missing_df = test_X_missing_df[test_X_missing_df['N_Missing_Values'] > 0]

            st.write("**Number of columns with missing values: {}**".format(test_missing_df.shape[0]))

            # Display the dataframe with number of missing values.
            st.write(test_X_missing_df)

            # Check for duplicate
            st.write("## **Duplicates**")
            if subset:
                st.write(f"Number of duplicates in {subset} column:  {test.duplicated(subset=[subset]).sum()}")
            else:
                st.write(f"Number of duplicates in row:  {test.duplicated(keep=keep).sum()}")

            # **** Handling outlies ***
            st.write("## **Outliers In The Dataset**")
            st.write("Columns containing outlier values in test data")

            # Check for outliers
            checker = outliersChecker(test)
            st.write(checker)

            # Add a dataframe for inspection
            st.write('---')
            st.write('## Test_X DataFrame')
            st.write(test)

            # Data shape
            test_shape = test.shape
            st.info("""
            Test shape
            rows: {}
            columns: {}
            """.format(test_shape[0], test_shape[1])
            )

            # Add datasets to the session
            st.session_state['test'] = test
    
    # Add datasets to the session
    st.session_state['train_X'] = train_X
    st.session_state['valid_X'] = valid_X
    st.session_state['train_y'] = train_y
    st.session_state['valid_y'] = valid_y

    SIDEBAR.write("")
    SIDEBAR.write("")
    # Make a page title
    SIDEBAR.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
    SIDEBAR.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)

else:
    st.write("First split the data from the data split page to continue")
    st.write("cleaning your data.")

st.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
st.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)




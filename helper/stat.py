import pandas as pd
import numpy as np
from typing import Any


def outliers(data: pd.DataFrame, column: str) -> dict[str, bool | int | Any]:
    """
    Represent outliers in data
    
    # Parameter:

        data: (pd.Series) Data to check for outlier.
        column: (str) Column name.
    
    # Return:

        A DataFrame with outlier
    """

    q1 = np.percentile(data[column], 25)
    q3 = np.percentile(data[column], 75)

    # Calculate the  range
    inter_quartile_range = q3 - q1

    # Initialize the lower threshold.
    lower_threshold = q1 - 1.5 * inter_quartile_range

    # Initialize the upper threshold.
    upper_threshold = q3 + 1.5 * inter_quartile_range

    # Filter out outlier values.
    filter_outlier_values = (data[column] < lower_threshold) | (data[column] > upper_threshold)
    filter_out_outlier = np.logical_not(filter_outlier_values)
    return {"no_outliers": filter_out_outlier, "outliers": filter_outlier_values}


def outlier_checker(data: pd.DataFrame) -> pd.DataFrame:
    """
    Represents a data frame with column name of the data
    with number of outliers
    Parameter
    ----------
        data: pandas data frame to check for outliers

    Return
    --------
        Data frame with data column name with number of outliers
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
    for column in columns:
        data = drop_outliers(data, column)

    return data


def nan_check(data: pd.DataFrame) -> pd.DataFrame:
    """
    Check for missing values in the data frame.
    
    # Parameter:

        data: (pd.DataFrame)  data to check for missing values.

    # Return:  
        
        data_missing_df: Dataframe with number of missing data and percent.
    """
    # Get the missing values with 'isnan' method.
    data_missing = data.isna().sum()

    # Calculate the percentage of missing values.
    percent = np.array(list(
        map(lambda x: str(x) + "%", list(np.round(data_missing / data.shape[0], 3) * 100))
    ))

    # Construct a missing values data frame.
    data_missing_df = pd.DataFrame({
        "Col": data.columns,
        "N_Missing_Values": data_missing,
        "Percent": percent
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

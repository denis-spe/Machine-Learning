from typing import Dict, List

import pandas as pd


def separate_columns_by_threshold(data: pd.DataFrame, threshold: int) -> Dict[str, List]:
    # data columns
    columns = data.columns

    # Empty a categorical list
    categorical_list = []

    # Empty a continuous list
    continuous_list = []

    # Loop over the columns
    for column in columns:
        if data[column].nunique() <= threshold:
            # store the column to the categorical list
            categorical_list.append(column)
        else:
            # store the column to the continuous list
            continuous_list.append(column)

    return {
        "categorical_columns": categorical_list,
        "continuous_columns": continuous_list
    }

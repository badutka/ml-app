import pandas as pd
from ensure import ensure_annotations


@ensure_annotations
def is_numeric(df: pd.DataFrame | pd.Series) -> pd.Series | bool:
    """
    Function that check for numerical columns, returns series of boolean values when pd.DataFrame is passed, and boolean value when pd.Series is passed

    :param df: Pandas' DataFrame or Series object
    :return: Boolean value or a Pandas' Series of boolean values indicating if a column is - or which columns are - numerical.
    """
    if isinstance(df, pd.DataFrame):
        return df.apply(pd.api.types.is_numeric_dtype)
    elif isinstance(df, pd.Series):
        return pd.api.types.is_numeric_dtype(df)


@ensure_annotations
def get_num_cols(df: pd.DataFrame) -> pd.Index:
    """
    Function that extracts numerical columns (as Pandas' Index object) from a Pandas' DataFrame

    :param df: pd.DataFrame object to extract numerical columns from
    :return: pd.Index object of numerical columns of df
    """
    return df.columns[is_numeric(df)]


@ensure_annotations
def get_cat_cols(df: pd.DataFrame) -> pd.Index:
    """
    Function that extracts categorical columns (as Pandas' Index object) from a Pandas' DataFrame

    :param df: pd.DataFrame object to extract categorical columns from
    :return: pd.Index object of categorical columns of df
    """
    return df.columns[~is_numeric(df)]


@ensure_annotations
def group_below_top_n(count_df: pd.DataFrame, n: int, text: str) -> pd.DataFrame:
    """
    Function expects a DataFrame that counts number of occurrences of a given unique value in a certain df column,
    and returns a DataFrame, where all unique values except from top n are joined into 'Others'

    :param count_df: pd.DataFrame containing occurrences of unique values in a column
    :param n: int describing how many most frequently occurring unique values should not be concatenated
    :param text: name of the index of number of occurrences, e.g. 'Occurrences'.
    :return: pd.DataFrame containing top n most frequently occurring values with all other values joined into 'Others'
    """

    sorted_df = count_df.sort_values(by=text, ascending=False)
    top_n = sorted_df.iloc[:n]
    others_sum = sorted_df.iloc[n:].sum().values[0]
    others = pd.DataFrame({text: [others_sum]}, index=['Others'])
    pie_df = pd.concat([top_n, others], ignore_index=False)
    print(type(pie_df))
    return pie_df

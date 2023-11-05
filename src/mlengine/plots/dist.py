import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from collections import Counter
import pandas as pd
from typing import Optional
from ensure import ensure_annotations

from mlengine.dataops.dataframe import is_numeric, group_below_top_n, get_num_cols, get_cat_cols
from mlengine.config.settings import settings


@ensure_annotations
def create_pie_plot(column_data: pd.Series, others: Optional[int] = None) -> go.Figure:
    """
    Function that plots pie chart for a given column data

    :param column_data: Pandas Series - column data to be plotted on pie chart
    :param others: If not none, then concatenates all outside of top n=others into 'Others'
    :return: return plotly's go.Figure object
    """
    text = 'Occurrences'
    count_df = pd.DataFrame.from_dict(Counter(column_data), orient='index', columns=[text])

    if others is not None and len(count_df) > others:
        pie_df = group_below_top_n(count_df, others, text)
    else:
        pie_df = count_df

    fig = px.pie(pie_df, values=text, names=list(pie_df.index), hover_data=[text],
                 labels={text: text})

    fig.update_traces(textinfo='percent+label')

    return fig


@ensure_annotations
def create_histogram_plot(column_data: pd.Series) -> go.Figure:
    """
    Function that plots histogram for a given column data

    :param column_data: column_data: Pandas series - column data to be plotted on pie chart
    :return: return plotly's go.Figure object
    """
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Histogram(x=column_data), row=1, col=1)
    fig.update_traces(name=column_data.name)

    return fig


@ensure_annotations
def plot_features(df: pd.DataFrame, opt_cat: str = 'pie', others: Optional[int] = None):
    """
    Function that plots histograms or pie charts for all features (columns) of a given dataframe

    :param df: Pandas DataFrame - data to be plotted on histograms or pie charts
    :param opt_cat: string, if 'pie' then categorical features are plotted on pie chart, otherwise histogram is used
    :param others: number of top distinct groups that should not be joined into 'Others'. If None then no join is performed.
    :return: None
    """
    plots_array = []
    titles_array = []

    for column in df.columns:
        if not is_numeric(df=df[column]) and df[column].nunique() == df[column].size:
            plot = create_histogram_plot(column_data=df[column])
            titles_array.append(f'{df[column].size} unique values.')
        elif is_numeric(df=df[column]):
            plot = create_histogram_plot(column_data=df[column])
            titles_array.append(f'Histogram of {column}.')
        else:
            if opt_cat == 'pie':
                plot = create_pie_plot(column_data=df[column], others=others)
            else:
                plot = create_histogram_plot(column_data=df[column])
            titles_array.append(f'Pie chart of {column}.')

        plots_array.append(plot)

    # Determine the number of rows and columns in the grid
    num_rows = 5
    num_cols = len(plots_array) // num_rows + (len(plots_array) % num_rows > 0)

    subplot_types = ['pie' if plot.data and isinstance(plot.data[0], go.Pie) else 'xy' for plot in plots_array]

    combined_fig = make_subplots(
        rows=num_rows,
        cols=num_cols,
        specs=[[{"type": subplot_types[i * num_cols + j]} if i * num_cols + j < len(subplot_types) else {"type": "xy"} for j in range(num_cols)] for i in range(num_rows)],
        subplot_titles=titles_array
    )

    # Add plots to subplots
    for i, plot in enumerate(plots_array):
        col_num = (i % num_cols) + 1
        row_num = (i // num_cols) + 1
        for trace in plot.data:
            combined_fig.add_trace(trace, row=row_num, col=col_num)

    # Update layout and show the combined figure

    combined_fig.update_layout(dict(settings.plot_layouts.features_plots_layout))
    combined_fig.show()


@ensure_annotations
def histograms_across_feats(df: pd.DataFrame, column: str):
    """
    Function that plots histograms of a given column data (with kde for numerical data) across other CATEGORICAL features and their respective groups

    :param df: Pandas DataFrame - data to be plotted on histograms or pie charts
    :param column: str, name of the DataFrame column to be plotted
    :return: None
    """

    def rotate_xticklabels(axs):
        axs.set_xticks(axs.get_xticks())
        axs.set_xticklabels(axs.get_xticklabels(), rotation=40, ha="right")

    kde = bool(is_numeric(df[column]))
    cat_feats = get_cat_cols(df)

    fig, axs = plt.subplots(1, len(cat_feats) + 1, figsize=(25, 5))

    sns.histplot(data=df, x=column, bins=30, kde=kde, ax=axs[0], color='g')
    rotate_xticklabels(axs[0])

    for i, col in enumerate(cat_feats):
        sns.histplot(data=df, x=column, bins=30, kde=kde, ax=axs[i + 1], hue=col)
        rotate_xticklabels(axs[i + 1])

    plt.show()


@ensure_annotations
def distplots_across_feats(df: pd.DataFrame, column: str, mode: str = 'box'):
    """
    Function that plots histograms of a given column data (with kde for numerical data) across other CATEGORICAL features and their respective groups

    :param df: Pandas DataFrame - data to be plotted on histograms or pie charts
    :param column: str, name of the DataFrame column to be plotted
    :param mode: str - 'box', 'violin' or 'rug' - defines the type of additional plots embedded into histogram plot
    :return: None
    """
    for col in get_cat_cols(df):
        fig = px.histogram(df, x=column, color=col,
                           marginal=mode,
                           hover_data=df.columns)
        fig.update_layout(bargap=0.1, width=750)
        fig.show()

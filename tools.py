from pandas.api.types import is_numeric_dtype
from langchain.tools import tool
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect("bus_data.db")
df = pd.read_sql_query("SELECT * FROM bus_trips", conn)
conn.close()

@tool
def select_columns(columns:list[str]) -> list[dict]:
    """Return selected data columns. Use exact column names"""
    return df[columns].to_dict(orient="records")

#-----------------#
# Aggregate tools #
#-----------------#

@tool
def cols_mean(columns: list[str]) -> str:
    """Return means from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a mean for '{col}': numeric data is required."
    return str(data[columns[0]].mean().round(2))


@tool
def cols_sum(columns: list[str]) -> str:
    """Return sums from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a sum for '{col}': numeric data is required."
    return str(data[columns[0]].sum())

@tool
def cols_min(columns: list[str]) -> str:
    """Return mins from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a min for '{col}': numeric data is required."
    return str(data[columns[0]].min())

@tool
def cols_max(columns: list[str]) -> str:
    """Return maxes from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a max for '{col}': numeric data is required."
    return str(data[columns[0]].max())

@tool
def cols_count(columns: list[str]) -> str:
    """Return number of non-missing values from each selected column"""
    data = df[columns]
    return str(data[columns[0]].count())

@tool
def cols_median(columns: list[str]) -> str:
    """Return medians from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a median for '{col}': numeric data is required."
    return str(data[columns[0]].median().round(2))

@tool
def cols_unique(columns: list[str]) -> str:
    """Return number of distinct non-missing values from each selected column"""
    data = df[columns]
    return str(data[columns[0]].nunique())

@tool
def cols_std(columns: list[str]) -> str:
    """Return standard deviations from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a standard deviation for '{col}': numeric data is required."
    return str(data[columns[0]].std().round(2))


#---------------------#
# Visualization tools #
#---------------------#

@tool
def plot_bar_chart(column: list[str]):
    """Display a bar chart of trip counts of non-missing values in one column"""
    column = column[0]
    counts = df[column].value_counts()
    
    fig = plt.figure()
    plt.bar(counts.index, counts.values)
    plt.title(f"Number of Bus Trips by {column}")
    plt.xlabel(column)
    plt.ylabel(f"Number of Trips")
    plt.close(fig)
    return fig
    
@tool
def plot_histogram(column: list[str]):
    """Display a histogram showing the distribution of values in a column"""
    column = column[0]
    fig = plt.figure()
    plt.hist(df[column], bins=10, edgecolor="black")
    plt.title(f"Distribution of {column}")
    plt.xlabel(f"Number of {column}")
    plt.ylabel("Number of trips")
    plt.close(fig)
    return fig
    
@tool
def plot_scatterPlot(column: list[str]):
    """Display a scatter plot showing the relationship of two numeric variables"""
    column1 = column[0]
    column2 = column[1]
    fig = plt.figure()
    plt.scatter(df[column1], df[column2], alpha=0.6)
    plt.title(f"{column1} versus {column2}")
    plt.xlabel(f"Number of {column1}")
    plt.ylabel(column2)
    plt.close(fig)
    return fig
    
@tool
def plot_boxPlot(column: list[str]):
    """Display a box plot showing the spread of numeric data"""
    column = column[0]
    fig = plt.figure()
    plt.boxplot(df[column])
    plt.title(f"Spread of {column}")
    plt.ylabel(column)
    plt.close(fig)
    return fig

@tool
def plot_pieChart(column: list[str]):
    """Display a pie chat showing how selected value divided into categories"""
    counts = df[column].value_counts()
    fig = plt.figure()
    plt.pie(counts.values, labels = counts.index, autopct = "%1.1f%%")
    plt.title(f"{column[0]} across the trips")
    plt.close(fig)
    return fig


tools = [select_columns, cols_mean, cols_sum, cols_min,
        cols_max, cols_count, cols_median, cols_unique, cols_std,
        plot_bar_chart, plot_histogram, plot_scatterPlot, plot_boxPlot, plot_pieChart]
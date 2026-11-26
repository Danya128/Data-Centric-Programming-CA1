from pandas.api.types import is_numeric_dtype
from langchain.tools import tool
import pandas as pd
import sqlite3

conn = sqlite3.connect("bus_data.db")
df = pd.read_sql_query("SELECT * FROM bus_trips", conn)
conn.close()

@tool
def select_columns(columns:list[str]) -> list[dict]:
    """Return selected data columns. Use exact column names"""
    return df[columns].to_dict(orient="records")

#---------------------#
# Aggregate functions #
#---------------------#

@tool
def cols_mean(columns: list[str]) -> dict:
    """Return means from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a mean for '{col}': numeric data is required."
    return data.mean().round(2).to_dict()


@tool
def cols_sum(columns: list[str]) -> dict:
    """Return sums from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a sum for '{col}': numeric data is required."
    return data.sum().to_dict()

@tool
def cols_min(columns: list[str]) -> dict:
    """Return mins from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a min for '{col}': numeric data is required."
    return data.min().to_dict()

@tool
def cols_max(columns: list[str]) -> dict:
    """Return maxes from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a max for '{col}': numeric data is required."
    return data.max().to_dict()

@tool
def cols_count(columns: list[str]) -> dict:
    """Return number of non-missing values from each selected column"""
    data = df[columns]
    return data.count().to_dict()

@tool
def cols_median(columns: list[str]) -> dict:
    """Return medians from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a median for '{col}': numeric data is required."
    return data.median().round(2).to_dict()

@tool
def cols_unique(columns: list[str]) -> dict:
    """Return number of distinct non-missing values from each selected column"""
    data = df[columns]
    return data.nunique().to_dict()

@tool
def cols_std(columns: list[str]) -> dict:
    """Return standard deviations from each selected column"""
    data = df[columns]
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a standard deviation for '{col}': numeric data is required."
    return data.std().round(2).to_dict()



tools = [select_columns, cols_mean, cols_sum, cols_min, cols_max, cols_count, cols_median, cols_unique, cols_std]
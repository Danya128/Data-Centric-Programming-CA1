from pandas.api.types import is_numeric_dtype
from langchain.tools import tool
import pandas as pd
import sqlite3

conn = sqlite3.connect("bus_data.db")
df = pd.read_sql_query("SELECT * FROM bus_trips", conn)
conn.close()

# @tools
def select_columns(columns:list[str]) -> pd.DataFrame:
    """Return selected data columns. Use exact column names"""
    return df[columns]

#---------------------#
# Aggregate functions #
#---------------------#

# @tools
def cols_mean(data:pd.DataFrame) -> pd.Series:
    """Return means from each selected column"""
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a mean for '{col}': numeric data is required."
    return data.mean().round(2)

# @tools
def cols_sum(data:pd.DataFrame) -> pd.Series:
    """Return sums from each selected column"""
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a sum for '{col}': numeric data is required."
    return data.sum()

# @tools
def cols_min(data:pd.DataFrame) -> pd.Series:
    """Return mins from each selected column"""
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a min for '{col}': numeric data is required."
    return data.min()

# @tools
def cols_max(data:pd.DataFrame) -> pd.Series:
    """Return maxes from each selected column"""
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a max for '{col}': numeric data is required."
    return data.max()

# @tools
def cols_count(data:pd.DataFrame) -> pd.Series:
    """Return number of non-missing values from each selected column"""
    return data.count()

# @tools
def cols_median(data:pd.DataFrame) -> pd.Series:
    """Return medians from each selected column"""
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a median for '{col}': numeric data is required."
    return data.median().round(2)

# @tools
def cols_unique(data:pd.DataFrame) -> pd.Series:
    """Return number of distinct non-missing values from each selected column"""
    return data.nunique()

# @tools
def cols_std(data:pd.DataFrame) -> pd.Series:
    """Return standard deviations from each selected column"""
    for col in data.columns:
        if not is_numeric_dtype(data[col]):
            return f"Cannot calculate a standard deviation for '{col}': numeric data is required."
    return data.std().round(2)
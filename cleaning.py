import pandas as pd

def clean():
    df = pd.read_csv("data.csv")

    # Remove spaces around column names
    df.columns = df.columns.str.strip()

    # Check data types
    # print(df.dtypes)

    # Convert Date data type
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    # Missing values
    # print(df.isna().sum())

    # Flag negative values
    neg_count = 0
    for column in ["No_people", "Delay_minutes"]:
        negative = df[column] < 0
        if negative.any():
            neg_count += 1
            print(df.loc[negative])
    print(f"Negative values found: {neg_count}")
    
    return df

clean()
import pandas as pd


def clean_df(df):

    # Simple Manupulation of Dataframe
    df = df[df['Type'] == "Sale"]
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
    df['Amount'] = df['Amount'].abs()
    df['Was Venmoed'] = ' '
    df["Split Count"] = df.get("Split Count", 1)

    df['Description'] = df['Description'].astype(str).str.replace(r"#\d+.*", "", regex=True).str.strip()

    # End Manupulation of dataset

    return df
import pandas as pd


def clean_df(df):
    df = df[df['Type'] == "Sale"].copy() 

    # Simple Manupulation of Dataframe
    df = df[df['Type'] == "Sale"]
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
    df['Amount'] = df['Amount'].abs()
    df['Was Venmoed'] = ' '
    df["Split Count"] = df.get("Split Count", 1)

    # df['Description'] = df['Description'].astype(str).str.replace(r"#\d+.*", "", regex=True).str.strip()
    df['Description'] = (
    df['Description']
    .astype(str)  # ensure string type
    .str.replace(r'[^A-Za-z\s]', '', regex=True)  # keep only letters and spaces
    .str.replace(r'\s+', ' ', regex=True)  # collapse multiple spaces
    .str.strip()  # remove leading/trailing spaces
)

    # End Manupulation of dataset

    return df
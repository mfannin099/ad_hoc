# Before uploading CC Statement... add Columns:
# Account - str (last 4 digits of card) and Statement - Date of the CC Statement

import streamlit as st
import pandas as pd

st.title("Credit Card Statement Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file - Credit Card Statement", type=["csv"])

if uploaded_file is not None:
    # Read the file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    
    st.subheader("✅ File Uploaded Successfully!")

    # Simple Manupulation of Dataframe
    df = df[df['Type'] == "Sale"]
    df = df.sort_values(by="Transaction Date", ascending=True)

    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
    df['Amount'] = df['Amount'].abs()

    # Allow users to edit
    edited_df = st.data_editor(df, use_container_width=True)
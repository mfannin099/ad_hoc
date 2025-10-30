# Before uploading CC Statement... add Columns:
# Account - str (last 4 digits of card) and Statement - Date of the CC Statement

cc_categories = ['Bills & Utilities', 'Food & Drink', 'Entertainment', 'Shopping',
                    'Personal', 'Groceries', 'Gas', 'Money out', 'Health & Wellness',
                    'Travel', 'Automotive', 'Fees & Adjustments']

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Credit Card Dashboard",  # Tab name
    page_icon="💳",                      # Favicon emoji or image path
    layout="wide",                       # 'centered' or 'wide'
    initial_sidebar_state="expanded"     # optional
)
st.title("Credit Card Statement Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file - Credit Card Statement", type=["csv"])
if uploaded_file is not None:
    # Read the file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    
    st.subheader("✅ File Uploaded Successfully!")

    # Simple Manupulation of Dataframe
    df = df[df['Type'] == "Sale"]
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
    df['Amount'] = df['Amount'].abs()
    df['Was Venmoed'] = ' '

    # End Manupulation of dataset

    # Allow User to pick how data is sorted
    sort_options = [col for col in ["Category", "Amount", "Transaction Date"] if col in df.columns]
    sort_by = st.selectbox("📊 Sort data by:", sort_options)

    sort_order = st.radio("Sort order:", ["Ascending", "Descending"], horizontal=True)

    # Sort dynamically based on user input
    df = df.sort_values(
        by=sort_by,
        ascending=(sort_order == "Ascending")
    )

    # Display dataframe that users can edit
    edited_df = st.data_editor(
    df,
    column_config={
        "Was Venmoed": st.column_config.CheckboxColumn(
            "Was Venmoed",
            help="Mark if this transaction was reimbursed via Venmo",
            default=False
        )
    },
    hide_index=True, use_container_width=True
)

    # Note under the table

    st.markdown("**Note:** Possible categories for transactions include:")
    st.markdown("• " + "\n• ".join(cc_categories))

    st.divider() 
    st.write("")  

    # Begin some Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Number of Purchases", len(edited_df))
    with col2:
        st.metric("Sum of Transactions", f"${df['Amount'].sum():,.2f}")
    with col3:
        edited_df["Was Venmoed"] = edited_df["Was Venmoed"].apply(lambda x: True if str(x).strip().lower() == "true" else False)
        num_venmoed = edited_df["Was Venmoed"].sum()

        # Display the metric
        st.metric("Number of Purchases Venmoed For", value=int(num_venmoed))
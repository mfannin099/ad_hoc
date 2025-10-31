import streamlit as st
import pandas as pd
from constants import cc_categories

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
    df["Split Count"] = df.get("Split Count", 1)

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
        ),
        "Split Count": st.column_config.NumberColumn(
            "Split Count",
            help="Number of people you split this purchase with",
            min_value=0,
            max_value=10,
            step=1,
            format="%d",
            ),
    },
    hide_index=True, use_container_width=True
)
    # Note under the table
    st.markdown("**Note:** Possible categories for transactions include:")
    st.markdown("• " + "\n• ".join(cc_categories))
    st.divider() 
    
    
    edited_df["Amount Venmoed"] = edited_df["Amount"] * (edited_df["Split Count"] - 1) / edited_df["Split Count"]
    # Fixing the type of Was Venmoed columb so that it can be used in metrics
    edited_df["Was Venmoed"] = edited_df["Was Venmoed"].apply(lambda x: True if str(x).strip().lower() == "true" else False)

    # Avoid division by zero
    edited_df["Split Count"] = edited_df["Split Count"].replace(0, 1)

    edited_df["Amount Venmoed"] = edited_df["Amount"] * (edited_df["Split Count"] - 1) / edited_df["Split Count"]
    edited_df.loc[~edited_df["Was Venmoed"], "Amount Venmoed"] = 0

    # Filter only venmoed transactions
    venmoed_df = edited_df[edited_df["Was Venmoed"] == True]

    # Only display if there are any Venmoed transactions
    if not venmoed_df.empty:
        st.subheader("💸 Venmoed Transactions")
        st.dataframe(
            venmoed_df[["Category", "Amount", "Split Count", "Amount Venmoed"]],
            use_container_width=True,
        )



    st.divider() 
    st.write("")  

    # Begin some Metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Number of Purchases", len(edited_df))
    with col2:
        st.metric("Sum of Transactions", f"${df['Amount'].sum():,.2f}")
    with col3:
        num_venmoed = edited_df["Was Venmoed"].sum()
        # Display the metric
        st.metric("Number of Purchases Venmoed For", value=int(num_venmoed))
    with col4:
        st.metric("Sum of Venmo", value=f"${venmoed_df['Amount Venmoed'].sum():,.2f}")
    with col5:
        net_expense = df['Amount'].sum() - venmoed_df['Amount Venmoed'].sum()
        st.metric("Net Expense", value=f"${net_expense:,.2f}")

    #TODO: Plot by category type (maybe do this one)
    #TODO: Most common merchants/places spent money (top 5/10 etc) (and this one.... in st.columns(2)) together
    #TODO: Plot by time by month/week/ etc
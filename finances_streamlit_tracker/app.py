import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from constants import cc_categories
from utils import clean_df

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

    # Clean df function
    df = clean_df(df)

    # Allow User to pick how data is sorted
    sort_options = [col for col in ["Category", "Amount", "Transaction Date"] if col in df.columns]
    sort_by = st.selectbox("📊 Sort data by:", sort_options)

    sort_order = st.radio("Sort order:", ["Ascending", "Descending"], horizontal=True)

    # Sort dynamically based on user input
    df = df.sort_values(
        by=sort_by,
        ascending=(sort_order == "Ascending")
    )

    # --- Description (Merchant) Filter --- (Creating the filter)
    descriptions = df["Description"].dropna().unique()
    with st.sidebar:
        st.header("Filters")
        selected_merchants = st.multiselect(
            "Select Merchant(s):",
            options=sorted(descriptions),
            default=descriptions  # all selected by default
        )
        
    #Actually filtering the df
    filtered_df = df[(df["Description"].isin(selected_merchants))]

    # Display dataframe that users can edit
    edited_df = st.data_editor(
    filtered_df,
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

    # Begin the Plots to look at spending
    st.write()
    st.header("Spending Overview")

    col1,col2 = st.columns(2)

    # --- Plot 1: Spending by Category (Vertical) ---
    with col1:
        st.markdown("### Spending by Category")
        category_spend = (
            edited_df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
            .sort_values(by="Amount", ascending=False)
            .head(10)
        )

        chart1 = (
            alt.Chart(category_spend)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
            .encode(
                x=alt.X("Category:N", sort="-y", title="Category"),
                y=alt.Y("Amount:Q", title="Total Spent ($)"),
                tooltip=["Category", alt.Tooltip("Amount:Q", format="$.2f")]
            )
            .properties(height=400)
            .configure_axis(labelAngle=-30)
        )
        st.altair_chart(chart1, use_container_width=True)

    # --- Plot 2: Top Merchants/Places Spent (Horizontal) ---
    with col2:
        st.markdown("### Top Merchants / Places Spent")
        merchant_spend = (
            edited_df.groupby("Description")["Amount"]
            .sum()
            .reset_index()
            .sort_values(by="Amount", ascending=False)
            .head(10)
        )

        chart2 = (
            alt.Chart(merchant_spend)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusBottomLeft=5)
            .encode(
                y=alt.Y("Description:N", sort="-x", title="Merchant / Place"),
                x=alt.X("Amount:Q", title="Total Spent ($)"),
                tooltip=["Description", alt.Tooltip("Amount:Q", format="$.2f")]
            )
            .properties(height=400)
        )
        st.altair_chart(chart2, use_container_width=True)

    st.write()
    st.write()

    # Plotting expenses over time 
    st.subheader("Spending Overview")
    
    # --- User selects aggregation level ---
    agg_option = st.radio(
        "Aggregate spending by:",
        ("Daily", "Weekly", "Monthly"),
        horizontal=True
    )

    # --- Map selection to Pandas resample codes ---
    resample_map = {
        "Daily": "D",
        "Weekly": "W",
        "Monthly": "M"
    }

    # --- Aggregate accordingly ---
    freq = resample_map[agg_option]
    time_spend = (
        edited_df
        .set_index("Transaction Date")
        .resample(freq)["Amount"]
        .sum()
        .reset_index()
    )

    # --- Altair Line Chart ---
    chart = (
        alt.Chart(time_spend)
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=60))
        .encode(
            x=alt.X("Transaction Date:T", title=agg_option, axis=alt.Axis(format="%b %d, %Y")),
            y=alt.Y("Amount:Q", title="Total Spent ($)"),
            tooltip=[
                alt.Tooltip("Transaction Date:T", title=agg_option),
                alt.Tooltip("Amount:Q", format="$.2f", title="Total Spent"),
            ],
            color=alt.value("#0078D4")  # Streamlit blue
        )
        .properties(height=400)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    # --- Detect which date was clicked ---
    selected_points = alt.selection_point(name="click")

    # Unfortunately, Altair selections alone don't pass values back to Streamlit directly.
    # We'll simulate interactivity using a Streamlit widget below 👇

    # --- Manual fallback selection for Streamlit (works reliably) ---
    selected_date = st.selectbox(
        f"Select a {agg_option[:-2]} to view transactions:",
        options=sorted(time_spend["Transaction Date"].dt.date.unique()),
    )

    # --- Filter transactions for that date range ---
    if selected_date:
        if freq == "D":
            filtered_df = edited_df[edited_df["Transaction Date"].dt.date == selected_date]
        elif freq == "W":
            # Get the week start and end for the selected date
            start = pd.to_datetime(selected_date) - pd.offsets.Week(weekday=6)
            end = start + pd.offsets.Week()
            filtered_df = edited_df[
                (edited_df["Transaction Date"] >= start) & (edited_df["Transaction Date"] < end)
            ]
        elif freq == "M":
            start = pd.to_datetime(selected_date).replace(day=1)
            end = (start + pd.offsets.MonthEnd(1))
            filtered_df = edited_df[
                (edited_df["Transaction Date"] >= start) & (edited_df["Transaction Date"] <= end)
            ]

        st.markdown(f"### Transactions for {selected_date.strftime('%B %d, %Y')}")
        st.dataframe(filtered_df.sort_values("Transaction Date"))


    #TODO - Identify areas to improve spending... where can I save money
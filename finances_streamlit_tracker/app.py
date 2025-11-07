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
st.info(
    "📄 **Expected CSV Columns:** Transaction Date, Post Date, Description, Category, Type, Amount",
    icon="ℹ️"
)

tab1, tab2, tab3= st.tabs(["📊 Overview", "🔍 Money Saving Opportunties/Analysis", "💡Recommendations"])

if uploaded_file is not None:
    with tab1:
        # --- Overivew Section---
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

        col1,col2, col3 = st.columns(3)

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
            st.markdown("### Top Merchants by Spent")
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

        # --- Plot 3: Most Frequent Merchants (Vertical) ---
        with col3:
            st.markdown("### Most Frequent Merchants")
            merchant_freq = (
                edited_df.groupby("Description")["Amount"]
                .count()  # count number of transactions per merchant
                .reset_index(name="Transaction Count")
                .sort_values(by="Transaction Count", ascending=False)
                .head(10)
            )

            chart3 = (
                alt.Chart(merchant_freq)
                .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, color="#6baed6")
                .encode(
                    x=alt.X("Description:N", sort="-y", title="Merchant / Place"),
                    y=alt.Y("Transaction Count:Q", title="Number of Transactions"),
                    tooltip=["Description", "Transaction Count"]
                )
                .properties(height=400)
            )

            st.altair_chart(chart3, use_container_width=True)

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

    with tab2:
        # --- Analysis Section---
        tab2_df = edited_df.copy()
        tab2_df['Month'] = tab2_df['Transaction Date'].dt.to_period('M')

        # 1) Recurring subscriptions (merchant appears >= n months with similar amounts)
        months_seen = st.number_input(
        "📆 Minimum number of months to qualify as a recurring merchant",
        min_value=1,
        max_value=12,
        value=3,  # default
        step=1,
        help="Merchants appearing at least this many months will be flagged as recurring."
        )

        monthly_counts = tab2_df.groupby(['Description', 'Month'])['Amount'].sum().reset_index()
        recurrence = monthly_counts.groupby('Description').size().reset_index(name='months_seen')
        recurring_merchants = recurrence[recurrence['months_seen'] >= months_seen]['Description'].tolist()
        tab2_df['is_recurring_candidate'] = tab2_df['Description'].isin(recurring_merchants)

        recurring_summary = (
            tab2_df[tab2_df['is_recurring_candidate']]
            .groupby('Description')
            .size()
            .reset_index(name='Transaction Count')
            .sort_values('Transaction Count', ascending=False)
        )

        st.subheader(f"📆 Merchants recurring in ≥ {months_seen} months")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.dataframe(
                recurring_summary.style.set_properties(**{
                    'text-align': 'left',
                    'font-size': '14px',
                }),
                use_container_width=True,
                height=400
            )

        st.write("")
        st.write("")

        # --- 2) Frequent small purchases (many transactions with small avg amount) ---
        st.subheader("💸 Frequent Small Purchases")

        col1, col2 = st.columns(2)
        with col1:
            freq = st.number_input(
                "Minimum number of transactions per merchant",
                min_value=2,
                max_value=20,
                value=5,
                step=1,
                help="Merchants with at least this many transactions will be included."
            )
        with col2:
            mean_dollars = st.number_input(
                "Maximum average amount ($)",
                min_value=5,
                max_value=50,
                value=25,
                step=5,
                help="Merchants with an average spend below this amount will be included."
            )

        # --- Compute frequent small purchases ---
        merchant_stats = tab2_df.groupby('Description')['Amount'].agg(['count', 'mean']).reset_index()
        freq_small = merchant_stats[
            (merchant_stats['count'] >= freq) & (merchant_stats['mean'] < mean_dollars)
        ]

        tab2_df['is_freq_small'] = tab2_df['Description'].isin(freq_small['Description'])

        freq_small_summary = (
            tab2_df[tab2_df['is_freq_small']]
            .groupby('Description')
            .size()
            .reset_index(name='Transaction Count')
            .sort_values('Transaction Count', ascending=False)
        )

        # --- Display results nicely centered ---
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"#### Merchants with ≥ {freq} transactions and average spend < ${mean_dollars}")
            st.dataframe(
                freq_small_summary.style.set_properties(**{
                    'text-align': 'left',
                    'font-size': '14px',
                }),
                use_container_width=True,
                height=400
            )

        st.write("")
        st.write("")

        # --- 3) Large one-off purchases (high z-score vs global mean) ---
        st.subheader("💰 Large One-Off Purchases")

        # --- User-adjustable parameter ---
        z_threshold = st.slider(
            "Z-Score Threshold for Large Purchases",
            min_value=1.0,
            max_value=5.0,
            value=3.0,
            step=0.5,
            help="Transactions with a z-score above this threshold are flagged as large one-offs."
        )

        # --- Compute z-scores relative to global mean/std ---
        global_mean = tab2_df['Amount'].mean()
        global_std = tab2_df['Amount'].std()

        tab2_df['z_score_global'] = (tab2_df['Amount'] - global_mean) / global_std
        tab2_df['is_one_off_large'] = tab2_df['z_score_global'] > z_threshold

        # --- Summarize flagged merchants ---
        one_off_summary = (
            tab2_df[tab2_df['is_one_off_large']]
            .groupby('Description')
            .size()
            .reset_index(name='Transaction Count')
            .sort_values('Transaction Count', ascending=False)
        )

        # --- Display results nicely centered ---
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"#### Merchants with Purchases Having Z-Score > {z_threshold}")
            st.dataframe(
                one_off_summary.style.set_properties(**{
                    'text-align': 'left',
                    'font-size': '14px',
                }),
                use_container_width=True,
                height=400
            )

        # --- Optional: Display summary metrics ---
        st.caption(f"📊 Global mean spend: ${global_mean:,.2f} | Std dev: ${global_std:,.2f}")

        st.write("")
        st.write("")

        # --- 4) New Merchants (first seen in the last N days) ---
        st.subheader("🆕 New Merchants")

        # --- User-adjustable parameter ---
        days_threshold = st.slider(
            "Days since first seen (merchant considered 'new')",
            min_value=15,
            max_value=180,
            value=60,
            step=15,
            help="Merchants first appearing within this many days will be flagged as new."
        )

        # --- Compute new merchants ---
        first_seen = (
            tab2_df.groupby('Description')['Transaction Date']
            .min()
            .reset_index(name='first_seen')
        )
        tab2_df = tab2_df.merge(first_seen, on='Description', how='left')

        tab2_df['days_since_first'] = (
            pd.Timestamp.today() - pd.to_datetime(tab2_df['first_seen'])
        ).dt.days

        tab2_df['is_new_merchant'] = tab2_df['days_since_first'] <= days_threshold

        # --- Summarize flagged merchants ---
        new_merchant_summary = (
            tab2_df[tab2_df['is_new_merchant']]
            .groupby('Description')
            .size()
            .reset_index(name='Transaction Count')
            .sort_values('Transaction Count', ascending=False)
        )

        # --- Display results nicely centered ---
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"#### Merchants first seen within the last {days_threshold} days")
            st.dataframe(
                new_merchant_summary.style.set_properties(**{
                    'text-align': 'left',
                    'font-size': '14px',
                }),
                use_container_width=True,
                height=400
            )

        # --- Optional summary caption ---
        n_new_merchants = new_merchant_summary['Description'].nunique()
        st.caption(f"🗓️ Found {n_new_merchants} new merchant(s) first seen within the last {days_threshold} days.")

    with tab3:
        # --- Recommendations Section ---
        st.subheader("💡 Money-Saving Recommendations")

        st.info(
            "These recommendations are based on your selections and the analyses in the 'Money Saving Opportunities / Analysis' tab. "
            "Merchants flagged across multiple categories are prioritized."
        )

        # --- Compute cut score ---
        flags = [
            'is_recurring_candidate',
            'is_freq_small',
            'is_one_off_large',
            'is_new_merchant'
        ]

        tab2_df['cut_score'] = tab2_df[flags].sum(axis=1)
        candidate_df = tab2_df[tab2_df['cut_score'] >= 2].sort_values('cut_score', ascending=False)

        # --- Summarize candidates ---
        candidate_summary = (
            candidate_df.groupby('Description')['Amount']
            .agg(['count', 'sum'])
            .reset_index()
            .rename(columns={'count': 'Transactions', 'sum': 'Total Amount'})
            .sort_values('Total Amount', ascending=False)
        )
        candidate_summary['Total Amount'] = candidate_summary['Total Amount'].apply(lambda x: f"${x:,.2f}")


        # --- Display centered table ---
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("Merchants flagged as 'True' in 2 or more categories")
            st.dataframe(
                candidate_summary.style.set_properties(**{
                    'text-align': 'left',
                    'font-size': '14px',
                }),
                use_container_width=True,
                height=400
            )

        # --- Total potential savings ---
        total_savings = candidate_df['Amount'].sum()
        st.metric("💰 Estimated Total Potential Savings", f"${total_savings:,.2f}")



          

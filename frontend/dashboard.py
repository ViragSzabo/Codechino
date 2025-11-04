import io
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
from collections import Counter

# --- Add project root to Python path ---
project_root = Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))

# --- Import backend modules ---
from backend.sams_coffee_orders import df_orders
from backend.utils import df_to_pdf

# --- Sidebar filters ---
st.sidebar.header("Filters")
min_date = df_orders["Date"].min()
max_date = df_orders["Date"].max()
date_range = st.sidebar.date_input("Select date range", [min_date, max_date])

tables = st.sidebar.multiselect(
    "Select table(s)",
    options=sorted(df_orders["Table"].unique()),
    default=df_orders["Table"].unique()
)

all_items = sorted({item for order in df_orders["Items"] for item in order})
selected_items = st.sidebar.multiselect(
    "Select items (optional)",
    options=all_items,
    default=None
)

# --- Apply filters ---
filtered_df = df_orders[
    (df_orders["Date"] >= pd.to_datetime(date_range[0])) &
    (df_orders["Date"] <= pd.to_datetime(date_range[1])) &
    (df_orders["Table"].isin(tables))
]

if selected_items:
    filtered_df = filtered_df[filtered_df["Items"].apply(lambda x: any(i in x for i in selected_items))]

# --- Dashboard layout ---
st.title("☕ Sam's Coffee Orders Dashboard")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", len(filtered_df))
col2.metric("Total Revenue (€)", round(filtered_df["Total (€)"].sum(), 2))
col3.metric("Average Order (€)", round(filtered_df["Total (€)"].mean(), 2))

# --- Tabs ---
tabs = st.tabs(["Charts", "Orders Table", "Download Data"])

with tabs[0]:
    # Most popular tables
    st.subheader("Most Popular Tables")
    table_counts = filtered_df["Table"].value_counts()
    st.bar_chart(table_counts)

    # Revenue over time
    st.subheader("Revenue Over Time")
    revenue_over_time = filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Total (€)"].sum()
    st.line_chart(revenue_over_time)

    # Top items
    st.subheader("Top Ordered Items")
    all_items = [item for order in filtered_df["Items"] for item in order]
    top_items = Counter(all_items).most_common(10)
    top_items_df = pd.DataFrame(top_items, columns=["Item", "Count"])
    st.bar_chart(top_items_df.set_index("Item"))

with tabs[1]:
    st.subheader("Orders Table")
    st.dataframe(filtered_df)

with tabs[2]:
    st.subheader("Download Filtered Data")

    # CSV
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="filtered_orders.csv", mime="text/csv")

    # JSON
    json_data = filtered_df.to_json(orient="records", date_format="iso").encode("utf-8")
    st.download_button("Download JSON", data=json_data, file_name="filtered_orders.json", mime="application/json")

    # EXCEL
    excel_buffer = io.BytesIO()
    filtered_df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
    excel_buffer.seek(0)
    st.download_button("Download Excel", excel_buffer, "filtered_orders.xlsx")

    # PDF
    pdf_buffer = df_to_pdf(filtered_df)
    st.download_button("Download PDF", pdf_buffer, "filtered_orders.pdf")

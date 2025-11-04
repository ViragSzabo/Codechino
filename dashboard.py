import streamlit as st
import pandas as pd
import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

# Load data
with open("sam_orders.json", "r", encoding="utf-8") as f:
    orders = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(orders)
df["Date"] = pd.to_datetime(df["Date"])
df["Total (€)"] = df["Total (€)"].astype(float)

# Sidebar filters
st.sidebar.header("Filters")
years = st.sidebar.multiselect("Select year(s)", options=df["Date"].dt.year.unique(), default=df["Date"].dt.year.unique())
tables = st.sidebar.multiselect("Select table(s)", options=df["Table"].unique(), default=df["Table"].unique())

filtered_df = df[(df["Date"].dt.year.isin(years)) & (df["Table"].isin(tables))]

# Metrics
st.title("☕ Sam's Coffee Orders Dashboard")
st.metric("Total Orders", len(filtered_df))
st.metric("Total Revenue (€)", round(filtered_df["Total (€)"].sum(), 2))
st.metric("Average Order (€)", round(filtered_df["Total (€)"].mean(), 2))

# Most popular tables
table_counts = filtered_df["Table"].value_counts()
st.subheader("Most Popular Tables")
st.bar_chart(table_counts)

# Spending over time
st.subheader("Revenue Over Time")
revenue_over_time = filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Total (€)"].sum()
st.line_chart(revenue_over_time)

# Top items
st.subheader("Top Ordered Items")
all_items = [item for order in filtered_df["Items"] for item in order]
top_items = Counter(all_items).most_common(10)
top_items_df = pd.DataFrame(top_items, columns=["Item", "Count"])
st.bar_chart(top_items_df.set_index("Item"))

# Orders table
st.subheader("Orders Table")
st.dataframe(filtered_df)
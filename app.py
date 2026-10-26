import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="GreenLeaf Grocers Dashboard",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 GreenLeaf Grocers")
st.subheader("Inventory & Sales Management Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("GreenLeaf_Grocers_Sample_Dataset.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Unable to load the CSV file. Check that its filename matches the code.")
    st.stop()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

# Key performance indicators
total_revenue = filtered_df["Revenue_INR"].sum()
total_units = filtered_df["Units_Sold"].sum()
total_products = filtered_df["Product_ID"].nunique()
low_stock = filtered_df[
    filtered_df["Closing_Stock"] <= filtered_df["Reorder_Level"]
]["Product_ID"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("📦 Units Sold", f"{total_units:,.0f}")
col3.metric("🛒 Unique Products", f"{total_products}")
col4.metric("⚠️ Low-Stock Products", f"{low_stock}")

st.divider()

# Sales by category and region
left, right = st.columns(2)

with left:
    st.subheader("📊 Sales by Category")
    category_sales = (
        filtered_df.groupby("Category", as_index=False)["Revenue_INR"]
        .sum()
        .sort_values("Revenue_INR", ascending=False)
    )
    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Revenue_INR",
        color="Category",
        title="Revenue by Product Category"
    )
    st.plotly_chart(fig_category, use_container_width=True)

with right:
    st.subheader("🌍 Sales by Region")
    region_sales = (
        filtered_df.groupby("Region", as_index=False)["Revenue_INR"]
        .sum()
        .sort_values("Revenue_INR", ascending=False)
    )
    fig_region = px.pie(
        region_sales,
        names="Region",
        values="Revenue_INR",
        title="Revenue Share by Region"
    )
    st.plotly_chart(fig_region, use_container_width=True)

# Monthly sales trend
st.subheader("📈 Monthly Revenue Trend")

monthly_sales = filtered_df.dropna(subset=["Order_Date"]).copy()
monthly_sales["Month"] = monthly_sales["Order_Date"].dt.to_period("M").astype(str)
monthly_sales = (
    monthly_sales.groupby("Month", as_index=False)["Revenue_INR"]
    .sum()
    .sort_values("Month")
)

fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Revenue_INR",
    markers=True,
    title="Monthly Sales Revenue"
)
st.plotly_chart(fig_monthly, use_container_width=True)

# Top 10 products
st.subheader("🏆 Top 10 Products by Revenue")

top_products = (
    filtered_df.groupby("Product_Name", as_index=False)["Revenue_INR"]
    .sum()
    .sort_values("Revenue_INR", ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products.sort_values("Revenue_INR"),
    x="Revenue_INR",
    y="Product_Name",
    orientation="h",
    title="Top 10 Products"
)
st.plotly_chart(fig_products, use_container_width=True)

# Inventory monitoring
st.subheader("⚠️ Inventory Stock Monitoring")

stock_columns = [
    "Product_ID", "Product_Name", "Category",
    "Closing_Stock", "Reorder_Level"
]

inventory = filtered_df[stock_columns].drop_duplicates()
inventory = inventory.copy()
inventory["Stock Status"] = inventory.apply(
    lambda row: "Low Stock"
    if row["Closing_Stock"] <= row["Reorder_Level"]
    else "In Stock",
    axis=1
)

st.dataframe(inventory, use_container_width=True)

# Raw filtered data
with st.expander("View Filtered Sales Data"):
    st.dataframe(filtered_df, use_container_width=True)

st.caption("GreenLeaf Grocers | Inventory & Sales Analytics Project")

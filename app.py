import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile

@st.cache_data
def load_data():
    zip_path = "dataset/ezyZip.zip"
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall("dataset")
    data = pd.read_csv("dataset/processed_retail_data.csv")
    return data

data = load_data()

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

# Country filter (only if column exists)
if "Country" in data.columns:
    countries = data["Country"].dropna().unique().tolist()
    selected_country = st.sidebar.selectbox("Select Country", ["All"] + countries)
    if selected_country != "All":
        data = data[data["Country"] == selected_country]

# Product Category filter
if "Description" in data.columns:
    products = data["Description"].dropna().unique().tolist()
    selected_product = st.sidebar.selectbox("Select Product", ["All"] + products)
    if selected_product != "All":
        data = data[data["Description"] == selected_product]

# -----------------------
# Key Insights
# -----------------------

product_sales = (
    data.groupby("Description")
    .agg(Total_Sales=("Total_Price", "sum"))
    .reset_index()
    .sort_values(by="Total_Sales", ascending=False)
    .head(10)
)

monthly_sales = (
    data.groupby("Month")
    .agg(Total_Sales=("Total_Price", "sum"))
    .reset_index()
)

trending_product = (
    data.groupby("Description")["Month"]
    .agg(lambda x: x.mode()[0])
    .reset_index()
)


sales_by_country = data.groupby("Country").agg(
    Total_Sales=("Total_Price", "sum")
).reset_index().sort_values(by="Total_Sales", ascending=False)
top_ten_sales_by_country=sales_by_country.head(10)


peak_hours = data.groupby("Hours").agg(
    Total_Sales=("Total_Price", "sum")
).reset_index().sort_values(by="Total_Sales", ascending=False)
# -----------------------
# Dashboard Layout
# -----------------------
st.title("📊 Online Retail Store Dashboard")


# Monthly Sales
fig1 = px.line(monthly_sales,x="Month",y="Total_Sales",labels={"Month": "Month", "Total_Sales": "Total Sales"}
)
fig1.update_yaxes(range=[0, monthly_sales["Total_Sales"].max() * 1.1])
st.plotly_chart(fig1, use_container_width=True)

# Peak Hours Sales
st.subheader("Peak Sales Hour")
fig2 = px.bar(peak_hours, x="Hours", y="Total_Sales",color="Hours",color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig2, use_container_width=True)

# Top 10 Products
st.subheader("Top 10 Products by Sales")
fig3 = px.bar(product_sales, x="Description", y="Total_Sales",color="Description",color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig3, use_container_width=True)

# Trending Products
st.subheader("Trending Products")
fig4 = px.bar(trending_product.head(10), x="Description", y="Month",color="Description",color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig4, use_container_width=True)

# Top 10 Countries By Sales
st.subheader("Top 10 Countries By Sales")
fig5 = px.bar(top_ten_sales_by_country, x="Country", y="Total_Sales",color="Country",color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig5, use_container_width=True)





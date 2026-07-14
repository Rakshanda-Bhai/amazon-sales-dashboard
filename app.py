import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Amazon Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Amazon Sales Analytics Dashboard")
st.markdown("### Analyze Sales, Profit & Customer Performance")
@st.cache_data
def load_data():
    df = pd.read_csv(
        "Sample - Superstore.csv",
        encoding="latin1"
    )

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    return df

df = load_data()
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

segment = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment))
]
sales = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["Order ID"].nunique()
customers = filtered_df["Customer ID"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Total Sales",
    f"${sales:,.2f}"
)

c2.metric(
    "📈 Total Profit",
    f"${profit:,.2f}"
)

c3.metric(
    "📦 Orders",
    orders
)

c4.metric(
    "👥 Customers",
    customers
)
st.subheader("Sales by Category")

sales_category = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    sales_category,
    x="Category",
    y="Sales",
    color="Category",
    text_auto=".2s"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)
filtered_df["Month"] = filtered_df["Order Date"].dt.strftime("%b %Y")

monthly_sales = (
    filtered_df
    .groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
st.subheader("Top 10 Products")

top_products = (
    filtered_df
    .groupby("Product Name")["Sales"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig3 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)
st.subheader("Sales by Region")

region_sales = (
    filtered_df
    .groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig4 = px.pie(
    region_sales,
    values="Sales",
    names="Region",
    hole=0.5
)

st.plotly_chart(
    fig4,
    use_container_width=True
)
st.subheader("Profit by Segment")

segment_profit = (
    filtered_df
    .groupby("Segment")["Profit"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    segment_profit,
    x="Segment",
    y="Profit",
    color="Segment"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)
st.subheader("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)
left, right = st.columns(2)

# Sales by Category
sales_category = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    sales_category,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category"
)

left.plotly_chart(fig1, use_container_width=True)

# Profit by Category
profit_category = (
    filtered_df.groupby("Category")["Profit"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    profit_category,
    x="Category",
    y="Profit",
    color="Category",
    title="Profit by Category"
)

right.plotly_chart(fig2, use_container_width=True)
left, right = st.columns(2)

# Sales by Region
region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig3 = px.pie(
    region_sales,
    values="Sales",
    names="Region",
    hole=0.4,
    title="Sales by Region"
)

left.plotly_chart(fig3, use_container_width=True)

# Profit by Segment
segment_profit = (
    filtered_df.groupby("Segment")["Profit"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    segment_profit,
    x="Segment",
    y="Profit",
    color="Segment",
    title="Profit by Segment"
)

right.plotly_chart(fig4, use_container_width=True)
st.subheader("🏆 Top 10 Customers")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig5 = px.bar(
    top_customers,
    x="Sales",
    y="Customer Name",
    orientation="h",
    color="Sales"
)

st.plotly_chart(fig5, use_container_width=True)
st.subheader("🚚 Shipping Mode")

ship = (
    filtered_df.groupby("Ship Mode")["Sales"]
    .sum()
    .reset_index()
)

fig6 = px.pie(
    ship,
    values="Sales",
    names="Ship Mode",
    hole=0.5
)

st.plotly_chart(fig6, use_container_width=True)
st.subheader("💸 Discount vs Profit")

fig7 = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    size="Sales"
)

st.plotly_chart(fig7, use_container_width=True)
st.subheader("📌 Business Insights")

best_category = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

best_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

best_customer = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .idxmax()
)

st.success(f"""
### Key Insights

✅ Highest Sales Category : **{best_category}**

✅ Best Performing Region : **{best_region}**

✅ Top Customer : **{best_customer}**

""")
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_data.csv",
    "text/csv"
)
st.divider()

st.caption(
    "Amazon Sales Analytics Dashboard | Built using Streamlit, Pandas and Plotly"
)

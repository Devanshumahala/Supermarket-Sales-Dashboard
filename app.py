import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("supermarket_sales.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].apply(lambda x: x.replace(year=2025))
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')
df['Hour'] = df['Time'].dt.hour

# City mapping
city_map = {"Yangon": "Delhi", "Naypyitaw": "Mumbai", "Mandalay": "Bangalore"}
df["City"] = df["City"].replace(city_map)

# Sidebar filters
st.sidebar.header("Filter Data")
city_filter = st.sidebar.multiselect("Select City", options=df['City'].unique(), default=df['City'].unique())
gender_filter = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
product_filter = st.sidebar.multiselect("Select Product Line", options=df['Product line'].unique(), default=df['Product line'].unique())

# Filtered DataFrame
filtered_df = df[(df['City'].isin(city_filter)) & (df['Gender'].isin(gender_filter)) & (df['Product line'].isin(product_filter))]

st.title(" Supermarket Sales Dashboard (2025)")
st.markdown("---")

# KPI Section
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"₹{filtered_df['Total'].sum():,.2f}")
col2.metric("Invoices", f"{filtered_df['Invoice ID'].nunique()}")
col3.metric("Avg Rating", f"{filtered_df['Rating'].mean():.2f} ")
col4.metric("Gross Income", f"₹{filtered_df['gross income'].sum():,.2f}")

st.markdown("---")

# Graphs
st.subheader(" Interactive Visuals")

# Hourly Sales Trend
hourly_sales = filtered_df.groupby('Hour')['Total'].sum().reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=hourly_sales, x='Hour', y='Total', marker='o', ax=ax1, color='darkorange')
ax1.set_title("Sales by Hour", fontsize=14, fontweight='bold')
ax1.set_xlabel("Hour of Day")
ax1.set_ylabel("Total Sales (₹)")
st.pyplot(fig1)

# Product Line Sales
prod_sales = filtered_df.groupby("Product line")['Total'].sum().sort_values()
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x=prod_sales.values, y=prod_sales.index, palette="crest", ax=ax2)
ax2.set_title("Total Sales by Product Line")
ax2.set_xlabel("Sales")
ax2.set_ylabel("Product Line")
st.pyplot(fig2)

# City-wise Sales
city_sales = filtered_df.groupby("City")['Total'].sum().sort_values()
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.barplot(x=city_sales.values, y=city_sales.index, palette="viridis", ax=ax3)
ax3.set_title("Total Sales by City")
ax3.set_xlabel("Sales")
ax3.set_ylabel("City")
st.pyplot(fig3)

# Gender-wise Sales
gender_sales = filtered_df.groupby("Gender")['Total'].sum().sort_values()
fig4, ax4 = plt.subplots(figsize=(6, 4))
sns.barplot(x=gender_sales.index, y=gender_sales.values, palette="coolwarm", ax=ax4)
ax4.set_title("Total Sales by Gender")
ax4.set_xlabel("Gender")
ax4.set_ylabel("Sales")
st.pyplot(fig4)

# Monthly Sales Trend
monthly_sales = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['Total'].sum().reset_index()
monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()
monthly_sales['Month'] = monthly_sales['Date'].dt.strftime('%d-%m-%Y')
fig5, ax5 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=monthly_sales, x='Month', y='Total', marker='o', ax=ax5, color='green')
ax5.set_title("Monthly Sales Trend", fontsize=14, fontweight='bold')
ax5.set_xlabel("Month")
ax5.set_ylabel("Total Sales (₹)")
plt.xticks(rotation=45)
st.pyplot(fig5)

# Top Product + City Combos
top_combo = filtered_df.groupby(['Product line', 'City'])['Total'].sum().reset_index()
top_combo = top_combo.sort_values(by='Total', ascending=False).head(10)
fig6, ax6 = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_combo, x='Total', y='Product line', hue='City', palette='Set2', ax=ax6)
ax6.set_title("Top 10 Product + City Combos")
ax6.set_xlabel("Sales")
ax6.set_ylabel("Product Line")
st.pyplot(fig6)

st.markdown("---")

# Insights
st.subheader(" Business Insights")
try:
    with open("insights.txt", "r", encoding="utf-8") as f:
        insights = f.read()
    st.success(" Here's What We Discovered:")
    st.markdown(f"""<div style='background-color:#f0f2f6;padding:15px;border-radius:10px;'><pre style='white-space:pre-wrap;font-size:15px;'>{insights}</pre></div>""", unsafe_allow_html=True)
except:
    st.warning(" 'insights.txt' not found. Please make sure it exists in the project folder.")


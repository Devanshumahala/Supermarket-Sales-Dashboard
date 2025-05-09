import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Step 1: Create 'graphs' folder if not exists
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# Step 2: Load the dataset
try:
    df = pd.read_csv("supermarket_sales.csv", encoding="utf-8")
    print(" Data Loaded:", df.shape)
except Exception as e:
    print(" Error loading data:", e)
    exit()

# Step 3: Clean the data
df.dropna(inplace=True)
print("Data Cleaned:", df.shape)
# Step 4: Load the dataset
try:
    df = pd.read_csv("supermarket_sales.csv", encoding="utf-8")
    print(" Data Loaded:", df.shape)
except Exception as e:
    print(" Error loading data:", e)
    exit()

# Replace city names.
city_map = {
    "Yangon": "Delhi",
    "Naypyitaw": "Mumbai",
    "Mandalay": "Bangalore"
}
df["City"] = df["City"].replace(city_map)

# Step 5: Clean the data
df.dropna(inplace=True)
print("Data Cleaned:", df.shape)


# Step  6: First Graph – Total Sales by City
sales_by_city = df.groupby("City")["Total"].sum().sort_values()

plt.figure(figsize=(8, 5))
sns.barplot(x=sales_by_city.values, y=sales_by_city.index, palette="viridis")
plt.title("Total Sales by City")
plt.xlabel("Sales Amount")
plt.ylabel("City")
plt.tight_layout()
plt.savefig("graphs/sales_by_city.png")
plt.close()

print("First graph saved in 'graphs/sales_by_city.png'")
# Step 7: Gender-wise Total Sales

gender_sales = df.groupby("Gender")["Total"].sum().sort_values()

plt.figure(figsize=(6, 4))
sns.barplot(x=gender_sales.index, y=gender_sales.values, palette="coolwarm")
plt.title("Total Sales by Gender")
plt.xlabel("Gender")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("graphs/gender_sales.png")
plt.close()

print(" Gender-wise sales graph saved")
# Step 8: Product Line Performance (Total Sales per Category)

product_sales = df.groupby("Product line")["Total"].sum().sort_values()

plt.figure(figsize=(10, 6))
sns.barplot(x=product_sales.values, y=product_sales.index, palette="crest")
plt.title("Total Sales by Product Line")
plt.xlabel("Sales Amount")
plt.ylabel("Product Line")
plt.tight_layout()
plt.savefig("graphs/product_line_sales.png")
plt.close()

print(" Product line sales graph saved")
# Step 9: Monthly Sales Trend (Indian format & attractive)

df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].apply(lambda x: x.replace(year=2025))

monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Total'].sum().reset_index()
monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()

# Format date as Indian style: DD-MM-YYYY
monthly_sales['Date_Label'] = monthly_sales['Date'].dt.strftime('%d-%m-%Y')

plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
sns.lineplot(data=monthly_sales, x='Date_Label', y='Total', marker='o', color='darkgreen', linewidth=2.5)

plt.title("📈 Monthly Sales Trend", fontsize=16, fontweight='bold', color='navy')
plt.xlabel("Month (DD-MM-YYYY)", fontsize=12)
plt.ylabel("Total Sales (₹)", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("graphs/monthly_sales_trend.png")
plt.close()

print("Monthly Sales trend saved (Indian format, clean look)")
# Step 10: Top 10 Product Line & City Combinations by Total Sales

top_combo = (
    df.groupby(['Product line', 'City'])['Total']
    .sum()
    .reset_index()
    .sort_values(by='Total', ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_combo, x='Total', y='Product line', hue='City', palette='Set2')
plt.title("Top 10 Product Line & City Combinations by Sales", fontsize=14, fontweight='bold')
plt.xlabel("Total Sales (₹)")
plt.ylabel("Product Line")
plt.legend(title='City')
plt.tight_layout()
plt.savefig("graphs/top10_product_city_combos.png")
plt.close()

print(" Top 10 Product + City combo graph saved")
# Step 11: Sales by Hour (Customer Footfall Trend)

# Convert Time column to datetime and extract hour
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')
df['Hour'] = df['Time'].dt.hour

hourly_sales = df.groupby('Hour')['Total'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
sns.lineplot(data=hourly_sales, x='Hour', y='Total', marker='o', color='darkorange', linewidth=2.5)

plt.title(" Hourly Sales Trend", fontsize=16, fontweight='bold', color='darkred')
plt.xlabel("Hour of Day (24H Format)", fontsize=12)
plt.ylabel("Total Sales (₹)", fontsize=12)
plt.xticks(hourly_sales['Hour'])
plt.grid(True)
plt.tight_layout()
plt.savefig("graphs/hourly_sales_trend.png")
plt.close()

print("Hourly sales trend graph saved (customer footfall analysis)")






import pandas as pd
import matplotlib.pyplot as plt
import os


# -----------------------------
# Load Cleaned Dataset
# -----------------------------

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(
    project_path,
    "data",
    "cleaned_online_retail.csv"
)

data = pd.read_csv(file_path)


print("Dataset Loaded Successfully!")
print(data.head())
print(data.shape)


# -----------------------------
# Data Preparation
# -----------------------------

# Convert InvoiceDate into datetime
data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])


# Create Revenue column
data["Revenue"] = data["Quantity"] * data["Price"]


print("\nRevenue Column Added")
print(data.head())


# -----------------------------
# 1. Total Business Metrics
# -----------------------------

total_revenue = data["Revenue"].sum()
total_orders = data["Invoice"].nunique()
total_customers = data["Customer ID"].nunique()
total_products = data["StockCode"].nunique()


print("\nBusiness Metrics")
print("Total Revenue:", total_revenue)
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Total Products:", total_products)



# -----------------------------
# 2. Monthly Sales Trend
# -----------------------------

data["Month"] = data["InvoiceDate"].dt.to_period("M")

monthly_sales = data.groupby("Month")["Revenue"].sum()


plt.figure(figsize=(10,5))

monthly_sales.plot()

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(project_path, "assets", "monthly_sales_trend.png")
)

plt.show()



# -----------------------------
# 3. Top 10 Products
# -----------------------------

top_products = (
    data.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


plt.figure(figsize=(10,5))

top_products.plot(kind="bar")

plt.title("Top 10 Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")

plt.xticks(rotation=75)

plt.tight_layout()

plt.savefig(
    os.path.join(project_path, "assets", "top_products.png")
)

plt.show()



# -----------------------------
# 4. Top Countries by Revenue
# -----------------------------

country_sales = (
    data.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


plt.figure(figsize=(10,5))

country_sales.plot(kind="bar")

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Country")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(project_path, "assets", "top_countries.png")
)

plt.show()



# -----------------------------
# 5. Customer Revenue Analysis
# -----------------------------

customer_sales = (
    data.groupby("Customer ID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


print("\nTop Customers:")
print(customer_sales)



print("\nEDA Completed Successfully!")
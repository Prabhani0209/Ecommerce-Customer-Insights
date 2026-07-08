import pandas as pd
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt


# -----------------------------
# Load Cleaned Data
# -----------------------------

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(
    project_path,
    "data",
    "cleaned_online_retail.csv"
)

data = pd.read_csv(file_path)


# Convert date
data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])


# Create Revenue
data["Revenue"] = data["Quantity"] * data["Price"]


print("Data Loaded")
print(data.head())


# -----------------------------
# Create RFM Table
# -----------------------------

reference_date = data["InvoiceDate"].max()


rfm = data.groupby("Customer ID").agg({

    "InvoiceDate": lambda x: (reference_date - x.max()).days,

    "Invoice": "nunique",

    "Revenue": "sum"

})


# Rename columns

rfm.columns = [
    "Recency",
    "Frequency",
    "Monetary"
]


print("\nRFM Data:")
print(rfm.head())


# -----------------------------
# Scaling Data
# -----------------------------

scaler = StandardScaler()

rfm_scaled = scaler.fit_transform(rfm)


# -----------------------------
# K-Means Model
# -----------------------------

kmeans = KMeans(
    n_clusters=3,
    random_state=42
)


rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)


print("\nCustomer Segments:")
print(rfm.head())


# -----------------------------
# Cluster Count
# -----------------------------

print("\nCluster Distribution:")
print(rfm["Cluster"].value_counts())


# -----------------------------
# Save Result
# -----------------------------

output_file = os.path.join(
    project_path,
    "data",
    "customer_segments.csv"
)


rfm.to_csv(output_file)


print("\nCustomer segmentation completed!")
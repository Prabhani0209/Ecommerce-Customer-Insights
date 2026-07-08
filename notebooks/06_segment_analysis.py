import pandas as pd
import os
import matplotlib.pyplot as plt


# Project path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Load customer segments
file_path = os.path.join(
    project_path,
    "data",
    "customer_segments.csv"
)

rfm = pd.read_csv(file_path)


print("Customer Segment Data Loaded")
print(rfm.head())


# -----------------------------
# Rename Clusters
# -----------------------------

cluster_names = {
    0: "Regular Customers",
    1: "VIP Customers",
    2: "Low Value Customers"
}


rfm["Customer Segment"] = rfm["Cluster"].map(cluster_names)


print("\nSegment Names Added")
print(rfm.head())


# -----------------------------
# Segment Count
# -----------------------------

segment_count = rfm["Customer Segment"].value_counts()


print("\nCustomer Distribution:")
print(segment_count)


# -----------------------------
# Create Chart
# -----------------------------

plt.figure(figsize=(8,5))

segment_count.plot(kind="bar")

plt.title("Customer Segments Distribution")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")

plt.xticks(rotation=45)

plt.tight_layout()


output = os.path.join(
    project_path,
    "assets",
    "customer_segments.png"
)

plt.savefig(output)

plt.show()


# Save final segment data

output_file = os.path.join(
    project_path,
    "data",
    "final_customer_segments.csv"
)

rfm.to_csv(output_file,index=False)


print("\nSegment Analysis Completed!")
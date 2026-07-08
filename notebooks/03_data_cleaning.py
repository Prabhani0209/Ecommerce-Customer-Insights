import pandas as pd
import os


# Find project location
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Original dataset path
input_file = os.path.join(project_path, "data", "online_retail_II.csv")


# Load dataset
data = pd.read_csv(input_file)


print("Original Data Shape:")
print(data.shape)


# Remove duplicate rows
data = data.drop_duplicates()


print("\nAfter Removing Duplicates:")
print(data.shape)


# Remove rows where Customer ID is missing
data = data.dropna(subset=["Customer ID"])


# Remove rows where Description is missing
data = data.dropna(subset=["Description"])


print("\nAfter Removing Missing Values:")
print(data.shape)


# Convert InvoiceDate to datetime format
data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])


# Remove cancelled transactions
data = data[data["Quantity"] > 0]


# Remove invalid prices
data = data[data["Price"] > 0]


print("\nAfter Removing Invalid Transactions:")
print(data.shape)


# Save cleaned dataset

output_file = os.path.join(
    project_path,
    "data",
    "cleaned_online_retail.csv"
)


data.to_csv(output_file, index=False)


print("\nCleaning Completed!")
print("Cleaned file saved successfully.")
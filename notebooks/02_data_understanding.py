import pandas as pd
import os

# Get project path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset path
file_path = os.path.join(project_path, "data", "online_retail_II.csv")

# Load dataset
data = pd.read_csv(file_path)


# Missing values
print("\nMissing Values:")
print(data.isnull().sum())


# Duplicate rows
print("\nDuplicate Rows:")
print(data.duplicated().sum())


# Data types
print("\nData Types:")
print(data.dtypes)


# Statistical summary
print("\nStatistical Summary:")
print(data.describe())
import pandas as pd
import os

# Get project path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset path
file_path = os.path.join(project_path, "data", "online_retail_II.csv")

# Load dataset
data = pd.read_csv(file_path)

# Display first 5 rows
print(data.head())

# Display shape
print(data.shape)

# Display columns
print(data.columns)
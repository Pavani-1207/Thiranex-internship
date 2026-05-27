import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# ====================================
# CREATE FOLDERS
# ====================================

os.makedirs("output", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ====================================
# LOAD DATASET
# ====================================

print("Loading Customer Dataset...")

df = pd.read_csv("dataset/customers.csv")

print("\nDataset Loaded Successfully!")
print(f"Dataset Shape: {df.shape}")

# ====================================
# DATA CLEANING
# ====================================

print("\nStarting Data Cleaning Process...")

# Remove duplicates
duplicates = df.duplicated().sum()
df.drop_duplicates(inplace=True)

# Handle missing values
missing_values = df.isnull().sum().sum()
df.fillna(method='ffill', inplace=True)

print(f"Duplicate Rows Removed: {duplicates}")
print(f"Missing Values Handled: {missing_values}")

# ====================================
# FEATURE SELECTION
# ====================================

# Using Annual Income and Spending Score
X = df[['Annual Income (k$)', 'Spending Score (1-100)']]

# ====================================
# FEATURE SCALING
# ====================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ====================================
# K-MEANS CLUSTERING
# ====================================

print("\nPerforming Customer Segmentation...")

kmeans = KMeans(n_clusters=5, random_state=42)

df['Cluster'] = kmeans.fit_predict(X_scaled)

print("Customer Segmentation Completed!")

# ====================================
# SAVE SEGMENTED DATA
# ====================================

segmented_file = "output/customer_segments.csv"

df.to_csv(segmented_file, index=False)

print(f"\nSegmented Data Saved To:\n{segmented_file}")

# ====================================
# CLUSTER ANALYSIS
# ====================================

cluster_summary = df.groupby('Cluster')[[
    'Annual Income (k$)',
    'Spending Score (1-100)'
]].mean()

print("\n========== CLUSTER SUMMARY ==========")
print(cluster_summary)

# ====================================
# VISUALIZATION
# ====================================

print("\nGenerating Segmentation Graph...")

plt.figure(figsize=(8, 6))

scatter = plt.scatter(
    df['Annual Income (k$)'],
    df['Spending Score (1-100)'],
    c=df['Cluster']
)

plt.title('Customer Segmentation')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')

chart_path = "reports/customer_segmentation.png"

plt.tight_layout()
plt.savefig(chart_path)
plt.close()

print("Visualization Generated Successfully!")

# ====================================
# AUTOMATED REPORT
# ====================================

report_path = "reports/report.txt"

with open(report_path, "w") as report:

    report.write("CUSTOMER SEGMENTATION PROJECT\n")
    report.write("====================================\n\n")

    report.write("PROJECT SUMMARY\n")
    report.write("--------------------------\n")

    report.write(f"Dataset Shape           : {df.shape}\n")
    report.write(f"Duplicate Rows Removed  : {duplicates}\n")
    report.write(f"Missing Values Handled  : {missing_values}\n\n")

    report.write("CUSTOMER SEGMENTS\n")
    report.write("--------------------------\n")

    report.write(cluster_summary.to_string())

    report.write("\n\nFILES GENERATED\n")
    report.write("--------------------------\n")

    report.write("1. customer_segments.csv\n")
    report.write("2. customer_segmentation.png\n")
    report.write("3. report.txt\n")

print(f"\nAutomated Report Generated:\n{report_path}")

# ====================================
# EXPORT CLUSTER SUMMARY
# ====================================

excel_path = "output/cluster_summary.xlsx"

cluster_summary.to_excel(excel_path)

print(f"\nCluster Summary Saved To:\n{excel_path}")

# ====================================
# FINAL MESSAGE
# ====================================

print("\n===================================")
print("TASK COMPLETED SUCCESSFULLY!")
print("Customer Segmentation Project Finished")
print("===================================")
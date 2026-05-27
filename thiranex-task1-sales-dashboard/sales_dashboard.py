import pandas as pd
import matplotlib.pyplot as plt
import os

# ====================================
# CREATE FOLDERS
# ====================================

os.makedirs("output", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ====================================
# LOAD DATASET
# ====================================

print("Loading Sales Dataset...")

df = pd.read_csv("dataset/sales_data.csv", encoding='latin1')

print("\nDataset Loaded Successfully!")
print(f"Dataset Shape: {df.shape}")

# ====================================
# DATA CLEANING
# ====================================

print("\nStarting Data Cleaning...")

duplicates = df.duplicated().sum()
df.drop_duplicates(inplace=True)

missing_values = df.isnull().sum().sum()
df.fillna(method='ffill', inplace=True)

# Convert Date
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

print(f"Duplicate Rows Removed: {duplicates}")
print(f"Missing Values Handled: {missing_values}")

# ====================================
# KPI ANALYSIS
# ====================================

print("\nGenerating KPI Dashboard...")

total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
total_orders = df['order_id'].nunique()

top_product = (
    df.groupby('sub-category')['sales']
    .sum()
    .idxmax()
)

top_region = (
    df.groupby('region')['sales']
    .sum()
    .idxmax()
)

print("\n========== KPI SUMMARY ==========")
print(f"Total Sales       : ${total_sales:,.2f}")
print(f"Total Profit      : ${total_profit:,.2f}")
print(f"Total Orders      : {total_orders}")
print(f"Top Product       : {top_product}")
print(f"Top Region        : {top_region}")

# ====================================
# VISUALIZATION 1
# SALES BY REGION
# ====================================

region_sales = (
    df.groupby('region')['sales']
    .sum()
)

plt.figure(figsize=(8, 5))

region_sales.plot(kind='bar')

plt.title('Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales')

chart1 = "reports/sales_by_region.png"

plt.tight_layout()
plt.savefig(chart1)
plt.close()

# ====================================
# VISUALIZATION 2
# MONTHLY SALES TREND
# ====================================

monthly_sales = (
    df.groupby(df['order_date'].dt.month)['sales']
    .sum()
)

plt.figure(figsize=(8, 5))

monthly_sales.plot(marker='o')

plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')

chart2 = "reports/monthly_sales_trend.png"

plt.tight_layout()
plt.savefig(chart2)
plt.close()

# ====================================
# VISUALIZATION 3
# TOP PRODUCTS
# ====================================

top_products = (
    df.groupby('sub-category')['sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

top_products.plot(kind='bar')

plt.title('Top 10 Products by Sales')
plt.xlabel('Product')
plt.ylabel('Sales')

chart3 = "reports/top_products.png"

plt.tight_layout()
plt.savefig(chart3)
plt.close()

print("\nDashboard Charts Generated Successfully!")

# ====================================
# EXPORT KPI SUMMARY
# ====================================

summary_df = pd.DataFrame({
    'Metric': [
        'Total Sales',
        'Total Profit',
        'Total Orders',
        'Top Product',
        'Top Region'
    ],
    'Value': [
        total_sales,
        total_profit,
        total_orders,
        top_product,
        top_region
    ]
})

excel_path = "output/kpi_summary.xlsx"

summary_df.to_excel(excel_path, index=False)

print(f"\nKPI Summary Saved To:\n{excel_path}")

# ====================================
# SAVE CLEANED DATA
# ====================================

cleaned_file = "output/cleaned_sales_data.csv"

df.to_csv(cleaned_file, index=False)

# ====================================
# AUTOMATED REPORT
# ====================================

report_path = "reports/report.txt"

with open(report_path, "w") as report:

    report.write("SALES & REVENUE ANALYSIS DASHBOARD\n")
    report.write("====================================\n\n")

    report.write("PROJECT SUMMARY\n")
    report.write("--------------------------\n")

    report.write(f"Dataset Shape           : {df.shape}\n")
    report.write(f"Duplicate Rows Removed  : {duplicates}\n")
    report.write(f"Missing Values Handled  : {missing_values}\n\n")

    report.write("KPI SUMMARY\n")
    report.write("--------------------------\n")

    report.write(f"Total Sales      : ${total_sales:,.2f}\n")
    report.write(f"Total Profit     : ${total_profit:,.2f}\n")
    report.write(f"Total Orders     : {total_orders}\n")
    report.write(f"Top Product      : {top_product}\n")
    report.write(f"Top Region       : {top_region}\n\n")

    report.write("FILES GENERATED\n")
    report.write("--------------------------\n")

    report.write("1. cleaned_sales_data.csv\n")
    report.write("2. kpi_summary.xlsx\n")
    report.write("3. sales_by_region.png\n")
    report.write("4. monthly_sales_trend.png\n")
    report.write("5. top_products.png\n")
    report.write("6. report.txt\n")

print(f"\nAutomated Report Generated:\n{report_path}")

# ====================================
# FINAL MESSAGE
# ====================================

print("\n===================================")
print("TASK COMPLETED SUCCESSFULLY!")
print("Sales Dashboard Project Finished")
print("===================================")
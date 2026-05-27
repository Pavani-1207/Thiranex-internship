import pandas as pd
import matplotlib.pyplot as plt
import os

# ==============================
# CREATE FOLDERS AUTOMATICALLY
# ==============================

os.makedirs("output", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ==============================
# LOAD DATASET
# ==============================

print("Loading dataset...")

df = pd.read_csv("dataset/sales_data.csv", encoding='latin1')

print("\nDataset Loaded Successfully!")
print(f"Original Dataset Shape: {df.shape}")

# ==============================
# DATA CLEANING
# ==============================

print("\nStarting Data Cleaning Process...")

# Remove duplicate rows
duplicate_rows = df.duplicated().sum()
df.drop_duplicates(inplace=True)

print(f"Removed Duplicate Rows: {duplicate_rows}")

# Handle missing values
missing_values = df.isnull().sum().sum()

# Fill missing values using forward fill
df.fillna(method='ffill', inplace=True)

print(f"Handled Missing Values: {missing_values}")

# Convert date column
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

print("\nColumn Names Standardized!")

print(f"\nCleaned Dataset Shape: {df.shape}")

# ==============================
# SAVE CLEANED DATA
# ==============================

cleaned_file = "output/cleaned_sales_data.csv"

df.to_csv(cleaned_file, index=False)

print(f"\nCleaned Dataset Saved To:\n{cleaned_file}")

# ==============================
# KPI ANALYSIS
# ==============================

print("\nGenerating KPI Analysis...")

total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
total_orders = df['order_id'].nunique()

top_category = (
    df.groupby('category')['sales']
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
print(f"Top Category      : {top_category}")
print(f"Top Sales Region  : {top_region}")

# ==============================
# VISUALIZATION 1
# SALES BY CATEGORY
# ==============================

print("\nGenerating Charts...")

category_sales = (
    df.groupby('category')['sales']
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))

category_sales.plot(kind='bar')

plt.title('Sales by Category')
plt.xlabel('Category')
plt.ylabel('Sales')
plt.xticks(rotation=0)

chart1 = "reports/sales_by_category.png"

plt.tight_layout()
plt.savefig(chart1)
plt.close()

# ==============================
# VISUALIZATION 2
# MONTHLY SALES TREND
# ==============================

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

# ==============================
# VISUALIZATION 3
# PROFIT BY REGION
# ==============================

region_profit = (
    df.groupby('region')['profit']
    .sum()
)

plt.figure(figsize=(8, 5))

region_profit.plot(kind='bar')

plt.title('Profit by Region')
plt.xlabel('Region')
plt.ylabel('Profit')

chart3 = "reports/profit_by_region.png"

plt.tight_layout()
plt.savefig(chart3)
plt.close()

print("Charts Generated Successfully!")

# ==============================
# AUTOMATED TEXT REPORT
# ==============================

report_path = "reports/report.txt"

with open(report_path, "w") as report:

    report.write("DATA CLEANING & REPORTING AUTOMATION\n")
    report.write("====================================\n\n")

    report.write("PROJECT SUMMARY\n")
    report.write("--------------------------\n")

    report.write(f"Original Dataset Shape : {df.shape}\n")
    report.write(f"Duplicate Rows Removed : {duplicate_rows}\n")
    report.write(f"Missing Values Handled : {missing_values}\n\n")

    report.write("KPI SUMMARY\n")
    report.write("--------------------------\n")

    report.write(f"Total Sales      : ${total_sales:,.2f}\n")
    report.write(f"Total Profit     : ${total_profit:,.2f}\n")
    report.write(f"Total Orders     : {total_orders}\n")
    report.write(f"Top Category     : {top_category}\n")
    report.write(f"Top Sales Region : {top_region}\n\n")

    report.write("GENERATED FILES\n")
    report.write("--------------------------\n")

    report.write("1. cleaned_sales_data.csv\n")
    report.write("2. sales_by_category.png\n")
    report.write("3. monthly_sales_trend.png\n")
    report.write("4. profit_by_region.png\n")
    report.write("5. report.txt\n")

print(f"\nAutomated Report Generated:\n{report_path}")

# ==============================
# EXPORT SUMMARY TO EXCEL
# ==============================

summary_df = pd.DataFrame({
    'Metric': [
        'Total Sales',
        'Total Profit',
        'Total Orders',
        'Top Category',
        'Top Region'
    ],
    'Value': [
        total_sales,
        total_profit,
        total_orders,
        top_category,
        top_region
    ]
})

excel_report = "output/kpi_summary.xlsx"

summary_df.to_excel(excel_report, index=False)

print(f"\nExcel KPI Summary Saved To:\n{excel_report}")

# ==============================
# FINAL MESSAGE
# ==============================

print("\n===================================")
print("TASK COMPLETED SUCCESSFULLY!")
print("Data Cleaning & Reporting Automation Finished")
print("===================================")
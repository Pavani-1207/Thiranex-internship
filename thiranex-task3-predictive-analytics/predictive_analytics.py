import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import os

# ====================================
# CREATE FOLDERS
# ====================================

os.makedirs("output", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ====================================
# LOAD DATASET
# ====================================

print("Loading Walmart Sales Dataset...")

df = pd.read_csv("dataset/walmart_sales.csv")

print("\nDataset Loaded Successfully!")
print(f"Dataset Shape: {df.shape}")

# ====================================
# DATA PREPROCESSING
# ====================================

print("\nStarting Data Preprocessing...")

# Convert Date column
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

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

# Using Temperature, Fuel Price, CPI, Unemployment
# to predict Weekly Sales

X = df[['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']]
y = df['Weekly_Sales']

# ====================================
# TRAIN TEST SPLIT
# ====================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# ====================================
# TRAIN MODEL
# ====================================

print("\nTraining Predictive Model...")

model = LinearRegression()

model.fit(X_train, y_train)

print("Model Training Completed!")

# ====================================
# PREDICTIONS
# ====================================

y_pred = model.predict(X_test)

# ====================================
# MODEL EVALUATION
# ====================================

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n========== MODEL PERFORMANCE ==========")
print(f"Mean Absolute Error : {mae:,.2f}")
print(f"R2 Score            : {r2:.4f}")

# ====================================
# SAVE PREDICTIONS
# ====================================

predictions_df = pd.DataFrame({
    'Actual Sales': y_test.values,
    'Predicted Sales': y_pred
})

prediction_file = "output/sales_predictions.csv"

predictions_df.to_csv(prediction_file, index=False)

print(f"\nPredictions Saved To:\n{prediction_file}")

# ====================================
# VISUALIZATION
# ====================================

print("\nGenerating Prediction Graph...")

plt.figure(figsize=(10, 6))

plt.plot(y_test.values[:50], label='Actual Sales')
plt.plot(y_pred[:50], label='Predicted Sales')

plt.title('Actual vs Predicted Sales')
plt.xlabel('Sample Data')
plt.ylabel('Sales')
plt.legend()

chart_path = "reports/sales_forecast.png"

plt.tight_layout()
plt.savefig(chart_path)
plt.close()

print("Visualization Generated Successfully!")

# ====================================
# AUTOMATED REPORT
# ====================================

report_path = "reports/report.txt"

with open(report_path, "w") as report:

    report.write("PREDICTIVE ANALYTICS USING HISTORICAL DATA\n")
    report.write("==========================================\n\n")

    report.write("PROJECT SUMMARY\n")
    report.write("--------------------------\n")

    report.write(f"Dataset Shape           : {df.shape}\n")
    report.write(f"Duplicate Rows Removed  : {duplicates}\n")
    report.write(f"Missing Values Handled  : {missing_values}\n\n")

    report.write("MODEL PERFORMANCE\n")
    report.write("--------------------------\n")

    report.write(f"Mean Absolute Error : {mae:,.2f}\n")
    report.write(f"R2 Score            : {r2:.4f}\n\n")

    report.write("FILES GENERATED\n")
    report.write("--------------------------\n")

    report.write("1. sales_predictions.csv\n")
    report.write("2. sales_forecast.png\n")
    report.write("3. report.txt\n")

print(f"\nAutomated Report Generated:\n{report_path}")

# ====================================
# EXPORT MODEL SUMMARY
# ====================================

summary_df = pd.DataFrame({
    'Metric': [
        'Mean Absolute Error',
        'R2 Score'
    ],
    'Value': [
        mae,
        r2
    ]
})

excel_path = "output/model_summary.xlsx"

summary_df.to_excel(excel_path, index=False)

print(f"\nModel Summary Saved To:\n{excel_path}")

# ====================================
# FINAL MESSAGE
# ====================================

print("\n===================================")
print("TASK COMPLETED SUCCESSFULLY!")
print("Predictive Analytics Project Finished")
print("===================================")
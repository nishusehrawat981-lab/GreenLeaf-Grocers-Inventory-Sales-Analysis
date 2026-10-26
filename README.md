# GreenLeaf Grocers — Inventory & Sales Management System

## Project overview
This beginner-friendly Python data analytics project explores retail sales and inventory for a fictional grocery business, GreenLeaf Grocers. It is designed to support an analytics dashboard showing revenue, units sold, category performance, regional performance, and low-stock items.

## Important note about the dataset
The screenshot provided contains the project brief, but it does not include the actual dataset file. Therefore, `GreenLeaf_Grocers_Sample_Dataset.csv` is a **synthetic practice dataset created for this submission package**. It is not official company data. If your instructor provided a separate CSV, use that file instead and adjust column names in your analysis.

## Files
- `GreenLeaf_Grocers_Sample_Dataset.csv` — 240 sample order records.
- `GreenLeaf_Grocers_Project_Report.pdf` — short project introduction, dataset details, objectives, and explanation.
- `README.md` — project notes and suggested workflow.

## Dataset columns
- `Order_ID`: unique order record identifier
- `Order_Date`: date of the order (YYYY-MM-DD)
- `Product_ID`, `Product_Name`: product identifiers and names
- `Category`: grocery product category
- `Units_Sold`: quantity sold in the order record
- `Unit_Price_INR`: price per unit in Indian rupees
- `Revenue_INR`: `Units_Sold × Unit_Price_INR`
- `Opening_Stock`: stock quantity before the recorded sale (sampled)
- `Reorder_Level`: stock threshold used to flag replenishment
- `Closing_Stock`: estimated remaining stock after the sale and a small adjustment
- `Supplier`: supplier label
- `Region`: sales region label

## Suggested analysis
1. Load the CSV with pandas.
2. Check missing values and duplicate order IDs.
3. Convert `Order_Date` to a datetime column.
4. Calculate total revenue, total units sold, average order revenue, and revenue by category.
5. Compare revenue by month and region.
6. Flag records where `Closing_Stock <= Reorder_Level`.
7. Build charts and an interactive dashboard using Plotly or Power BI.

## Example Python starter code
```python
import pandas as pd

df = pd.read_csv("GreenLeaf_Grocers_Sample_Dataset.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

print("Rows and columns:", df.shape)
print("Total revenue (INR):", df["Revenue_INR"].sum())
print("Units sold:", df["Units_Sold"].sum())

category_sales = df.groupby("Category")["Revenue_INR"].sum().sort_values(ascending=False)
print(category_sales)

low_stock = df[df["Closing_Stock"] <= df["Reorder_Level"]]
print("Low-stock records:", len(low_stock))
```

## Limitations
This dataset is synthetic and suitable for demonstrating analysis methods only. Stock values are illustrative, not a real stock ledger. Do not present the figures as actual GreenLeaf Grocers business results.

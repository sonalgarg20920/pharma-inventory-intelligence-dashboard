import pandas as pd

# Read inventory file
df = pd.read_excel(
    "../Stock_Detail.xls",
    header=8
)

# Clean column names
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Keep only products with stock value > 0
df = df[
    df["stock_value"] > 0
]

# Calculate product inventory value
df = df[
    df["nametodisplay"].notna()
]

df = df[
    ~df["nametodisplay"]
    .astype(str)
    .str.upper()
    .eq("GRAND TOTAL")
]


top_products = (
    df.groupby("nametodisplay")["stock_value"]
    .sum()
    .sort_values(ascending=False)
    .head(521)
    .reset_index()
)

top_products.columns = [
    "product_name",
    "inventory_value"
]

# Save CSV
top_products.to_csv(
    "top_521_products.csv",
    index=False
)

print(
    f"Created top_521_products.csv with {len(top_products)} products"
)

print("\nTop 10 Products:\n")

print(
    top_products.head(10)
)
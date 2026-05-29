# Pharma Inventory Intelligence Dashboard

An interactive inventory analytics dashboard built using Streamlit, 
Pandas, and Plotly to monitor inventory health, identify expiry risk, and 
support proactive inventory management decisions.

---

## Business Problem

Pharmaceutical inventory often contains products approaching expiry, 
creating financial risk through product write-offs and inventory wastage.

This dashboard provides visibility into inventory at risk by segmenting 
products based on expiry timelines and enabling users to drill down into 
inventory details using interactive filters.

---

## Features

### KPI Monitoring

* Total Inventory Value
* Risk Inventory Value (Products expiring within 60 days)
* Risk Inventory Percentage

### Expiry Risk Analysis

* Inventory segmentation by expiry window:

  * <30 Days
  * 30-60 Days
  * 60-90 Days
  * 90-120 Days
  * 120-150 Days
  * 150+ Days

### Marketing Group Risk Analysis

* Identify marketing groups contributing most to near-expiry inventory.

### Inventory Product Explorer

Interactive filters for:

* Expiry Bucket
* Marketing Group
* Category
* Days to Expiry
* Stock Value
* Stock Quantity

Additional functionality:

* Product Search
* CSV Export

---

## Dashboard Screenshots

### KPI Overview

![KPI Dashboard](screenshots/kpis.png)

### Inventory Distribution by Expiry Window

![Inventory 
Distribution](screenshots/inventory_distribution_by_expiry_window.png)

### Product Explorer

![Product Explorer](screenshots/inventory_product_explorer.png)

### Top Marketing Groups at Risk

![Marketing Group Risk](screenshots/top_marketing_group_atrisk.png)

---

## Technology Stack

* Python
* Pandas
* Streamlit
* Plotly
* OpenPyXL
* XLRD

---

## Data Processing Workflow

1. Load inventory report
2. Clean and standardize columns
3. Calculate Days to Expiry
4. Remove expired and zero-value inventory
5. Create Expiry Buckets
6. Calculate Risk KPIs
7. Visualize inventory risk
8. Enable interactive inventory exploration

---

## Project Structure

```text
pharma-inventory-intelligence-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── screenshots/
│   ├── kpis.png
│   ├── inventory_distribution_by_expiry_window.png
│   ├── inventory_product_explorer.png
│   └── top_marketing_group_atrisk.png
└── .gitignore
```

---

## Future Enhancements

### Version 2

* Gmail API Integration
* Automatic retrieval of latest inventory report
* One-click inventory refresh

### Version 3

* Expiry Forecasting
* Automated Alerts
* Reorder Recommendations
* AI-Generated Inventory Insights

---

## Author

Sonal Garg

Data Analytics | Business Intelligence | Inventory Analytics


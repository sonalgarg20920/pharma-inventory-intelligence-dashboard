import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Pharma Inventory Dashboard",
    layout="wide"
)

st.title("Pharma Inventory Intelligence Dashboard")

# Load data
df = pd.read_excel(
    "Stock_Detail.xls",
    header=8
)

# Clean columns
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace("/", "_", regex=False)
    .str.replace("'", "", regex=False)
)

# Convert expiry date
df['expirydate'] = pd.to_datetime(
    df['expirydate'],
    errors='coerce'
)

# Days to expiry
today = pd.Timestamp.today()

df['days_to_expiry'] = (
    df['expirydate'] - today
).dt.days

# Remove invalid records
df = df[
    (df['stock_value'] > 0) &
    (df['days_to_expiry'] >= 0)
]

# Expiry bucket
def expiry_bucket(days):

    if days < 30:
        return "<30 Days"

    elif days < 60:
        return "30-60 Days"

    elif days < 90:
        return "60-90 Days"

    elif days < 120:
        return "90-120 Days"

    elif days < 150:
        return "120-150 Days"

    else:
        return "150+ Days"

df['expiry_bucket'] = df['days_to_expiry'].apply(expiry_bucket)

st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox(
    "Select Company",
    ['All'] + list(df['marketing_group'].dropna().unique())
)

if selected_category != 'All':
    df = df[
        df['marketing_group'] == selected_category
    ]

# KPI calculations
total_inventory = df['stock_value'].sum()

risk_inventory = df[
    df['expiry_bucket'].isin(
        ['<30 Days', '30-60 Days']
    )
]['stock_value'].sum()

critical_pct = (
    risk_inventory / total_inventory
) * 100


# KPI cards
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Inventory Value",
    f"₹{total_inventory:,.0f}"
)

col2.metric(
    "Risk Inventory Value",
    f"₹{risk_inventory:,.0f}",
    help="Includes inventory expiring within 60 days"
)

col3.metric(
    "Risk Inventory %",
    f"{critical_pct:.2f}%",
    help="Includes inventory expiring within 60 days"
)



st.subheader("Risk Distribution")

risk_df = (
    df.groupby('expiry_bucket')['stock_value']
    .sum()
    .reset_index()
)

risk_df.columns = [
    'Expiry Bucket',
    'Inventory Value'
]

# Convert to percentage
risk_df['Percentage'] = (
    risk_df['Inventory Value']
    /
    risk_df['Inventory Value'].sum()
) * 100

# Sort bucket order
bucket_order = [
    '<30 Days',
    '30-60 Days',
    '60-90 Days',
    '90-120 Days',
    '120-150 Days',
    '150+ Days'
]

risk_df['Expiry Bucket'] = pd.Categorical(
    risk_df['Expiry Bucket'],
    categories=bucket_order,
    ordered=True
)

risk_df = risk_df.sort_values(
    'Expiry Bucket'
)

fig = px.bar(
    risk_df,
    x='Percentage',
    y='Expiry Bucket',
    orientation='h',
    text=risk_df['Percentage'].apply(
        lambda x: f"{x:.1f}%"
    ),
    title='Inventory Distribution by Expiry Window'
)

fig.update_traces(
    textposition='outside'
)

fig.update_layout(
    xaxis_title='Percentage of Inventory Value',
    yaxis_title='Expiry Window'
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Inventory Product Explorer")

# =========================
# =========================
# FILTER SECTION
# =========================

col1, col2, col3 = st.columns(3)

# Expiry Bucket Filter
selected_buckets = col1.multiselect(
    "Select Expiry Bucket",
    options=[
        '<30 Days',
        '30-60 Days',
        '60-90 Days',
        '90-120 Days',
        '120-150 Days',
        '150+ Days'
    ],
    default=[]
)

# Marketing Group Filter
selected_groups = col2.multiselect(
    "Select Marketing Group",
    options=sorted(
        df['marketing_group']
        .dropna()
        .unique()
    ),
    default=[]
)

# Category Filter
selected_categories = col3.multiselect(
    "Select Category",
    options=sorted(
        df['category']
        .dropna()
        .unique()
    ),
    default=[]
)

# =========================
# SLIDER FILTERS
# =========================

days_range = st.slider(
    "Select Days to Expiry Range",
    min_value=int(df['days_to_expiry'].min()),
    max_value=int(df['days_to_expiry'].max()),
    value=(
        int(df['days_to_expiry'].min()),
        int(df['days_to_expiry'].max())
    )
)

stock_value_range = st.slider(
    "Select Stock Value Range",
    min_value=int(df['stock_value'].min()),
    max_value=int(df['stock_value'].max()),
    value=(
        int(df['stock_value'].min()),
        int(df['stock_value'].max())
    )
)

stock_range = st.slider(
    "Select Stock Range",
    min_value=int(df['stock'].min()),
    max_value=int(df['stock'].max()),
    value=(
        int(df['stock'].min()),
        int(df['stock'].max())
    )
)

# =========================
# START WITH FULL DATA
# =========================

filtered_products = df.copy()

# =========================
# APPLY FILTERS ONLY IF USED
# =========================

if selected_buckets:
    filtered_products = filtered_products[
        filtered_products['expiry_bucket']
        .isin(selected_buckets)
    ]

if selected_groups:
    filtered_products = filtered_products[
        filtered_products['marketing_group']
        .isin(selected_groups)
    ]

if selected_categories:
    filtered_products = filtered_products[
        filtered_products['category']
        .isin(selected_categories)
    ]

# Numeric filters
filtered_products = filtered_products[
    (
        filtered_products['days_to_expiry']
        .between(days_range[0], days_range[1])
    )
    &
    (
        filtered_products['stock_value']
        .between(
            stock_value_range[0],
            stock_value_range[1]
        )
    )
    &
    (
        filtered_products['stock']
        .between(
            stock_range[0],
            stock_range[1]
        )
    )
]
search_term = st.text_input(
    "Search Product Name"
)

if search_term:
    filtered_products = filtered_products[
        filtered_products['nametodisplay']
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]
# =========================
# SORT DATA
# =========================

filtered_products = filtered_products.sort_values(
    by='stock_value',
    ascending=False
)

# =========================
# DOWNLOAD BUTTON
# =========================

csv = filtered_products.to_csv(
    index=False
)

st.download_button(
    label="Download Filtered Inventory",
    data=csv,
    file_name='filtered_inventory.csv',
    mime='text/csv'
)

# =========================
# RECORD COUNT
# =========================

st.write(
    f"Showing {len(filtered_products)} products"
)

# =========================
# DISPLAY TABLE
# =========================

st.dataframe(
    filtered_products[
        [
            'nametodisplay',
            'marketing_group',
            'category',
            'stock',
            'stock_value',
            'days_to_expiry',
            'expiry_bucket'
        ]
    ]
)
st.subheader("Top Marketing Groups at Risk")

risk_products = df[
    df['expiry_bucket'].isin(
        ['<30 Days', '30-60 Days']
    )
]

group_risk = (
    risk_products
    .groupby('marketing_group')['stock_value']
    .sum()
)

group_risk = (
    group_risk / group_risk.sum()
) * 100

group_risk = group_risk.sort_values(
    ascending=True
).tail(10)

group_df = group_risk.reset_index()

group_df.columns = [
    'Marketing Group',
    'Percentage'
]

fig_group = px.bar(
    group_df,
    x='Percentage',
    y='Marketing Group',
    orientation='h',
    text=group_df['Percentage'].apply(
        lambda x: f"{x:.1f}%"
    ),
    title='Top Marketing Group Contribution to Risk Inventory'
)

fig_group.update_traces(
    textposition='outside'
)

fig_group.update_layout(
    xaxis_title='Percentage Contribution',
    yaxis_title='Marketing Group'
)

st.plotly_chart(
    fig_group,
    use_container_width=True
)
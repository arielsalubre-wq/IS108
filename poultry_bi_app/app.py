import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Poultry BI Dashboard", layout="wide")
st.title("🐔 Poultry Production & Dressing BI Dashboard")
st.markdown("### Final Project: Business Intelligence Analysis")
st.markdown("---")

# --- 2. ETL: DATA LOADING & CLEANING ---
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("poultry_bi_app/Prod_cleaned.csv")
    
    # Strip whitespace from headers
    df.columns = df.columns.str.strip()
    
    # Handle missing/invalid values
    df.replace({'#DIV/0!': np.nan, '-': np.nan}, inplace=True)
    df.dropna(subset=['Farm'], inplace=True)
    
    # Date formatting
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Clean numeric columns (Remove commas, convert to float)
    num_cols = ['ALW', 'Dressing_Volume_hds', 'Dressing Volume (KG)']
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Clean percentage columns
    pct_cols = [c for c in df.columns if '%' in c or 'Yield' in c or 'Recovery' in c]
    for col in pct_cols:
        df[col] = df[col].astype(str).str.replace('%', '', regex=False).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce') / 100
        
    return df

df = load_and_clean_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
farm_filter = st.sidebar.multiselect("Select Farm(s)", options=sorted(df['Farm'].unique()), default=df['Farm'].unique())
filtered_df = df[df['Farm'].isin(farm_filter)]

# --- 4. KEY PERFORMANCE INDICATORS (KPIs) ---
st.header("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_kg = filtered_df['Dressing Volume (KG)'].sum()
avg_alw = filtered_df['ALW'].mean()
avg_carcass = filtered_df['Carcass Yield (77.49%)'].mean() * 100
avg_invoice = filtered_df['Invoice Yield (74%)'].mean() * 100

col1.metric("Total Volume (KG)", f"{total_kg:,.0f}")
col2.metric("Avg ALW", f"{avg_alw:.2f}")
col3.metric("Avg Carcass Yield", f"{avg_carcass:.2f}%")
col4.metric("Avg Invoice Yield", f"{avg_invoice:.2f}%")

st.markdown("---")

# --- 5. VISUALIZATIONS ---
st.header("Analytical Insights")

# Row 1: Trends and Volume
c1, c2 = st.columns(2)
with c1:
    st.subheader("Daily Production Trend")
    trend = filtered_df.groupby('Date')['Dressing Volume (KG)'].sum().reset_index()
    fig1 = px.line(trend, x='Date', y='Dressing Volume (KG)', markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Total Volume by Farm")
    farm_vol = filtered_df.groupby('Farm')['Dressing Volume (KG)'].sum().reset_index()
    fig2 = px.bar(farm_vol, x='Farm', y='Dressing Volume (KG)', color='Farm')
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Yield Analysis
c3, c4 = st.columns(2)
with c3:
    st.subheader("Yield Efficiency Comparison")
    yields = filtered_df.groupby('Farm')[['Carcass Yield (77.49%)', 'Invoice Yield (74%)']].mean().reset_index()
    fig3 = px.bar(yields.melt(id_vars='Farm'), x='Farm', y='value', color='variable', barmode='group')
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("ALW vs. Yield Correlation")
    fig4 = px.scatter(filtered_df, x='ALW', y='Carcass Yield (77.49%)', color='Farm', trendline="ols")
    st.plotly_chart(fig4, use_container_width=True)

# --- 6. DATA TABLE ---
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))
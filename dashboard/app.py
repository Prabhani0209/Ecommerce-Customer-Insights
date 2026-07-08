import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="E-commerce Customer Insights",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Maximum Readability & Large Font CSS Theme
# -----------------------------
st.markdown("""
<style>
    /* Premium background tint */
    .stApp {
        background-color: #F4F6F9;
    }
    
    /* CRITICAL FIX: Constrains dashboard width to stop charts from flattening on ultra-wide screens */
    .block-container {
        max-width: 1100px !important;
        padding-top: 40px !important;
        padding-bottom: 60px !important;
    }
    
    /* High contrast, large scale typography */
    h1 { font-size: 52px !important; font-weight: 800; color: #1E293B; margin-bottom: 5px; }
    h2 { font-weight: 700; color: #1E293B; font-size: 34px !important; margin-top: 15px !important; margin-bottom: 25px !important; }
    p, .stMarkdown { font-size: 22px !important; color: #475569; line-height: 1.6; }

    /* Massive, legible metric cards */
    .kpi-card {
        background-color: #FFFFFF;
        padding: 30px 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #EAEFF4;
        text-align: center;
        margin-bottom: 20px;
    }
    .kpi-label {
        color: #64748B;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        color: #0F172A;
        font-size: 36px;
        font-weight: 800;
    }
    
    /* Thick padded containers to push charts vertically */
    .chart-container {
        background-color: #FFFFFF;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        border: 1px solid #EAEFF4;
    }
    
    /* Huge separator spaces to guarantee an active scroll wheel experience */
    .section-space {
        margin-bottom: 80px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Project Path & Load Data
# -----------------------------
project_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
cleaned_file = os.path.join(project_path, "data", "cleaned_online_retail.csv")
segment_file = os.path.join(project_path, "data", "final_customer_segments.csv")

@st.cache_data
def load_and_process_data():
    df_data = pd.read_csv(cleaned_file)
    df_seg = pd.read_csv(segment_file)
    
    df_data["InvoiceDate"] = pd.to_datetime(df_data["InvoiceDate"])
    df_data["Revenue"] = df_data["Quantity"] * df_data["Price"]
    df_data["Month"] = df_data["InvoiceDate"].dt.to_period("M").astype(str)
    
    return df_data, df_seg

try:
    data, segments = load_and_process_data()
except Exception as e:
    st.error(f"Error loading dashboard source files: {e}")
    st.stop()

# -----------------------------
# Title Header
# -----------------------------
st.markdown("<h1>Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p>This dashboard analyzes customer purchasing behavior, sales trends, and customer segments using Machine Learning.</p>", unsafe_allow_html=True)
st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

# -----------------------------
# KPI Section (Stacked clean boxes)
# -----------------------------
total_revenue = data["Revenue"].sum()
total_orders = data["Invoice"].nunique()
total_customers = data["Customer ID"].nunique()
total_products = data["StockCode"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Total Revenue</div><div class="kpi-value">₹{total_revenue:,.0f}</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Total Orders</div><div class="kpi-value">{total_orders:,}</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Total Customers</div><div class="kpi-value">{total_customers:,}</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Unique Products</div><div class="kpi-value">{total_products:,}</div></div>""", unsafe_allow_html=True)

st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

# -----------------------------
# 1. Monthly Revenue Trend (Gradient Area Style)
# -----------------------------
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("<h2>Payments Overview (Monthly Trend)</h2>", unsafe_allow_html=True)

monthly_sales = data.groupby("Month")["Revenue"].sum().reset_index()

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=monthly_sales["Month"], 
    y=monthly_sales["Revenue"],
    mode='lines+markers',
    line=dict(color='#6366F1', width=5), 
    marker=dict(size=10, color='#6366F1'),
    fill='tozeroy',
    fillcolor='rgba(99, 102, 241, 0.08)', 
    name="Revenue"
))

fig_trend.update_layout(
    template="plotly_white",
    # Fixed: Removed 'intensity' property and used standard typography sizes instead
    xaxis=dict(showgrid=False, tickfont=dict(color='#1E293B', size=20)),
    yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#1E293B', size=20)),
    margin=dict(l=20, r=20, t=20, b=20),
    height=600  
)
st.plotly_chart(fig_trend, width="stretch")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

# -----------------------------
# 2. Top 10 Selling Products (Clean Sky Blue Bars)
# -----------------------------
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("<h2>Top 10 Selling Products</h2>", unsafe_allow_html=True)

top_products = (
    data.groupby("Description")["Quantity"]
    .sum().reset_index()
    .sort_values(by="Quantity", ascending=False).head(10)
)

fig_prod = px.bar(
    top_products, x="Quantity", y="Description",
    orientation='h', template="plotly_white"
)
fig_prod.update_traces(marker_color="#00D2FF", marker_line_width=0)
fig_prod.update_layout(
    yaxis={'categoryorder':'total ascending', 'tickfont': dict(color='#1E293B', size=18)},
    xaxis={'tickfont': dict(color='#1E293B', size=20), 'gridcolor': '#F1F5F9'},
    margin=dict(l=20, r=20, t=20, b=20), 
    height=650
)
st.plotly_chart(fig_prod, width="stretch")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

# -----------------------------
# 3. Customer Segments (Sleek Columns)
# -----------------------------
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("<h2>Profit This Week (Customer Segments)</h2>", unsafe_allow_html=True)

segment_count = segments["Customer Segment"].value_counts().reset_index()
segment_count.columns = ["Segment", "Count"]

fig_seg = px.bar(
    segment_count, x="Segment", y="Count",
    template="plotly_white"
)
fig_seg.update_traces(marker_color="#0066FF")
fig_seg.update_layout(
    showlegend=False, 
    xaxis={'tickfont': dict(color='#1E293B', size=22)},
    yaxis={'gridcolor': '#F1F5F9', 'tickfont': dict(color='#1E293B', size=20)},
    margin=dict(l=20, r=20, t=20, b=20), 
    height=600
)
st.plotly_chart(fig_seg, width="stretch")
st.markdown('</div>', unsafe_allow_html=True)

st.toast("Dashboard optimized for widescreen scrolling layout!", icon="🎯")

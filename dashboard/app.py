import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================================================================
# 1. GLOBAL LAYOUT CONFIGURATION & THEME
# ==============================================================================

st.set_page_config(
    page_title="Global E-Commerce Enterprise Intelligence",
    page_icon="🛍️",
    layout="wide"
)

# Premium dashboard styling
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.stMetric {
    background-color: #ffffff;
    padding: 1.25rem;
    border-radius: 12px;
    border: 1px solid #e6e9ef;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. FILE PATH CONFIGURATION
# ==============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATH_CLEANED = os.path.join(
    BASE_DIR,
    "data",
    "cleaned_online_retail.csv"
)

PATH_SEGMENT = os.path.join(
    BASE_DIR,
    "data",
    "final_customer_segments.csv"
)


# ==============================================================================
# 3. DATA LOADING FUNCTION
# ==============================================================================

@st.cache_data
def load_and_standardize_data():

    sales_data = pd.read_csv(PATH_CLEANED)

    segment_data = pd.read_csv(PATH_SEGMENT)


    # Remove unwanted spaces in column names

    sales_data.columns = [
        col.strip()
        for col in sales_data.columns
    ]

    segment_data.columns = [
        col.strip()
        for col in segment_data.columns
    ]


    # Detect Date Column

    date_col = next(
        (
            c for c in sales_data.columns
            if c.lower() in [
                "invoicedate",
                "invoice date",
                "date"
            ]
        ),
        None
    )


    if date_col:

        sales_data["InvoiceDate"] = pd.to_datetime(
            sales_data[date_col]
        )

        sales_data["Month"] = (
            sales_data["InvoiceDate"]
            .dt.to_period("M")
            .astype(str)
        )

    else:

        sales_data["Month"] = "Unknown"



    # Detect Quantity Column

    qty_col = next(
        (
            c for c in sales_data.columns
            if c.lower() in [
                "quantity",
                "qty"
            ]
        ),
        None
    )


    # Detect Price Column

    price_col = next(
        (
            c for c in sales_data.columns
            if c.lower() in [
                "price",
                "unitprice",
                "unit_price"
            ]
        ),
        None
    )


    # Create Revenue Column

    if "Revenue" not in sales_data.columns:

        if qty_col and price_col:

            sales_data["Revenue"] = (
                sales_data[qty_col] *
                sales_data[price_col]
            )

        else:

            sales_data["Revenue"] = 0



    return sales_data, segment_data



# ==============================================================================
# 4. START APPLICATION
# ==============================================================================

try:

    df_sales, df_seg = load_and_standardize_data()


except Exception as error:

    st.error(
        f"❌ Data loading failed: {error}"
    )

    st.stop()
    # ==============================================================================
# 5. SIDEBAR CONTROL PANEL
# ==============================================================================

st.sidebar.title("🏙️ Business Intelligence Suite")

st.sidebar.markdown("---")


app_route = st.sidebar.radio(
    "Select Dashboard View:",
    [
        "📊 Executive Performance Summary",
        "📈 Commercial Sales & Product Trends",
        "👥 AI Customer Behavioral Clustering"
    ]
)


st.sidebar.markdown("---")

st.sidebar.subheader("🌍 Market Filter")


if "Country" in df_sales.columns:

    country_list = sorted(
        df_sales["Country"]
        .dropna()
        .unique()
        .tolist()
    )


    selected_country = st.sidebar.multiselect(
        "Choose Countries",
        country_list,
        default=country_list[:5]
    )


    df_filtered = df_sales[
        df_sales["Country"]
        .isin(selected_country)
    ]


else:

    df_filtered = df_sales.copy()



# ==============================================================================
# 6. EXECUTIVE PERFORMANCE DASHBOARD
# ==============================================================================

if app_route == "📊 Executive Performance Summary":


    st.title(
        "📊 Executive Performance Summary"
    )

    st.write(
        "Real-time business KPIs extracted from customer transaction data."
    )

    st.divider()



    invoice_col = next(
        (
            c for c in df_filtered.columns
            if c.lower() in [
                "invoiceno",
                "invoice",
                "invoice_no",
                "invoicenumber"
            ]
        ),
        None
    )


    customer_col = next(
        (
            c for c in df_filtered.columns
            if c.lower() in [
                "customerid",
                "customer_id",
                "customer id"
            ]
        ),
        None
    )


    product_col = next(
        (
            c for c in df_filtered.columns
            if c.lower() in [
                "description",
                "product_description",
                "item"
            ]
        ),
        None
    )



    revenue = df_filtered["Revenue"].sum()


    orders = (
        df_filtered[invoice_col]
        .nunique()
        if invoice_col else 0
    )


    customers = (
        df_filtered[customer_col]
        .nunique()
        if customer_col else 0
    )


    products = (
        df_filtered[product_col]
        .nunique()
        if product_col else 0
    )



    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "💰 Total Revenue",
        f"${revenue:,.2f}"
    )


    col2.metric(
        "🧾 Total Orders",
        f"{orders:,}"
    )


    col3.metric(
        "👥 Customers",
        f"{customers:,}"
    )


    col4.metric(
        "📦 Products",
        f"{products:,}"
    )



    st.subheader(
        "📋 Transaction Explorer"
    )


    st.dataframe(
        df_filtered.head(500),
        use_container_width=True
    )





# ==============================================================================
# 7. SALES AND PRODUCT ANALYTICS
# ==============================================================================


elif app_route == "📈 Commercial Sales & Product Trends":


    st.title(
        "📈 Commercial Sales & Product Trends"
    )


    st.write(
        "Analyze revenue movement and best performing products."
    )


    st.divider()



    left, right = st.columns(2)



    # Revenue Trend

    with left:


        st.subheader(
            "📅 Monthly Revenue Trend"
        )


        if "Month" in df_filtered.columns:


            monthly_sales = (
                df_filtered
                .groupby("Month")["Revenue"]
                .sum()
                .reset_index()
            )


            revenue_chart = px.line(
                monthly_sales,
                x="Month",
                y="Revenue",
                markers=True,
                template="plotly_white",
                title="Revenue Growth Over Time"
            )


            revenue_chart.update_traces(
                line_width=3
            )


            st.plotly_chart(
                revenue_chart,
                use_container_width=True
            )


        else:

            st.warning(
                "Date information unavailable."
            )



    # Product Ranking


    with right:


        st.subheader(
            "🏆 Top Selling Products"
        )


        product_col = next(
            (
                c for c in df_filtered.columns
                if c.lower() in [
                    "description",
                    "product_description",
                    "item"
                ]
            ),
            None
        )


        qty_col = next(
            (
                c for c in df_filtered.columns
                if c.lower() in [
                    "quantity",
                    "qty"
                ]
            ),
            None
        )


        if product_col and qty_col:


            top_products = (
                df_filtered
                .groupby(product_col)[qty_col]
                .sum()
                .sort_values(
                    ascending=False
                )
                .head(10)
                .reset_index()
            )


            product_chart = px.bar(
                top_products,
                x=qty_col,
                y=product_col,
                orientation="h",
                template="plotly_white"
            )


            product_chart.update_layout(
                yaxis={
                    "categoryorder":
                    "total ascending"
                }
            )


            st.plotly_chart(
                product_chart,
                use_container_width=True
            )


        else:

            st.warning(
                "Product information unavailable."
            )
            # ==============================================================================
# 8. AI CUSTOMER BEHAVIORAL CLUSTERING
# ==============================================================================

elif app_route == "👥 AI Customer Behavioral Clustering":

    st.title(
        "👥 AI Customer Behavioral Clustering"
    )

    st.write(
        "Machine Learning based customer segmentation using RFM analysis."
    )

    st.divider()



    left, right = st.columns(2)



    # Detect required clustering columns

    recency_col = next(
        (
            c for c in df_seg.columns
            if c.lower() in [
                "recency",
                "recency_score"
            ]
        ),
        None
    )


    monetary_col = next(
        (
            c for c in df_seg.columns
            if c.lower() in [
                "monetary",
                "monetary_value",
                "monetary_score"
            ]
        ),
        None
    )


    cluster_col = next(
        (
            c for c in df_seg.columns
            if c.lower() in [
                "cluster",
                "segment",
                "segments"
            ]
        ),
        None
    )


    customer_col = next(
        (
            c for c in df_seg.columns
            if c.lower() in [
                "customerid",
                "customer_id"
            ]
        ),
        None
    )



    # --------------------------------------------------------------------------
    # Scatter Plot
    # --------------------------------------------------------------------------

    with left:

        st.subheader(
            "🎯 Customer Cluster Map"
        )


        if recency_col and monetary_col and cluster_col:


            df_seg[cluster_col] = (
                df_seg[cluster_col]
                .astype(str)
            )


            hover = (
                [customer_col]
                if customer_col
                else None
            )


            cluster_chart = px.scatter(

                df_seg,

                x=recency_col,

                y=monetary_col,

                color=cluster_col,

                log_y=True,

                hover_data=hover,

                title="K-Means Customer Segmentation",

                labels={

                    recency_col:
                    "Recency (Days)",


                    monetary_col:
                    "Monetary Value ($)",


                    cluster_col:
                    "Customer Cluster"

                },

                template="plotly_white",

                color_discrete_sequence=
                px.colors.qualitative.Safe
            )



            cluster_chart.update_traces(

                marker=dict(

                    size=10,

                    opacity=0.75

                )

            )



            st.plotly_chart(

                cluster_chart,

                use_container_width=True

            )


        else:


            st.warning(

                "Cluster mapping requires Recency, Monetary and Cluster columns."

            )



    # --------------------------------------------------------------------------
    # Cluster Distribution
    # --------------------------------------------------------------------------

    with right:


        st.subheader(
            "📊 Cluster Distribution"
        )


        if cluster_col:


            cluster_count = (

                df_seg[cluster_col]

                .value_counts()

                .reset_index()

            )


            cluster_count.columns = [

                "Cluster",

                "Customers"

            ]



            st.dataframe(

                cluster_count,

                use_container_width=True

            )



            pie = px.pie(

                cluster_count,

                names="Cluster",

                values="Customers",

                title="Customer Segment Share",

                template="plotly_white",

                color_discrete_sequence=
                px.colors.qualitative.Safe

            )



            st.plotly_chart(

                pie,

                use_container_width=True

            )



        else:


            st.warning(

                "Cluster column not detected."

            )





# ==============================================================================
# FOOTER
# ==============================================================================

st.divider()


st.markdown(

"""

<center>

<h4>
🛍️ Global E-Commerce Enterprise Intelligence Dashboard
</h4>

<p>
Built using Python | Pandas | Plotly | Streamlit
</p>

</center>

""",

unsafe_allow_html=True

)
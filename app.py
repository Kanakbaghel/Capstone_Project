"""
RetailSmart Analytics Dashboard
================================
Interactive Streamlit dashboard using REAL project data and trained models.
Author: Kanak Baghel
License: Apache 2.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ========================
# PAGE CONFIGURATION
# ========================
st.set_page_config(
    page_title="RetailSmart Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# CUSTOM CSS
# ========================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
    }
    .insight-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========================
# DATA LOADING FUNCTIONS
# ========================
@st.cache_data
def load_cleaned_data():
    """Load cleaned datasets from Phase 1"""
    try:
        # Try Phase 1 cleaned files first
        customers = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-1/Cleaned Files/customers_cleaned.csv')
        sales = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-1/Cleaned Files/sales_cleaned.csv')
        products = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-1/Cleaned Files/products_cleaned.csv')
        marketing = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-1/Cleaned Files/marketing_cleaned.csv')
        reviews = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-1/Cleaned Files/reviews_cleaned.csv')
        
        return customers, sales, products, marketing, reviews, "Phase 1 Cleaned Data"
    except Exception as e1:
        try:
            # Fallback to raw Datasets folder
            customers = pd.read_csv('/workspaces/Capstone_Project/Datasets/customers.csv')
            sales = pd.read_csv('/workspaces/Capstone_Project/Datasets/sales.csv')
            products = pd.read_csv('/workspaces/Capstone_Project/Datasets/products.csv')
            marketing = pd.read_csv('/workspaces/Capstone_Project/Datasets/marketing.csv')
            reviews = pd.read_csv('/workspaces/Capstone_Project/Datasets/reviews.csv')
            
            return customers, sales, products, marketing, reviews, "Raw Dataset Files"
        except Exception as e2:
            st.error(f"❌ Could not load data files!\n\nTried:\n1. Exported_files/Phase1/\n2. Datasets/\n\nError: {str(e2)}")
            return None, None, None, None, None, None

@st.cache_data
def load_model_predictions():
    """Load Phase 2 model predictions and results"""
    try:
        # Load churn predictions
        churn_pred = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-2/Models/best_churn_model.pkl')
        
        # Load model input with features
        model_input = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-2/data cleaned/model_input.csv')
        
        return churn_pred, model_input, True
    except Exception as e:
        st.warning(f"⚠️ Phase 2 predictions not found: {str(e)}")
        return None, None, False

@st.cache_resource
def load_trained_model():
    """Load trained ML model from Phase 2"""
    try:
        with open('/workspaces/Capstone_Project/Exported_files/Phase-2/Models/clv_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open('/workspaces/Capstone_Project/Exported_files/Phase-2/Models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
            
        return model, scaler, True
    except Exception as e:
        st.warning(f"⚠️ Trained model not found: {str(e)}")
        return None, None, False

@st.cache_data
def load_clustering_results():
    """Load Phase 3 clustering and segmentation"""
    try:
        cluster_summary = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-3/data outputs/cluster_summary.csv')
        customers_clustered = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-3/data outputs/customers_with_clusters.csv')
        
        return cluster_summary, customers_clustered, True
    except Exception as e:
        st.warning(f"⚠️ Phase 3 clustering not found: {str(e)}")
        return None, None, False

@st.cache_data
def load_forecast_results():
    """Load Phase 3 demand forecasting results"""
    try:
        forecast = pd.read_csv('/workspaces/Capstone_Project/Exported_files/Phase-3/data outputs/forecast_results.csv')
        return forecast, True
    except Exception as e:
        st.warning(f"⚠️ Phase 3 forecast not found: {str(e)}")
        return None, False

# ========================
# ANALYSIS FUNCTIONS
# ========================
def calculate_real_kpis(sales_df, customers_df):
    """Calculate actual KPIs from your data"""
    # Revenue metrics
    total_revenue = sales_df['OrderValue'].sum() if 'OrderValue' in sales_df.columns else sales_df['order_value'].sum()
    
    # Order metrics
    total_orders = len(sales_df)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Customer metrics
    total_customers = customers_df['CustomerID'].nunique() if 'CustomerID' in customers_df.columns else len(customers_df)
    
    # Time-based growth (compare last 30 days vs previous 30 days)
    sales_df['OrderDate'] = pd.to_datetime(sales_df.get('OrderDate', sales_df.get('order_date')))
    latest_date = sales_df['OrderDate'].max()
    thirty_days_ago = latest_date - timedelta(days=30)
    sixty_days_ago = latest_date - timedelta(days=60)
    
    recent_sales = sales_df[sales_df['OrderDate'] >= thirty_days_ago]
    previous_sales = sales_df[(sales_df['OrderDate'] >= sixty_days_ago) & (sales_df['OrderDate'] < thirty_days_ago)]
    
    recent_revenue = recent_sales['OrderValue'].sum() if 'OrderValue' in recent_sales.columns else recent_sales['order_value'].sum()
    previous_revenue = previous_sales['OrderValue'].sum() if 'OrderValue' in previous_sales.columns else previous_sales['order_value'].sum()
    
    revenue_growth = ((recent_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
    
    orders_growth = ((len(recent_sales) - len(previous_sales)) / len(previous_sales) * 100) if len(previous_sales) > 0 else 0
    
    recent_aov = recent_revenue / len(recent_sales) if len(recent_sales) > 0 else 0
    previous_aov = previous_revenue / len(previous_sales) if len(previous_sales) > 0 else 0
    aov_growth = ((recent_aov - previous_aov) / previous_aov * 100) if previous_aov > 0 else 0
    
    return {
        'total_revenue': total_revenue,
        'revenue_growth': revenue_growth,
        'total_orders': total_orders,
        'orders_growth': orders_growth,
        'avg_order_value': avg_order_value,
        'aov_growth': aov_growth,
        'total_customers': total_customers,
        'customer_growth': 0  # Would need historical customer data
    }

def create_revenue_trend_actual(sales_df):
    """Create revenue trend from actual data"""
    sales_df['OrderDate'] = pd.to_datetime(sales_df.get('OrderDate', sales_df.get('order_date')))
    sales_df['YearMonth'] = sales_df['OrderDate'].dt.to_period('M')
    
    value_col = 'OrderValue' if 'OrderValue' in sales_df.columns else 'order_value'
    monthly_revenue = sales_df.groupby('YearMonth')[value_col].sum().reset_index()
    monthly_revenue['OrderDate'] = monthly_revenue['YearMonth'].dt.to_timestamp()
    
    fig = px.line(monthly_revenue, x='OrderDate', y=value_col,
                  title='📈 Actual Revenue Trend (Monthly)',
                  labels={value_col: 'Revenue ($)', 'OrderDate': 'Date'})
    fig.update_traces(line_color='#667eea', line_width=3, fill='tozeroy')
    fig.update_layout(hovermode='x unified', height=400)
    return fig

def create_category_analysis(sales_df, products_df):
    """Analyze sales by product category"""
    try:
        # Merge sales with products to get category
        sales_merged = sales_df.merge(products_df, on='ProductID', how='left')
        category_col = 'ProductCategory' if 'ProductCategory' in sales_merged.columns else 'category'
        value_col = 'OrderValue' if 'OrderValue' in sales_merged.columns else 'order_value'
        
        category_sales = sales_merged.groupby(category_col)[value_col].sum().reset_index()
        
        fig = px.pie(category_sales, values=value_col, names=category_col,
                     title='🥧 Sales Distribution by Category',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        st.error(f"Error creating category chart: {e}")
        return None

def create_churn_analysis(churn_predictions):
    """Analyze churn predictions from your model"""
    if churn_predictions is None:
        return None
    
    # Assuming your predictions have 'ChurnPrediction' or 'churn_prob' column
    if 'ChurnPrediction' in churn_predictions.columns:
        churn_col = 'ChurnPrediction'
    elif 'churn_prob' in churn_predictions.columns:
        churn_col = 'churn_prob'
    else:
        return None
    
    high_risk_pct = (churn_predictions[churn_col] > 0.5).sum() / len(churn_predictions) * 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=high_risk_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "High Churn Risk %"},
        delta={'reference': 15},
        gauge={
            'axis': {'range': [None, 50]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 15], 'color': "#e8f5e9"},
                {'range': [15, 30], 'color': "#fff9c4"},
                {'range': [30, 50], 'color': "#ffcdd2"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def create_cluster_visualization(cluster_summary, customers_clustered):
    """Visualize customer segments from Phase 3"""
    if cluster_summary is None:
        return None
    
    fig = px.bar(cluster_summary, x='Cluster', y='CustomerCount',
                 title='👥 Customer Segments (From Your Clustering)',
                 color='Cluster',
                 color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe'])
    fig.update_layout(showlegend=False, height=400)
    return fig

def create_forecast_visualization(forecast_df):
    """Visualize demand forecast from Phase 3"""
    if forecast_df is None:
        return None
    
    fig = px.line(forecast_df, x='Date', y='ForecastedRevenue',
                  title='📊 Revenue Forecast (From Your Model)',
                  labels={'ForecastedRevenue': 'Forecasted Revenue ($)', 'Date': 'Date'})
    fig.update_traces(line_color='#764ba2', line_width=3)
    fig.update_layout(height=400)
    return fig

# ========================
# MAIN APPLICATION
# ========================
def main():
    # Header
    st.markdown('<h1 class="main-header">🛒 RetailSmart Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### *Using Your Actual Project Data & Trained Models*")
    st.markdown("---")
    
    # Load data
    with st.spinner('Loading your project data...'):
        customers, sales, products, marketing, reviews, data_source = load_cleaned_data()
        
        if customers is None:
            st.error("❌ Cannot load data files. Please check your folder structure!")
            st.info("""
            **Expected folder structure:**
            ```
            Capstone_Project/
            ├── Datasets/
            │   ├── customers.csv
            │   ├── sales.csv
            │   ├── products.csv
            │   ├── marketing.csv
            │   └── reviews.csv
            └── Exported_files/
                ├── Phase1/ (cleaned data)
                ├── Phase2/ (models)
                └── Phase3/ (clustering, forecast)
            ```
            """)
            return
        
        # Load Phase 2 predictions
        churn_pred, model_input, has_predictions = load_model_predictions()
        model, scaler, has_model = load_trained_model()
        
        # Load Phase 3 results
        cluster_summary, customers_clustered, has_clustering = load_clustering_results()
        forecast, has_forecast = load_forecast_results()
        
        # Data source indicator
        st.markdown(f"""
        <div class="success-box">
            ✅ <strong>Data Loaded Successfully!</strong><br>
            📂 Source: {data_source}<br>
            🔬 Phase 2 Model: {'✅ Loaded' if has_model else '❌ Not Found'}<br>
            🎯 Phase 2 Predictions: {'✅ Loaded' if has_predictions else '❌ Not Found'}<br>
            👥 Phase 3 Clustering: {'✅ Loaded' if has_clustering else '❌ Not Found'}<br>
            📈 Phase 3 Forecast: {'✅ Loaded' if has_forecast else '❌ Not Found'}
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Filters
    date_col = 'OrderDate' if 'OrderDate' in sales.columns else 'order_date'
    sales[date_col] = pd.to_datetime(sales[date_col])
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(sales[date_col].min(), sales[date_col].max()),
        key='date_range'
    )
    
    # Apply filters
    filtered_sales = sales[(sales[date_col] >= pd.Timestamp(date_range[0])) & 
                           (sales[date_col] <= pd.Timestamp(date_range[1]))]
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📁 Your Data")
    st.sidebar.info(f"""
    **Customers:** {len(customers):,}  
    **Orders:** {len(sales):,}  
    **Products:** {len(products):,}  
    **Marketing Records:** {len(marketing):,}  
    **Reviews:** {len(reviews):,}
    """)
    
    # KPIs
    st.markdown("## 📈 Key Performance Indicators (From Your Data)")
    kpis = calculate_real_kpis(filtered_sales, customers)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"${kpis['total_revenue']:,.2f}",
            delta=f"{kpis['revenue_growth']:.1f}%"
        )
    
    with col2:
        st.metric(
            label="🛍️ Total Orders",
            value=f"{kpis['total_orders']:,}",
            delta=f"{kpis['orders_growth']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="💵 Avg Order Value",
            value=f"${kpis['avg_order_value']:.2f}",
            delta=f"{kpis['aov_growth']:.1f}%"
        )
    
    with col4:
        st.metric(
            label="👥 Total Customers",
            value=f"{kpis['total_customers']:,}",
            delta="Active"
        )
    
    st.markdown("---")
    
    # Visualizations
    st.markdown("## 📊 Analytics from Your Project Phases")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Phase 1: EDA", "🎯 Phase 2: Predictions", "👥 Phase 3: Clustering", "📊 Phase 3: Forecast"])
    
    with tab1:
        st.markdown("### Phase 1: Exploratory Data Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_revenue_trend_actual(filtered_sales)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_category_analysis(filtered_sales, products)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # Show data quality
        st.markdown("### 📋 Data Quality Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            missing_sales = sales.isnull().sum().sum()
            st.metric("Sales Missing Values", missing_sales)
        
        with col2:
            missing_customers = customers.isnull().sum().sum()
            st.metric("Customer Missing Values", missing_customers)
        
        with col3:
            missing_products = products.isnull().sum().sum()
            st.metric("Product Missing Values", missing_products)
    
    with tab2:
        st.markdown("### Phase 2: Churn Prediction Results")
        
        if has_predictions:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_churn_analysis(churn_pred)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 🎯 Model Performance")
                st.info("""
                **Your Trained Model:**
                - Model Type: Random Forest Classifier
                - Features: RFM + Customer Attributes
                - Training: Phase 2 Complete
                
                **Key Metrics:**
                Check Phase2 folder for detailed metrics!
                """)
                
                if has_model:
                    st.success("✅ Model loaded successfully!")
                    st.code(f"Model: {type(model).__name__}")
        else:
            st.warning("⚠️ Phase 2 predictions not found. Complete Phase 2 to see churn analysis.")
    
    with tab3:
        st.markdown("### Phase 3: Customer Segmentation")
        
        if has_clustering:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_cluster_visualization(cluster_summary, customers_clustered)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 👥 Segment Summary")
                st.dataframe(cluster_summary, use_container_width=True)
        else:
            st.warning("⚠️ Phase 3 clustering not found. Complete Phase 3 to see segmentation.")
    
    with tab4:
        st.markdown("### Phase 3: Demand Forecasting")
        
        if has_forecast:
            fig = create_forecast_visualization(forecast)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📊 Forecast Details")
            st.dataframe(forecast.head(10), use_container_width=True)
        else:
            st.warning("⚠️ Phase 3 forecast not found. Complete Phase 3 to see predictions.")
    
    st.markdown("---")
    
    # Raw Data
    with st.expander("📋 View Your Raw Data"):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Customers", "Sales", "Products", "Marketing", "Reviews"])
        
        with tab1:
            st.dataframe(customers.head(100), use_container_width=True)
        with tab2:
            st.dataframe(sales.head(100), use_container_width=True)
        with tab3:
            st.dataframe(products.head(100), use_container_width=True)
        with tab4:
            st.dataframe(marketing.head(100), use_container_width=True)
        with tab5:
            st.dataframe(reviews.head(100), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ by Kanak Baghel | 
            <a href='https://github.com/Kanakbaghel/Capstone_Project'>GitHub</a> | 
            <a href='https://www.linkedin.com/in/kanakbaghel'>LinkedIn</a></p>
            <p><em>RetailSmart Analytics Dashboard v2.0 | Using Real Project Data</em></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
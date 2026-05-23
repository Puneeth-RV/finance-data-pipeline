import streamlit as st
import pandas as pd
from src.processor import compute_summary_stats
from src.ml_visualizations import run_ml_pipeline, generate_visualizations
import matplotlib.pyplot as plt

# 1. Custom CSS for a premium "Not AI" look
st.set_page_config(page_title="Finance Data Pipeline", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean Fonts and Margins */
    html, body, [class*="css"]  {
        font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Stylish KPI Cards */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Finance Data Pipeline & Analysis")
st.write("An end-to-end data processing, machine learning, and visualization dashboard.")

# Sidebar
st.sidebar.header("Control Panel")

# Load summary stats
@st.cache_data
def load_stats():
    # Only compute once for performance
    try:
         return compute_summary_stats("data/raw")
    except Exception as e:
         st.error(f"Error loading stats: {e}")
         return {}
         
stats = load_stats()

if not stats:
    st.sidebar.warning("No data found. Please run the fetcher first.")
    st.stop()

tickers = list(stats.keys())
selected_ticker = st.sidebar.selectbox("Select a Stock", tickers, index=tickers.index('AAPL') if 'AAPL' in tickers else 0)

# KPI Section
st.subheader(f"Key Performance Indicators: {selected_ticker}")
kpis = stats[selected_ticker]
col1, col2, col3 = st.columns(3)
col1.metric("Avg Daily Return", f"{kpis['Avg_Return'] * 100:.2f}%")
col2.metric("Volatility (Std Dev)", f"{kpis['Volatility']:.4f}")
col3.metric("Total Volume", f"{kpis['Total_Volume']:,.0f}")

st.divider()

# ML Section
st.subheader("Machine Learning Predictions")
st.write("Predicting if the stock will close HIGHER tomorrow using a Random Forest Classifier.")

if st.button(f"Run Model on {selected_ticker}", type="primary"):
    with st.spinner('Training model and generating plots...'):
        df, ticker_name, acc = run_ml_pipeline(selected_ticker)
        
        st.success(f"Model trained successfully! Accuracy: **{acc * 100:.2f}%**")
        
        # Render Visualizations
        fig2d, fig3d, bokeh_plot = generate_visualizations(df, ticker_name)
        
        st.markdown("### Model Visualizations")
        tab1, tab2, tab3 = st.tabs(["📈 Interactive Price Chart", "📊 Moving Average Trend", "🧊 3D Feature Analysis"])
        
        with tab1:
            import streamlit.components.v1 as components
            try:
                 with open(f"visualizations/{ticker_name}_interactive.html", 'r', encoding='utf-8') as f:
                     components.html(f.read(), height=450)
            except Exception as e:
                 st.error(f"Could not load Bokeh chart: {e}")
                 
        with tab2:
            st.pyplot(fig2d)
            
        with tab3:
            st.pyplot(fig3d)

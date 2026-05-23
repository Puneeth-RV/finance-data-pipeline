import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from src.processor import process_file, get_csv_files

def prepare_ml_data(file_path):
    """
    Prepares data for machine learning.
    Target: 1 if next day's return is > 0, else 0.
    Features: Returns, Volatility, Moving Averages.
    """
    df = process_file(file_path)
    if df is None or len(df) < 50:
        return None
        
    # Features
    df['MA_10'] = df['Close'].rolling(window=10).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['Volatility_10'] = df['Daily_Return'].rolling(window=10).std()
    
    # Target
    df['Target'] = (df['Daily_Return'].shift(-1) > 0).astype(int)
    
    df.dropna(inplace=True)
    return df

def run_ml_pipeline():
    """
    Runs a Random Forest Classifier on Apple (AAPL) stock as a demonstration.
    """
    print("\n--- Running Machine Learning Pipeline ---")
    data_path = Path("data/raw/AAPL.csv")
    if not data_path.exists():
         # Fallback to first file
         data_path = list(get_csv_files("data/raw"))[0]
         
    df = prepare_ml_data(data_path)
    
    features = ['Daily_Return', 'MA_10', 'MA_50', 'Volatility_10', 'Volume']
    X = df[features]
    y = df['Target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Random Forest Accuracy on {data_path.stem}: {acc * 100:.2f}%")
    return df, data_path.stem

def generate_visualizations(df, ticker_name):
    """
    Generates 2D/3D Matplotlib plots and an interactive Bokeh plot.
    """
    print("\n--- Generating Visualizations ---")
    os.makedirs("visualizations", exist_ok=True)
    
    # 1. 2D Matplotlib Plot (Price and Moving Averages)
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Close'], label='Close Price')
    plt.plot(df['Date'], df['MA_50'], label='50-Day MA')
    plt.title(f"{ticker_name} Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.savefig(f"visualizations/{ticker_name}_2D_plot.png")
    print(f"Saved 2D plot: visualizations/{ticker_name}_2D_plot.png")
    
    # 2. 3D Matplotlib Plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(df['Daily_Return'], df['Volatility_10'], df['Volume'], c=df['Target'], cmap='coolwarm', alpha=0.6)
    ax.set_xlabel('Daily Return')
    ax.set_ylabel('10-Day Volatility')
    ax.set_zlabel('Volume')
    ax.set_title("3D Feature Scatter Plot (Red=Up, Blue=Down)")
    plt.colorbar(sc, ax=ax, label='Target (0 or 1)')
    plt.savefig(f"visualizations/{ticker_name}_3D_plot.png")
    print(f"Saved 3D plot: visualizations/{ticker_name}_3D_plot.png")
    
    # 3. Interactive Bokeh Plot
    source = ColumnDataSource(df)
    
    p = figure(x_axis_type="datetime", title=f"Interactive {ticker_name} Chart",
               width=800, height=400)
    
    p.line(x='Date', y='Close', source=source, color="blue", legend_label="Close Price")
    
    p.add_tools(HoverTool(
        tooltips=[
            ("Date", "@Date{%F}"),
            ("Close", "$@Close{0.2f}"),
            ("Volume", "@Volume{0.00 a}")
        ],
        formatters={
            '@Date': 'datetime'
        },
        mode='mouse'
    ))
    
    output_file(f"visualizations/{ticker_name}_interactive.html")
    save(p)
    print(f"Saved interactive plot: visualizations/{ticker_name}_interactive.html")

if __name__ == "__main__":
    df, ticker = run_ml_pipeline()
    if df is not None:
         generate_visualizations(df, ticker)

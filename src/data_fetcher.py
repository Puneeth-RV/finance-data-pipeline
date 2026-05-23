import yfinance as yf
import pandas as pd
import os
from pathlib import Path

# A list of 50 common stocks across various sectors
TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'JNJ',
    'WMT', 'PG', 'MA', 'UNH', 'DIS', 'HD', 'BAC', 'VZ', 'ADBE', 'CMCSA',
    'NFLX', 'KO', 'NKE', 'MRK', 'PEP', 'T', 'PFE', 'INTC', 'CRM', 'ABT',
    'ORCL', 'ABBV', 'CSCO', 'TMO', 'AVGO', 'XOM', 'ACN', 'QCOM', 'COST', 'CVX',
    'LLY', 'MCD', 'DHR', 'MDT', 'NEE', 'TXN', 'HON', 'UPS', 'BMY', 'UNP'
]

def fetch_data(tickers, start_date="2020-01-01", end_date="2024-01-01", output_dir="data/raw"):
    """
    Fetches historical stock data for a list of tickers and saves them to CSV.
    Demonstrates basic filesystem operations.
    """
    # Filesystem operations
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching data for {len(tickers)} tickers...")
    
    for ticker in tickers:
        try:
            print(f"Downloading {ticker}...")
            # Fetch data using yfinance
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            # Save to CSV if data exists
            if not df.empty:
                output_path = Path(output_dir) / f"{ticker}.csv"
                df.to_csv(output_path)
                print(f"Saved {ticker} to {output_path}")
            else:
                print(f"Warning: No data found for {ticker}")
                
        except Exception as e:
            # Exception handling
            print(f"Error fetching data for {ticker}: {e}")

if __name__ == "__main__":
    fetch_data(TICKERS)

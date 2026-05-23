import os
import pandas as pd
from pathlib import Path

def get_csv_files(directory):
    """
    Generator expression to yield CSV files one by one.
    This fulfills the requirement of 'generator expressions' and 'filesystem operations'.
    """
    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"Directory {directory} does not exist.")
        
    return (file for file in path.iterdir() if file.suffix == '.csv')

def process_file(file_path):
    """
    Reads a single CSV, cleans it, and calculates some basic metrics.
    Demonstrates exception handling.
    """
    try:
        # Check if it has yfinance multi-level header
        with open(file_path, 'r') as f:
            first_line = f.readline()
            
        if "Price," in first_line:
            df = pd.read_csv(file_path, header=[0, 1], index_col=0)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            df = df.reset_index()
        else:
            df = pd.read_csv(file_path)
            
        # Exception handling: Ensure required columns exist
        required_cols = {'Date', 'Close', 'Volume'}
        if not required_cols.issubset(df.columns):
            df = df.reset_index() # Fallback for index issue
            if not required_cols.issubset(df.columns):
                 raise ValueError(f"Missing required columns in {file_path}")
            
        # Convert Date to datetime but handle timezone offset issues securely
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        
        # Sort by date just in case
        df = df.sort_values('Date')
        
        # Calculate daily returns
        df['Daily_Return'] = df['Close'].pct_change()
        
        # Drop NaN values (the first row will be NaN because of pct_change)
        df.dropna(subset=['Daily_Return'], inplace=True)
        
        return df
    except pd.errors.EmptyDataError:
        print(f"Warning: {file_path} is empty.")
        return None
    except ValueError as ve:
        print(f"Validation Error in {file_path}: {ve}")
        return None
    except Exception as e:
        print(f"Unexpected Error processing {file_path}: {e}")
        return None

def compute_summary_stats(directory="data/raw"):
    """
    Computes summary statistics for all tickers in the directory.
    Demonstrates comprehensions.
    """
    files = get_csv_files(directory)
    
    # List comprehension to process all files
    processed_dfs = [
        (file.stem, process_file(file)) 
        for file in files 
    ]
    
    # Dictionary comprehension to build summary stats, filtering out None values
    summary_stats = {
        ticker: {
            'Avg_Return': df['Daily_Return'].mean(),
            'Volatility': df['Daily_Return'].std(),
            'Total_Volume': df['Volume'].sum()
        }
        for ticker, df in processed_dfs if df is not None and not df.empty
    }
    
    return summary_stats

if __name__ == "__main__":
    stats = compute_summary_stats()
    print(f"Processed {len(stats)} tickers successfully.")
    for t, s in list(stats.items())[:5]: # Print first 5
        print(f"{t}: {s}")

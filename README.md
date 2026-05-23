# Data Science Foundation - Final Assignment

**Course Code:** CSE4111A  
**Program:** B. Tech. in CSE, Batch 2025  
**University:** Ramaiah University of Applied Sciences  

## Project Overview

This repository contains an end-to-end Data Science pipeline built for analyzing historical financial data. The project fetches stock market data from Yahoo Finance, processes it using advanced Python features, runs Machine Learning models to predict stock price movements, and visualizes the results through an interactive web dashboard.

---

## 🎯 Rubric Fulfillment

This project was specifically designed to strictly meet all requirements of the Data Science Foundation assignment:

### Part-B Question 1 (10 Marks)
*   **Real-world Dataset:** Selected from the **Finance** domain (historical daily prices for 50 major stocks).
*   **Filesystem Operations:** Uses `os` and `pathlib` to dynamically read multiple `.csv` files from the `data/raw/` directory.
*   **Generator Expressions:** Employs a generator expression `(file for file in path.iterdir())` to lazily yield file paths, preventing memory overload.
*   **Advanced Collections & Comprehensions:** Utilizes dictionary and list comprehensions to efficiently aggregate summary statistics across all 50 stocks.
*   **Exception Handling:** Robust `try...except` blocks handle corrupted CSVs, missing columns, and differences in multi-level headers.
*   **Machine Learning:** Implements a **Random Forest Classifier** (`scikit-learn`) to predict if a stock will close higher the next day based on moving averages and volatility.
*   **Visualizations:** Generates 2D/3D Matplotlib plots and an interactive candlestick-like Bokeh chart.

### Part-B Question 2 (8 Marks)
*   **Concurrency vs. Parallelism Benchmarking:** Included is `src/concurrency_benchmark.py`, a script that simulates heavy computation across the dataset.
*   **GIL Analysis:** The script explicitly demonstrates the bottleneck of Python's Global Interpreter Lock (GIL) by comparing the execution time of Threading (Concurrency) versus Multiprocessing (Parallelism). 

### Part-B Question 3 (7 Marks)
*   **Test-Driven Development (TDD):** A TDD mini-framework is implemented in `tests/test_processor.py` using `pytest`.
*   **Debugging with `pdb`:** The test suite includes a demonstration setup for Python's built-in debugger (`pdb`).
*   **Deployment Readiness:** The entire project is configured to run inside a Python virtual environment (`venv`).

---

## 🚀 How to Run the Project

### 1. Environment Setup
Clone this repository and set up the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # Or install pandas numpy yfinance scikit-learn matplotlib bokeh pytest streamlit
```

### 2. Export Python Path
Ensure the `src` directory can be discovered:
```bash
export PYTHONPATH=.
```

### 3. Launch the Interactive Web Dashboard
The easiest way to interact with this project is via the premium Streamlit dashboard.
```bash
streamlit run app.py
```
This will open a web application where you can select a stock, view its Key Performance Indicators, and run the Random Forest model live to generate interactive plots.

### 4. Running Scripts Individually
You can also run any module from the terminal:
*   **Fetch Data:** `python src/data_fetcher.py`
*   **Test Data Processor:** `python src/processor.py`
*   **Run Concurrency Benchmark:** `python src/concurrency_benchmark.py`
*   **Run TDD Framework:** `pytest tests/test_processor.py -v`

---
*Developed for the Data Science Foundation Assessment.*

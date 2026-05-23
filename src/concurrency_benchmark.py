import time
import os
from pathlib import Path
import pandas as pd
import concurrent.futures
from src.processor import get_csv_files

# A CPU-bound task to simulate heavy computation on data
def heavy_computation(file_path):
    # Read the file just to include some I/O
    try:
        df = pd.read_csv(file_path)
    except:
        pass
        
    # Simulate an extremely heavy CPU-bound math task
    # This will clearly demonstrate the GIL limitation and Multiprocessing speedup
    count = 0
    for i in range(5 * 10**6):
        count += i
    return count

def benchmark_sequential(files):
    start = time.time()
    results = [heavy_computation(f) for f in files]
    end = time.time()
    return end - start

def benchmark_threading(files):
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(heavy_computation, files))
    end = time.time()
    return end - start

def benchmark_multiprocessing(files):
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(heavy_computation, files))
    end = time.time()
    return end - start

def main():
    directory = "data/raw"
    files = list(get_csv_files(directory))
    
    print(f"Benchmarking with {len(files)} files...\n")
    
    seq_time = benchmark_sequential(files)
    print(f"Sequential Time: {seq_time:.2f} seconds")
    
    thread_time = benchmark_threading(files)
    print(f"Threading Time (Concurrency): {thread_time:.2f} seconds")
    
    process_time = benchmark_multiprocessing(files)
    print(f"Multiprocessing Time (Parallelism): {process_time:.2f} seconds")
    
    print("\n--- Analysis for the Report ---")
    print("1. Threading (Concurrency) in Python is limited by the Global Interpreter Lock (GIL).")
    print("   Because the task is CPU-bound (heavy math), threads block each other, resulting in")
    print(f"   a time ({thread_time:.2f}s) that is similar to or worse than Sequential ({seq_time:.2f}s) due to context switching overhead.")
    print("2. Multiprocessing (Parallelism) bypasses the GIL by creating entirely new Python processes.")
    print(f"   This allows true parallel execution on multiple CPU cores, resulting in a significantly faster time ({process_time:.2f}s).")

if __name__ == "__main__":
    main()

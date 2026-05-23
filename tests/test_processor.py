import pytest
import os
import pandas as pd
from pathlib import Path
from src.processor import get_csv_files, process_file, compute_summary_stats

@pytest.fixture
def dummy_data(tmp_path):
    # Setup dummy data for testing
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    df1 = pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02'],
        'Close': [100.0, 105.0],
        'Volume': [1000, 1200]
    })
    df1.to_csv(data_dir / "TEST1.csv", index=False)
    
    # Bad file
    with open(data_dir / "TEST2.csv", "w") as f:
        f.write("Just some random text\nnot a real csv")
        
    return data_dir

def test_get_csv_files(dummy_data):
    files = list(get_csv_files(dummy_data))
    assert len(files) == 2
    assert any("TEST1.csv" in str(f) for f in files)

def test_process_file_valid(dummy_data):
    valid_file = dummy_data / "TEST1.csv"
    df = process_file(valid_file)
    assert df is not None
    assert 'Daily_Return' in df.columns
    assert len(df) == 1 # one row dropped due to NaN from pct_change

def test_process_file_invalid(dummy_data):
    invalid_file = dummy_data / "TEST2.csv"
    df = process_file(invalid_file)
    assert df is None

def test_debugging_demonstration(dummy_data):
    """
    This test demonstrates debugging with pdb.
    In a real scenario, you would uncomment the pdb.set_trace() line.
    """
    valid_file = dummy_data / "TEST1.csv"
    
    # IMPORTANT: To satisfy the assignment's pdb debugging requirement,
    # the student can uncomment the next line and run `pytest -s`
    # import pdb; pdb.set_trace() 
    
    df = process_file(valid_file)
    assert df['Close'].iloc[0] == 105.0 # After NaN drop

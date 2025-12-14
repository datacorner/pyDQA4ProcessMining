"""
Pytest configuration and fixtures for pyDQA4ProcessMining tests.
"""

import os
import sys
import pytest
import tempfile
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_csv_path():
    """Path to the sample data CSV file."""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "samples",
        "data.csv"
    )


@pytest.fixture
def sample_intl_csv_path():
    """Path to the International Declarations sample CSV file."""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "samples",
        "InternationalDeclarations.csv"
    )


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_csv_file(temp_dir):
    """Create a temporary CSV file with sample data."""
    csv_path = os.path.join(temp_dir, "test_data.csv")
    
    data = {
        "case_id": ["C001", "C001", "C002", "C002", "C003"],
        "activity": ["Start", "End", "Start", "End", "Start"],
        "timestamp": [
            "2023-01-15 09:00:00",
            "2023-01-15 10:00:00",
            "2023-01-15 11:00:00",
            "2023-01-15 12:00:00",
            "2023-01-15 13:00:00"
        ],
        "amount": [100, 100, 200, 200, 300]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    
    return csv_path


@pytest.fixture
def temp_csv_with_nulls(temp_dir):
    """Create a temporary CSV file with null values."""
    csv_path = os.path.join(temp_dir, "test_nulls.csv")
    
    data = {
        "case_id": ["C001", None, "C003", "C004", "C005"],
        "activity": ["Start", "End", None, "End", "Start"],
        "timestamp": [
            "2023-01-15 09:00:00",
            "2023-01-15 10:00:00",
            "2023-01-15 11:00:00",
            None,
            "2023-01-15 13:00:00"
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    
    return csv_path


@pytest.fixture
def temp_csv_with_duplicates(temp_dir):
    """Create a temporary CSV file with duplicate rows."""
    csv_path = os.path.join(temp_dir, "test_dups.csv")
    
    data = {
        "case_id": ["C001", "C001", "C001", "C002", "C002"],
        "activity": ["Start", "Start", "End", "Start", "Start"],
        "timestamp": [
            "2023-01-15 09:00:00",
            "2023-01-15 09:00:00",  # Duplicate
            "2023-01-15 10:00:00",
            "2023-01-15 11:00:00",
            "2023-01-15 11:00:00"   # Duplicate
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    
    return csv_path


@pytest.fixture
def sample_events_df():
    """Create a sample events DataFrame."""
    return pd.DataFrame({
        "Column": ["Start Process", "End Process", "Review!", "Approve?"],
        "Frequency": [100, 90, 50, 30]
    })


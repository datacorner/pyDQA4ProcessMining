"""
Tests for pydqa4pm.core.dqa module (main DQA orchestrator).
"""

import os
import pytest
from pydqa4pm.core.dqa import Dqa4PM
from pydqa4pm.utils.logger import Logger


class TestDqa4PM:
    """Test suite for Dqa4PM class."""
    
    @pytest.fixture
    def dqa_instance(self):
        """Create a Dqa4PM instance for testing."""
        logger = Logger("test")
        return Dqa4PM(logger)
    
    def test_dqa_creation(self, dqa_instance):
        """Test Dqa4PM can be created."""
        assert dqa_instance is not None
    
    def test_dqa_has_logger(self, dqa_instance):
        """Test Dqa4PM has logger property."""
        assert dqa_instance.T is not None
        assert isinstance(dqa_instance.T, Logger)
    
    def test_open_dataset(self, dqa_instance, temp_csv_file):
        """Test opening a dataset."""
        ds = dqa_instance.open_dataset(temp_csv_file, ",", "case_id", "activity", "timestamp")
        
        assert ds is not None
        assert ds.isOpened() is True
    
    def test_open_dataset_backward_compat(self, dqa_instance, temp_csv_file):
        """Test OpenDataset backward compatibility alias."""
        ds = dqa_instance.OpenDataset(temp_csv_file, ",", "case_id", "activity", "timestamp")
        
        assert ds is not None
        assert ds.isOpened() is True
    
    def test_make_dqa_checks(self, dqa_instance, temp_csv_file):
        """Test making DQA checks."""
        ds = dqa_instance.open_dataset(temp_csv_file, ",", "case_id", "activity", "timestamp")
        report_data = dqa_instance.make_dqa_checks(ds)
        
        assert report_data is not None
        assert report_data.AllChecksOK is True
        assert report_data.RowCount > 0
    
    def test_make_dqa_checks_backward_compat(self, dqa_instance, temp_csv_file):
        """Test MakeDQAChecks backward compatibility alias."""
        ds = dqa_instance.open_dataset(temp_csv_file, ",", "case_id", "activity", "timestamp")
        report_data = dqa_instance.MakeDQAChecks(ds)
        
        assert report_data is not None
    
    def test_create_alternative_data(self, dqa_instance, temp_csv_file, temp_dir):
        """Test creating alternative data files."""
        # Create CSV in temp dir
        import shutil
        temp_csv = os.path.join(temp_dir, "test.csv")
        shutil.copy(temp_csv_file, temp_csv)
        
        ds = dqa_instance.open_dataset(temp_csv, ",", "case_id", "activity", "timestamp")
        ds.check3PKeys()
        dqa_instance.create_alternative_data(ds)
        
        events_file = ds.uniqueEventsFilename
        assert os.path.exists(events_file)
    
    def test_full_process(self, dqa_instance, temp_csv_file, temp_dir, capsys):
        """Test full process workflow."""
        import shutil
        temp_csv = os.path.join(temp_dir, "test.csv")
        shutil.copy(temp_csv_file, temp_csv)
        
        # Run full process
        dqa_instance.process(temp_csv, ",", "case_id", "activity", "timestamp")
        
        # Check output was logged
        captured = capsys.readouterr()
        assert "Opening dataset" in captured.out or "open" in captured.out.lower()
    
    def test_process_backward_compat(self, dqa_instance, temp_csv_file, temp_dir):
        """Test Process backward compatibility alias."""
        import shutil
        temp_csv = os.path.join(temp_dir, "test.csv")
        shutil.copy(temp_csv_file, temp_csv)
        
        # Should not raise
        dqa_instance.Process(temp_csv, ",", "case_id", "activity", "timestamp")


class TestDqa4PMErrorHandling:
    """Test error handling in Dqa4PM."""
    
    @pytest.fixture
    def dqa_instance(self):
        """Create a Dqa4PM instance for testing."""
        logger = Logger("test_error")
        return Dqa4PM(logger)
    
    def test_open_nonexistent_file(self, dqa_instance, capsys):
        """Test opening a non-existent file."""
        ds = dqa_instance.open_dataset("/nonexistent/file.csv", ",", "a", "b", "c")
        
        # Should not crash, just log error
        assert ds.isOpened() is False
    
    def test_open_wrong_columns(self, dqa_instance, temp_csv_file, capsys):
        """Test opening with wrong column names."""
        ds = dqa_instance.open_dataset(temp_csv_file, ",", "wrong", "columns", "here")
        
        # File should open but key check fails
        assert ds.isOpened() is True
        
        captured = capsys.readouterr()
        # Should have error about columns not found
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()


class TestDqa4PMWithSampleData:
    """Test Dqa4PM with actual sample data files."""
    
    @pytest.fixture
    def dqa_instance(self):
        """Create a Dqa4PM instance."""
        logger = Logger("test_sample")
        return Dqa4PM(logger)
    
    def test_with_sample_csv(self, dqa_instance, sample_csv_path):
        """Test with the sample data.csv file."""
        if not os.path.exists(sample_csv_path):
            pytest.skip("Sample CSV not found")
        
        ds = dqa_instance.open_dataset(
            sample_csv_path, ",", "id", "concept:name", "time:timestamp"
        )
        
        assert ds.isOpened() is True
    
    def test_with_intl_declarations(self, dqa_instance, sample_intl_csv_path):
        """Test with the InternationalDeclarations.csv file."""
        if not os.path.exists(sample_intl_csv_path):
            pytest.skip("International Declarations CSV not found")
        
        ds = dqa_instance.open_dataset(
            sample_intl_csv_path, ",", "id", "concept:name", "time:timestamp"
        )
        
        assert ds.isOpened() is True
        
        report_data = dqa_instance.make_dqa_checks(ds)
        assert report_data.AllChecksOK is True


"""
Tests for pydqa4pm.reports module.
"""

import os
import pytest
import tempfile
from pydqa4pm.reports.store import ReportStore
from pydqa4pm.reports.pdf_builder import PDFReportBuilder
from pydqa4pm.core.report_data import DQAReportData
from pydqa4pm.utils import constants as C


class TestReportStore:
    """Test suite for ReportStore class."""
    
    def test_store_creation(self):
        """Test ReportStore can be created."""
        store = ReportStore()
        assert store is not None
    
    def test_store_initialize(self, temp_dir):
        """Test store initialization creates temp folder."""
        store = ReportStore()
        # Access the property setter directly
        store.tempPath = os.path.join(temp_dir, "temp_store/")
        
        result = store.initialize()
        assert result is True
        assert os.path.exists(store.tempPath)
    
    def test_store_get_path(self):
        """Test getPath returns full path."""
        store = ReportStore()
        path = store.getPath("test.jpg")
        assert path.endswith("test.jpg")
        assert C.DEFAULT_STORE_FOLDER in path
    
    def test_store_finalize(self, temp_dir):
        """Test store finalize cleans up files."""
        store = ReportStore()
        store.tempPath = os.path.join(temp_dir, "temp_store/")
        store.initialize()
        
        # Create a test file
        test_file = store.getPath("test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        
        store.finalize()
        assert not os.path.exists(test_file)
    
    def test_store_is_folder_exist(self, temp_dir):
        """Test isStoreFolderExist method."""
        store = ReportStore()
        store.tempPath = temp_dir
        assert store.isStoreFolderExist() is True
        
        store.tempPath = "/nonexistent/path/"
        assert store.isStoreFolderExist() is False


class TestDQAReportData:
    """Test suite for DQAReportData class."""
    
    def test_report_data_creation(self):
        """Test DQAReportData can be created."""
        data = DQAReportData("test.csv", "pfi", "sn", "t")
        assert data is not None
    
    def test_report_data_properties(self):
        """Test DQAReportData properties."""
        data = DQAReportData("test.csv", "case_id", "activity", "timestamp")
        
        assert data.filename == "test.csv"
        assert data.PFIKey == "case_id"
        assert data.SNKey == "activity"
        assert data.TKey == "timestamp"
    
    def test_report_data_row_col_count(self):
        """Test row and column count properties."""
        data = DQAReportData("test.csv", "pfi", "sn", "t")
        
        data.RowCount = 100
        data.ColCount = 5
        
        assert data.RowCount == 100
        assert data.ColCount == 5
    
    def test_report_data_attributes(self):
        """Test attributes property."""
        data = DQAReportData("test.csv", "pfi", "sn", "t")
        
        data.attributes = ["attr1", "attr2"]
        assert data.attributes == ["attr1", "attr2"]
    
    def test_report_data_missings(self):
        """Test missings property."""
        data = DQAReportData("test.csv", "pfi", "sn", "t")
        
        data.missings = [1, 2, 3]
        assert data.missings == [1, 2, 3]
    
    def test_report_data_uniques(self):
        """Test uniques property."""
        data = DQAReportData("test.csv", "pfi", "sn", "t")
        
        data.uniques = [10, 20, 30]
        assert data.uniques == [10, 20, 30]
    
    def test_report_data_all_checks_ok(self):
        """Test AllChecksOK property."""
        data = DQAReportData("test.csv", "pfi", "sn", "t")
        
        data.AllChecksOK = True
        assert data.AllChecksOK is True
        
        data.AllChecksOK = False
        assert data.AllChecksOK is False
    
    def test_report_data_ratio_calculation(self):
        """Test getRatioValCount calculation."""
        data = DQAReportData("test.csv", "pfi", "sn", "t")
        data.RowCount = 100
        
        result = data.getRatioValCount(25)
        assert "25" in result
        assert "100" in result
        assert "25.0%" in result


class TestPDFReportBuilder:
    """Test suite for PDFReportBuilder class."""
    
    def test_builder_creation(self):
        """Test PDFReportBuilder can be created."""
        builder = PDFReportBuilder()
        assert builder is not None
        assert builder.WIDTH == 210
        assert builder.HEIGHT == 297
    
    def test_builder_add_page(self):
        """Test adding a page."""
        builder = PDFReportBuilder()
        builder.add_page()
        assert builder.page_no() == 1
    
    def test_builder_insert_title(self):
        """Test inserting a title (no error)."""
        builder = PDFReportBuilder()
        builder.add_page()
        builder.insert_title("Test Title")
        # Just checking no exception is raised
    
    def test_builder_insert_text_and_value(self):
        """Test inserting text and value."""
        builder = PDFReportBuilder()
        builder.add_page()
        builder.insert_text_and_value("Label:", "Value")
        # Just checking no exception is raised
    
    def test_builder_backward_compatibility(self):
        """Test backward compatibility aliases."""
        builder = PDFReportBuilder()
        builder.add_page()
        
        # Test aliases exist and work
        builder.insertTitle("Title")
        builder.insertTextAndValue("Label", "Value")
        builder.addBreak()
    
    def test_builder_output(self, temp_dir):
        """Test PDF output generation."""
        builder = PDFReportBuilder()
        builder.add_page()
        builder.insert_title("Test Report")
        
        output_path = os.path.join(temp_dir, "test_report.pdf")
        builder.output(output_path, 'F')
        
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0


class TestPDFReportBuilderAlias:
    """Test backward compatibility alias for PDF builder."""
    
    def test_dqa4bppi_alias(self):
        """Test DQA4BPPIReportBuilder alias exists."""
        from pydqa4pm.reports.pdf_builder import DQA4BPPIReportBuilder
        assert DQA4BPPIReportBuilder is PDFReportBuilder


"""
Integration tests for pyDQA4ProcessMining.

These tests verify the complete workflow from end to end.
"""

import os
import pytest
import tempfile
import shutil
from pydqa4pm import Dqa4PM, Logger, DataSource, DQAReportData
from pydqa4pm.reports import ReportStore, PDFReportBuilder
from pydqa4pm.utils import constants as C


class TestEndToEndWorkflow:
    """End-to-end workflow tests."""
    
    def test_complete_analysis_workflow(self, temp_csv_file, temp_dir):
        """Test complete analysis from file to report."""
        # Copy test file to temp dir
        test_csv = os.path.join(temp_dir, "analysis_test.csv")
        shutil.copy(temp_csv_file, test_csv)
        
        # Initialize
        logger = Logger("integration_test")
        dqa = Dqa4PM(logger)
        
        # Run full process
        dqa.process(test_csv, ",", "case_id", "activity", "timestamp")
        
        # Verify output files exist
        base_name = test_csv.replace(".csv", "")
        
        # Check events file
        events_file = base_name + "-events.csv"
        assert os.path.exists(events_file), f"Events file not found: {events_file}"
        
        # Check reject files (may be empty but should exist)
        read_rejects = base_name + "-read.rejects"
        keys_rejects = base_name + "-3keys.rejects"
        assert os.path.exists(read_rejects), f"Read rejects not found: {read_rejects}"
        assert os.path.exists(keys_rejects), f"Keys rejects not found: {keys_rejects}"
    
    def test_step_by_step_workflow(self, temp_csv_file, temp_dir):
        """Test step-by-step workflow using API."""
        # Copy test file
        test_csv = os.path.join(temp_dir, "step_test.csv")
        shutil.copy(temp_csv_file, test_csv)
        
        # Step 1: Initialize
        logger = Logger("step_test")
        dqa = Dqa4PM(logger)
        
        # Step 2: Open dataset
        ds = dqa.open_dataset(test_csv, ",", "case_id", "activity", "timestamp")
        assert ds.isOpened()
        
        # Step 3: Initialize storage
        store = ReportStore()
        store._ReportStore__tempPath = os.path.join(temp_dir, "temp/")
        store.initialize()
        
        # Step 4: Make DQA checks
        report_data = dqa.make_dqa_checks(ds)
        assert report_data.AllChecksOK
        
        # Step 5: Create events file
        dqa.create_alternative_data(ds)
        assert os.path.exists(ds.uniqueEventsFilename)
        
        # Step 6: Build charts
        success = dqa.build_charts(report_data, store)
        assert success
        
        # Step 7: Generate report
        report_name = ds.filenameWithoutExt + C.SUFFIX_REPORT
        dqa.generate_report(report_data, report_name)
        assert os.path.exists(report_name)
        
        # Cleanup
        store.finalize()


class TestDataSourceIntegration:
    """Integration tests for DataSource."""
    
    def test_datasource_full_analysis(self, temp_csv_file):
        """Test DataSource performs full analysis."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        
        # Check keys
        valid, msg = ds.check3PKeys()
        assert valid
        
        # Get all statistics
        assert ds.rowsCount() > 0
        assert ds.colsCount() > 0
        assert ds.countDistinctValues("case_id") > 0
        assert ds.countDistinctValues("activity") > 0
        
        # Check date formats
        date_check = ds.checkBPPIDateFormats()
        assert len(date_check) == len(C.FMT)
        
        # Get frequency distributions
        freq_pfi = ds.getCountValuesForField("case_id")
        assert len(freq_pfi) > 0
        
        freq_sn = ds.getCountValuesForField("activity")
        assert len(freq_sn) > 0


class TestReportDataIntegration:
    """Integration tests for report data generation."""
    
    def test_report_data_population(self, temp_csv_file):
        """Test DQAReportData is properly populated."""
        logger = Logger("report_data_test")
        dqa = Dqa4PM(logger)
        
        ds = dqa.open_dataset(temp_csv_file, ",", "case_id", "activity", "timestamp")
        report_data = dqa.make_dqa_checks(ds)
        
        # Verify all data is populated
        assert report_data.RowCount > 0
        assert report_data.ColCount > 0
        assert report_data.AllChecksOK
        assert isinstance(report_data.missings, list)
        assert isinstance(report_data.uniques, list)
        assert len(report_data.attributes) >= 0


class TestPDFGenerationIntegration:
    """Integration tests for PDF report generation."""
    
    def test_pdf_report_generation(self, temp_csv_file, temp_dir):
        """Test PDF report is generated correctly."""
        test_csv = os.path.join(temp_dir, "pdf_test.csv")
        shutil.copy(temp_csv_file, test_csv)
        
        logger = Logger("pdf_test")
        dqa = Dqa4PM(logger)
        
        # Run full workflow
        dqa.process(test_csv, ",", "case_id", "activity", "timestamp")
        
        # Check PDF exists
        pdf_path = test_csv.replace(".csv", "-report.pdf")
        assert os.path.exists(pdf_path)
        
        # Check PDF has content
        assert os.path.getsize(pdf_path) > 1000  # Should be > 1KB


class TestImportStructure:
    """Test import structure and package organization."""
    
    def test_main_imports(self):
        """Test main package imports work."""
        from pydqa4pm import Dqa4PM, DataSource, DQAReportData, Logger
        
        assert Dqa4PM is not None
        assert DataSource is not None
        assert DQAReportData is not None
        assert Logger is not None
    
    def test_submodule_imports(self):
        """Test submodule imports work."""
        from pydqa4pm.core import Dqa4PM, DataSource, DQAReportData
        from pydqa4pm.charts import Chart, SeabornChart, MatplotlibChart
        from pydqa4pm.reports import PDFReportBuilder, ReportStore
        from pydqa4pm.utils import Logger, constants, SNList
        
        assert all([
            Dqa4PM, DataSource, DQAReportData,
            Chart, SeabornChart, MatplotlibChart,
            PDFReportBuilder, ReportStore,
            Logger, constants, SNList
        ])
    
    def test_version_exists(self):
        """Test version is defined."""
        from pydqa4pm import __version__
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert "." in __version__


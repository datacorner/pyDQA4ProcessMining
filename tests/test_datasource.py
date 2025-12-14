"""
Tests for pydqa4pm.core.datasource module.
"""

import os
import pytest
import pandas as pd
from pydqa4pm.core.datasource import DataSource, check_date_format
from pydqa4pm.utils import constants as C


class TestCheckDateFormat:
    """Test suite for check_date_format utility function."""
    
    def test_valid_date_format_1(self):
        """Test date format: %Y-%m-%d %H:%M:%S."""
        assert check_date_format("2023-12-25 14:30:00", "%Y-%m-%d %H:%M:%S") is True
    
    def test_valid_date_format_iso(self):
        """Test ISO date format."""
        assert check_date_format("2023-12-25T14:30:00", "%Y-%m-%dT%H:%M:%S") is True
    
    def test_invalid_date_format(self):
        """Test invalid date format returns False."""
        assert check_date_format("not a date", "%Y-%m-%d %H:%M:%S") is False
    
    def test_wrong_format(self):
        """Test date with wrong format returns False."""
        assert check_date_format("2023-12-25", "%Y-%m-%d %H:%M:%S") is False
    
    def test_empty_string(self):
        """Test empty string returns False."""
        assert check_date_format("", "%Y-%m-%d %H:%M:%S") is False
    
    def test_none_value(self):
        """Test None value returns False."""
        assert check_date_format(None, "%Y-%m-%d %H:%M:%S") is False


class TestDataSource:
    """Test suite for DataSource class."""
    
    def test_datasource_creation(self, temp_csv_file):
        """Test DataSource can be created."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        assert ds is not None
        assert ds.filename == temp_csv_file
    
    def test_datasource_properties(self, temp_csv_file):
        """Test DataSource properties."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        assert ds.PFI == "case_id"
        assert ds.SN == "activity"
        assert ds.T == "timestamp"
    
    def test_datasource_open(self, temp_csv_file):
        """Test DataSource can open a CSV file."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        success, error = ds.open(",")
        assert success is True
        assert error is None
        assert ds.isOpened() is True
    
    def test_datasource_is_opened_alias(self, temp_csv_file):
        """Test is_opened() alias works."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        assert ds.is_opened() is True
    
    def test_datasource_not_opened_initially(self, temp_csv_file):
        """Test DataSource is not opened initially."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        assert ds.isOpened() is False
    
    def test_datasource_row_count(self, temp_csv_file):
        """Test row count after opening."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        assert ds.rowsCount() == 5
        assert ds.rows_count() == 5
    
    def test_datasource_col_count(self, temp_csv_file):
        """Test column count after opening."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        assert ds.colsCount() == 4  # case_id, activity, timestamp, amount
        assert ds.cols_count() == 4
    
    def test_datasource_check3pkeys_success(self, temp_csv_file):
        """Test check3PKeys with valid columns."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        valid, message = ds.check3PKeys()
        assert valid is True
        assert message == ""
    
    def test_datasource_check3pkeys_failure(self, temp_csv_file):
        """Test check3PKeys with invalid column."""
        ds = DataSource(temp_csv_file, "nonexistent", "activity", "timestamp")
        ds.open(",")
        valid, message = ds.check3PKeys()
        assert valid is False
        assert "Timeline ID" in message
    
    def test_datasource_attributes(self, temp_csv_file):
        """Test attributes property returns non-key columns."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        ds.check3PKeys()
        assert "amount" in ds.attributes
        assert "case_id" not in ds.attributes
    
    def test_datasource_head(self, temp_csv_file):
        """Test head method returns first rows."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        head = ds.head(3)
        assert len(head) == 3
        assert isinstance(head, pd.DataFrame)
    
    def test_datasource_filename_without_ext(self, temp_csv_file):
        """Test filenameWithoutExt property."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        assert ds.filenameWithoutExt.endswith("test_data")
        assert not ds.filenameWithoutExt.endswith(".csv")


class TestDataSourceAnalysis:
    """Test DataSource analysis methods."""
    
    def test_count_distinct_values(self, temp_csv_file):
        """Test counting distinct values."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        
        case_distinct = ds.countDistinctValues("case_id")
        assert case_distinct == 3  # C001, C002, C003
        
        activity_distinct = ds.countDistinctValues("activity")
        assert activity_distinct == 2  # Start, End
    
    def test_count_unique_values(self, temp_csv_file):
        """Test counting unique values."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        
        unique = ds.countUniqueValues("case_id")
        assert unique == 3
    
    def test_get_count_values_for_field(self, temp_csv_file):
        """Test frequency distribution."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        
        freq = ds.getCountValuesForField("activity")
        assert freq is not None
        assert C.FLD_COL_VALUECOUNT in freq.columns
        assert C.FLD_FREQ_VALUECOUNT in freq.columns
    
    def test_get_count_values_with_limit(self, temp_csv_file):
        """Test frequency distribution with limit."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        
        freq = ds.getCountValuesForField("activity", limit=1)
        assert len(freq) == 1
    
    def test_check_duplicates_count_no_dups(self, temp_csv_file):
        """Test duplicate count with no duplicates."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        
        dups = ds.checkDuplicatesCount()
        assert dups == 0
    
    def test_check_duplicates_count_with_dups(self, temp_csv_with_duplicates):
        """Test duplicate count with duplicates."""
        ds = DataSource(temp_csv_with_duplicates, "case_id", "activity", "timestamp")
        ds.open(",")
        
        dups = ds.checkDuplicatesCount()
        assert dups == 2  # 2 duplicate rows
    
    def test_missing_values(self, temp_csv_with_nulls):
        """Test missing values detection."""
        ds = DataSource(temp_csv_with_nulls, "case_id", "activity", "timestamp")
        ds.open(",")
        
        missing = ds.missingValues()
        assert len(missing) == 3
        assert missing[0] == 1  # 1 missing case_id
        assert missing[1] == 1  # 1 missing activity
        assert missing[2] == 1  # 1 missing timestamp
    
    def test_check_date_formats(self, temp_csv_file):
        """Test date format checking."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        
        formats = ds.checkBPPIDateFormats()
        assert isinstance(formats, pd.DataFrame)
        assert "Format" in formats.columns
        assert "GoodRows" in formats.columns


class TestDataSourceRejects:
    """Test DataSource reject file generation."""
    
    def test_read_rejects_count_clean_file(self, temp_csv_file):
        """Test read rejects count with clean file."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        ds.open(",")
        assert ds.readRejectsCount == 0
    
    def test_reject_filenames(self, temp_csv_file):
        """Test reject filename generation."""
        ds = DataSource(temp_csv_file, "case_id", "activity", "timestamp")
        
        assert ds.readRejectFilename.endswith("-read.rejects")
        assert ds.keysRejectFilename.endswith("-3keys.rejects")
        assert ds.uniqueEventsFilename.endswith("-events.csv")


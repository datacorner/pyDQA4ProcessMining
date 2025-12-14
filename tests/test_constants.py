"""
Tests for pydqa4pm.utils.constants module.
"""

import pytest
from pydqa4pm.utils import constants as C


class TestConstants:
    """Test suite for constants module."""
    
    def test_logging_constants_exist(self):
        """Test that logging constants are defined."""
        assert hasattr(C, 'ENCODING')
        assert hasattr(C, 'TRACE_LEVEL')
        assert hasattr(C, 'TRACE_FORMAT')
        assert hasattr(C, 'TRACE_FILENAME')
    
    def test_encoding_is_utf8(self):
        """Test that encoding is UTF-8."""
        assert C.ENCODING == "utf-8"
    
    def test_display_limit_is_positive(self):
        """Test that display limit is a positive integer."""
        assert isinstance(C.LIMIT_BARH_DISPLAY, int)
        assert C.LIMIT_BARH_DISPLAY > 0
    
    def test_field_names_defined(self):
        """Test that DataFrame field names are defined."""
        assert C.FLD_COL_VALUECOUNT == "Column"
        assert C.FLD_FREQ_VALUECOUNT == "Frequency"
        assert C.FLD_NEW_SN == "New Event"
        assert C.FLD_PFI_NB == "Nb Of Timeline"
        assert C.FLD_SN_NB == "Nb Of events"
    
    def test_file_suffixes_defined(self):
        """Test that file suffixes are defined correctly."""
        assert C.SUFFIX_3KEYS_REJECT == "-3keys.rejects"
        assert C.SUFFIX_REPORT == "-report.pdf"
        assert C.SUFFIX_READ_REJ == "-read.rejects"
        assert C.SUFFIX_EVENTS == "-events.csv"
    
    def test_date_formats_list(self):
        """Test that date formats list is defined and not empty."""
        assert isinstance(C.FMT, list)
        assert len(C.FMT) >= 7
    
    def test_date_formats_valid_strings(self):
        """Test that all date formats are valid strings containing %."""
        for fmt in C.FMT:
            assert isinstance(fmt, str)
            assert "%" in fmt
    
    def test_iso_formats_included(self):
        """Test that ISO date formats are included."""
        iso_formats = [f for f in C.FMT if "T" in f]
        assert len(iso_formats) >= 1
    
    def test_noise_characters_defined(self):
        """Test that noise characters string is defined."""
        assert hasattr(C, 'NOISE_CHARACTERS')
        assert isinstance(C.NOISE_CHARACTERS, str)
        assert len(C.NOISE_CHARACTERS) > 0
    
    def test_noise_contains_punctuation(self):
        """Test that noise characters contain common punctuation."""
        assert "," in C.NOISE_CHARACTERS
        assert "." in C.NOISE_CHARACTERS
        assert "?" in C.NOISE_CHARACTERS
        assert "!" in C.NOISE_CHARACTERS
    
    def test_temp_file_names_defined(self):
        """Test that temporary file names are defined."""
        assert hasattr(C, 'FILE_FORMAT_TABLE')
        assert hasattr(C, 'FILE_SAMPLES_TABLE')
        assert hasattr(C, 'FILE_PFI_CHART')
        assert hasattr(C, 'FILE_SNMOSTFQ_CHART')
    
    def test_temp_file_names_have_extension(self):
        """Test that temp file names have image extensions."""
        assert C.FILE_FORMAT_TABLE.endswith('.jpg')
        assert C.FILE_SAMPLES_TABLE.endswith('.jpg')
        assert C.FILE_PFI_CHART.endswith('.jpg')


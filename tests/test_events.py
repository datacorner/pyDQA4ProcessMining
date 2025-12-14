"""
Tests for pydqa4pm.utils.events module.
"""

import pytest
import pandas as pd
from pydqa4pm.utils.events import SNList
from pydqa4pm.utils import constants as C


class TestSNList:
    """Test suite for SNList class."""
    
    def test_snlist_creation(self, sample_events_df):
        """Test that SNList can be created."""
        sn_list = SNList(sample_events_df)
        assert sn_list is not None
        assert sn_list.SNList is not None
    
    def test_snlist_has_new_event_column(self, sample_events_df):
        """Test that SNList creates New Event column."""
        sn_list = SNList(sample_events_df)
        assert C.FLD_NEW_SN in sn_list.SNList.columns
    
    def test_snlist_preserves_original_columns(self, sample_events_df):
        """Test that original columns are preserved."""
        sn_list = SNList(sample_events_df)
        assert C.FLD_COL_VALUECOUNT in sn_list.SNList.columns
        assert C.FLD_FREQ_VALUECOUNT in sn_list.SNList.columns
    
    def test_snlist_cleanse_removes_punctuation(self):
        """Test that cleanse removes punctuation."""
        df = pd.DataFrame({
            C.FLD_COL_VALUECOUNT: ["Start!", "End?", "Review,Check"],
            C.FLD_FREQ_VALUECOUNT: [10, 20, 30]
        })
        sn_list = SNList(df)
        sn_list.cleanse()
        
        new_events = sn_list.SNList[C.FLD_NEW_SN].tolist()
        # Check each event individually for punctuation
        for event in new_events:
            assert "!" not in event
            assert "?" not in event
            # Comma should be removed from individual event names
        assert "Review,Check" not in new_events  # Original with comma should not exist
    
    def test_snlist_cleanse_capitalizes(self):
        """Test that cleanse capitalizes first letter."""
        df = pd.DataFrame({
            C.FLD_COL_VALUECOUNT: ["start process", "END PROCESS"],
            C.FLD_FREQ_VALUECOUNT: [10, 20]
        })
        sn_list = SNList(df)
        sn_list.cleanse()
        
        new_events = sn_list.SNList[C.FLD_NEW_SN].tolist()
        assert new_events[0][0].isupper()
    
    def test_snlist_cleanse_removes_multiple_spaces(self):
        """Test that cleanse removes multiple spaces."""
        df = pd.DataFrame({
            C.FLD_COL_VALUECOUNT: ["Start    Process", "End  Now"],
            C.FLD_FREQ_VALUECOUNT: [10, 20]
        })
        sn_list = SNList(df)
        sn_list.cleanse()
        
        new_events = sn_list.SNList[C.FLD_NEW_SN].tolist()
        assert "    " not in new_events[0]
        assert "  " not in new_events[1]
    
    def test_snlist_empty_dataframe(self):
        """Test SNList with empty DataFrame."""
        df = pd.DataFrame(columns=[C.FLD_COL_VALUECOUNT, C.FLD_FREQ_VALUECOUNT])
        sn_list = SNList(df)
        assert sn_list.SNList.empty
    
    def test_remove_noise_function(self):
        """Test the remove_noise method directly."""
        df = pd.DataFrame({
            C.FLD_COL_VALUECOUNT: ["Test"],
            C.FLD_FREQ_VALUECOUNT: [1]
        })
        sn_list = SNList(df)
        
        # Use snake_case method name
        result = sn_list.remove_noise("Hello!  World?  Test.")
        assert "!" not in result
        assert "?" not in result
        assert "." not in result
        assert "  " not in result
    
    def test_remove_noise_strips_whitespace(self):
        """Test that remove_noise strips leading/trailing whitespace."""
        df = pd.DataFrame({
            C.FLD_COL_VALUECOUNT: ["Test"],
            C.FLD_FREQ_VALUECOUNT: [1]
        })
        sn_list = SNList(df)
        
        # Use snake_case method name
        result = sn_list.remove_noise("  Hello World  ")
        assert not result.startswith(" ")
        assert not result.endswith(" ")


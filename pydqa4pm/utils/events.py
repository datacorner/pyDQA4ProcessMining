"""
Event list management for pyDQA4ProcessMining.

Provides functionality to manage and cleanse event/activity names from process logs.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import re
import pandas as pd
from pydqa4pm.utils import constants as C


class SNList:
    """
    Manages a list of events (Step Names) with cleansing capabilities.
    
    This class stores events in a DataFrame with columns:
    - FLD_COL_VALUECOUNT: Original event name
    - FLD_FREQ_VALUECOUNT: Frequency of the event
    - FLD_NEW_SN: Cleansed/standardized event name
    
    Attributes:
        SNList: DataFrame containing the events and their frequencies.
    
    Example:
        >>> events_df = datasource.getCountValuesForField("activity")
        >>> sn_list = SNList(events_df)
        >>> sn_list.cleanse()
        >>> sn_list.SNList.to_csv("events.csv")
    """
    
    def __init__(self, df_events_list: pd.DataFrame):
        """
        Initialize the event list from a DataFrame.
        
        Args:
            df_events_list: DataFrame with event names and frequencies.
        """
        self._sn_list = df_events_list
        if not self._sn_list.empty:
            # Create a column for the cleansed event name
            self._sn_list.insert(1, C.FLD_NEW_SN, self._sn_list[C.FLD_COL_VALUECOUNT])
    
    @property
    def SNList(self) -> pd.DataFrame:
        """Get the DataFrame with all events."""
        return self._sn_list
    
    def remove_noise(self, text: str, remove_punctuation: bool = True, 
                     collapse_spaces: bool = True) -> str:
        """
        Remove noise characters and normalize whitespace from event names.
        
        Args:
            text: The event name to clean.
            remove_punctuation: Whether to remove punctuation characters.
            collapse_spaces: Whether to replace multiple spaces with single space.
        
        Returns:
            Cleaned and capitalized event name.
        """
        result = str(text)
        
        # Remove noise punctuation characters
        if remove_punctuation:
            for char in C.NOISE_CHARACTERS:
                result = result.replace(char, "")
        
        # Collapse multiple spaces into one
        if collapse_spaces:
            result = re.sub(r"\s+", " ", result).strip()
        
        return result.strip().capitalize()
    
    def cleanse(self) -> None:
        """
        Apply noise removal to all event names.
        
        Updates the FLD_NEW_SN column with cleansed versions of event names.
        """
        self._sn_list[C.FLD_NEW_SN] = self._sn_list[C.FLD_COL_VALUECOUNT].apply(
            self.remove_noise
        )
    
    # Alias for backward compatibility
    Cleanse = cleanse


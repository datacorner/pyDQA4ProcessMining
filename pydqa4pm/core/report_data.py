"""
Report data container for pyDQA4ProcessMining.

Provides the DQAReportData class that stores all data needed to generate the DQA report.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from typing import List

import pandas as pd

from pydqa4pm.utils import constants as C


class DQAReportData:
    """
    Container for all data quality assessment results.
    
    This class stores all metrics, statistics, and chart references needed
    to generate the final PDF report.
    
    Attributes:
        filename: The analyzed CSV file path.
        PFIKey: Timeline ID column name.
        SNKey: Event ID column name.
        TKey: Timestamp column name.
        RowCount: Total number of rows.
        ColCount: Total number of columns.
        AllChecksOK: Whether all checks passed successfully.
    """
    
    def __init__(self, filename: str, pfi: str, sn: str, t: str):
        """
        Initialize the report data container.
        
        Args:
            filename: Path to the analyzed CSV file.
            pfi: Timeline ID column name.
            sn: Event ID column name.
            t: Timestamp column name.
        """
        self._filename = filename
        self._PFIKey = pfi
        self._SNKey = sn
        self._TKey = t
        
        # Counts
        self._RowCount = 0
        self._ColCount = 0
        self._DuplicateCount = 0
        self._rejects = 0
        self._PFINbOfDistinctValue = 0
        self._SNNbOfDistinctValue = 0
        
        # Chart file paths
        self._chartPFIValCount = C.NO_CHART_FILE
        self._chartSNValCount = C.NO_CHART_FILE
        self._tableSampleData = C.NO_CHART_FILE
        self._chartDatesFormat = C.NO_CHART_FILE
        self._chartAggSNPerPFISIze = C.NO_CHART_FILE
        
        # DataFrames
        self._dataFormatsCheck = pd.DataFrame()
        self._firstData = pd.DataFrame()
        self._SNValues = pd.DataFrame()
        self._PFIMostFreq = pd.DataFrame()
        self._PFICountPerSN = pd.DataFrame()
        
        # Lists
        self._missingValues = [0, 0, 0]  # [PFI, SN, T]
        self._uniquesValues = [0, 0, 0]  # [PFI, SN, T]
        self._attributes: List[str] = []
        
        # Status
        self._allchecksOK = False

    # =========================================================================
    # DataFrame Properties
    # =========================================================================
    
    @property
    def PFICountPerSN(self) -> pd.DataFrame:
        """Timeline size distribution data."""
        return self._PFICountPerSN
    
    @PFICountPerSN.setter
    def PFICountPerSN(self, value: pd.DataFrame):
        self._PFICountPerSN = value

    @property
    def PFIMostFreq(self) -> pd.DataFrame:
        """Most frequent timeline IDs."""
        return self._PFIMostFreq
    
    @PFIMostFreq.setter
    def PFIMostFreq(self, value: pd.DataFrame):
        self._PFIMostFreq = value

    @property
    def SNValues(self) -> pd.DataFrame:
        """Event frequency distribution."""
        return self._SNValues
    
    @SNValues.setter
    def SNValues(self, value: pd.DataFrame):
        self._SNValues = value

    @property
    def firstData(self) -> pd.DataFrame:
        """Sample data (first rows)."""
        return self._firstData
    
    @firstData.setter
    def firstData(self, value: pd.DataFrame):
        self._firstData = value

    @property
    def dateFormatsCheck(self) -> pd.DataFrame:
        """Date format validation results."""
        return self._dataFormatsCheck
    
    @dateFormatsCheck.setter
    def dateFormatsCheck(self, value: pd.DataFrame):
        self._dataFormatsCheck = value

    # =========================================================================
    # Status and Metadata Properties
    # =========================================================================
    
    @property
    def AllChecksOK(self) -> bool:
        """Whether all quality checks passed."""
        return self._allchecksOK
    
    @AllChecksOK.setter
    def AllChecksOK(self, value: bool):
        self._allchecksOK = value

    @property
    def attributes(self) -> List[str]:
        """List of non-key column names."""
        return self._attributes
    
    @attributes.setter
    def attributes(self, value: List[str]):
        self._attributes = value

    @property
    def filename(self) -> str:
        """Path to the analyzed file."""
        return self._filename

    @property
    def PFIKey(self) -> str:
        """Timeline ID column name."""
        return self._PFIKey
    
    @property
    def SNKey(self) -> str:
        """Event ID column name."""
        return self._SNKey
    
    @property
    def TKey(self) -> str:
        """Timestamp column name."""
        return self._TKey

    # =========================================================================
    # Count Properties with Ratio Display
    # =========================================================================
    
    def _get_ratio_display(self, value: int) -> str:
        """Format a value with its percentage of total rows."""
        if self._RowCount == 0:
            return f"{value} / 0 (0%)"
        percentage = round(value / self._RowCount * 100, 2)
        return f"{value} / {self._RowCount} ({percentage}%)"

    @property
    def rejects(self) -> str:
        """Number of rejected rows with percentage."""
        return self._get_ratio_display(self._rejects)
    
    @rejects.setter
    def rejects(self, value: int):
        self._rejects = value

    @property
    def duplicates(self) -> str:
        """Number of duplicate rows with percentage."""
        return self._get_ratio_display(self._DuplicateCount)
    
    @duplicates.setter
    def duplicates(self, value: int):
        self._DuplicateCount = value

    @property
    def RowCount(self) -> int:
        """Total number of rows."""
        return self._RowCount
    
    @RowCount.setter
    def RowCount(self, value: int):
        self._RowCount = value

    @property
    def ColCount(self) -> int:
        """Total number of columns."""
        return self._ColCount
    
    @ColCount.setter
    def ColCount(self, value: int):
        self._ColCount = value

    @property
    def distinctPFI(self) -> str:
        """Number of distinct timeline IDs with percentage."""
        return self._get_ratio_display(self._PFINbOfDistinctValue)
    
    @distinctPFI.setter
    def distinctPFI(self, value: int):
        self._PFINbOfDistinctValue = value

    @property
    def distinctSN(self) -> str:
        """Number of distinct event IDs with percentage."""
        return self._get_ratio_display(self._SNNbOfDistinctValue)
    
    @distinctSN.setter
    def distinctSN(self, value: int):
        self._SNNbOfDistinctValue = value

    # =========================================================================
    # Chart Path Properties
    # =========================================================================
    
    @property
    def chartAggSNPerPFISIze(self) -> str:
        """Path to timeline size chart."""
        return self._chartAggSNPerPFISIze
    
    @chartAggSNPerPFISIze.setter
    def chartAggSNPerPFISIze(self, value: str):
        self._chartAggSNPerPFISIze = value

    @property
    def chartPFIValCount(self) -> str:
        """Path to PFI frequency chart."""
        return self._chartPFIValCount
    
    @chartPFIValCount.setter
    def chartPFIValCount(self, value: str):
        self._chartPFIValCount = value

    @property
    def chartSNValCount(self) -> str:
        """Path to SN frequency chart."""
        return self._chartSNValCount
    
    @chartSNValCount.setter
    def chartSNValCount(self, value: str):
        self._chartSNValCount = value

    @property
    def tableSampleData(self) -> str:
        """Path to sample data table image."""
        return self._tableSampleData
    
    @tableSampleData.setter
    def tableSampleData(self, value: str):
        self._tableSampleData = value

    @property
    def chartDatesFormat(self) -> str:
        """Path to date format check table image."""
        return self._chartDatesFormat
    
    @chartDatesFormat.setter
    def chartDatesFormat(self, value: str):
        self._chartDatesFormat = value

    # =========================================================================
    # List Properties
    # =========================================================================
    
    @property
    def uniques(self) -> List[int]:
        """Unique value counts [PFI, SN, T]."""
        return self._uniquesValues
    
    @uniques.setter
    def uniques(self, value: List[int]):
        self._uniquesValues = value

    @property
    def missings(self) -> List[int]:
        """Missing value counts [PFI, SN, T]."""
        return self._missingValues
    
    @missings.setter
    def missings(self, value: List[int]):
        self._missingValues = value
    
    # Backward compatibility alias
    def getRatioValCount(self, value: int) -> str:
        """Format a value with its percentage of total rows."""
        return self._get_ratio_display(value)


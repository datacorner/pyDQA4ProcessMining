"""
Data source management for pyDQA4ProcessMining.

Provides the DataSource class for loading, validating, and analyzing CSV datasets.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from datetime import datetime
from typing import List, Optional, Tuple

import pandas as pd

from pydqa4pm.utils import constants as C
from pydqa4pm.utils.events import SNList


def check_date_format(date_str: str, fmt: str) -> bool:
    """
    Check if a date string matches a given format.
    
    Args:
        date_str: The date string to validate.
        fmt: The expected format string.
    
    Returns:
        True if the date matches the format, False otherwise.
    """
    try:
        datetime.strptime(str(date_str), fmt)
        return True
    except (ValueError, TypeError):
        return False


class DataSource:
    """
    Manages CSV data source loading, validation, and analysis.
    
    This class handles:
    - Loading CSV files with error handling for malformed rows
    - Validating the presence of required process mining keys
    - Analyzing data quality metrics (duplicates, missing values, etc.)
    - Generating reject files for problematic rows
    
    Attributes:
        PFI: The Timeline ID column name.
        SN: The Event ID column name.
        T: The Timestamp column name.
        filename: Path to the CSV file.
        attributes: List of non-key column names.
    
    Example:
        >>> ds = DataSource("data.csv", "case_id", "activity", "timestamp")
        >>> ds.open(",")
        >>> if ds.is_opened():
        ...     print(f"Rows: {ds.rows_count()}")
        ...     print(f"Duplicates: {ds.check_duplicates_count()}")
    """
    
    def __init__(self, filename: str, pfi: str, sn: str, t: str):
        """
        Initialize the data source.
        
        Args:
            filename: Path to the CSV file.
            pfi: Column name for Timeline ID (Process Flow Identifier).
            sn: Column name for Event ID (Step Name).
            t: Column name for Timestamp.
        """
        self._filename = filename
        self._dataset = pd.DataFrame()
        self._keyname_PFI = pfi
        self._keyname_SN = sn
        self._keyname_T = t
        self._initial_row_count = 0
        self._potential_attributes: List[str] = []
        self._read_rejects: List = []

    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def readRejectsCount(self) -> int:
        """Number of rows rejected during file reading."""
        return len(self._read_rejects)
    
    @property
    def readRejectFilename(self) -> str:
        """Path to the read rejects file."""
        return self.filenameWithoutExt + C.SUFFIX_READ_REJ
    
    @property
    def keysRejectFilename(self) -> str:
        """Path to the key validation rejects file."""
        return self.filenameWithoutExt + C.SUFFIX_3KEYS_REJECT
    
    @property
    def uniqueEventsFilename(self) -> str:
        """Path to the unique events file."""
        return self.filenameWithoutExt + C.SUFFIX_EVENTS

    @property
    def PFI(self) -> str:
        """Timeline ID column name."""
        return self._keyname_PFI
    
    @property
    def SN(self) -> str:
        """Event ID column name."""
        return self._keyname_SN
    
    @property
    def T(self) -> str:
        """Timestamp column name."""
        return self._keyname_T
    
    @property
    def filename(self) -> str:
        """Path to the CSV file."""
        return self._filename
    
    @property
    def attributes(self) -> List[str]:
        """List of non-key column names (potential attributes)."""
        return self._potential_attributes
    
    @property
    def filenameWithoutExt(self) -> str:
        """Filename without extension."""
        try:
            return '.'.join(self._filename.split('.')[:-1])
        except Exception:
            return C.DEFAULT_REPORT_FILE
    
    @property
    def rejectRows(self) -> int:
        """Number of rows rejected after key validation."""
        return self._initial_row_count - self._dataset.shape[0]

    # =========================================================================
    # Core Methods
    # =========================================================================
    
    def isOpened(self) -> bool:
        """Check if the dataset was successfully loaded."""
        return not self._dataset.empty
    
    # Alias
    def is_opened(self) -> bool:
        """Check if the dataset was successfully loaded."""
        return self.isOpened()
    
    def open(self, sep: str = ",") -> Tuple[bool, Optional[Exception]]:
        """
        Open and load the CSV file.
        
        Args:
            sep: The field separator character.
        
        Returns:
            Tuple of (success, error) where error is None on success.
        """
        try:
            self._dataset = pd.read_csv(
                self._filename,
                on_bad_lines=self._add_read_reject,
                engine='python',
                sep=sep
            )
            self._initial_row_count = self._dataset.shape[0]
            self._dump_read_rejects()
            return True, None
        except Exception as e:
            return False, e
    
    def _add_read_reject(self, row) -> None:
        """Callback for handling malformed CSV rows."""
        self._read_rejects.append(row)
    
    # Backward compatibility alias
    def addReadRejectLine(self, x):
        self._add_read_reject(x)
    
    def _dump_read_rejects(self) -> int:
        """Write rejected rows to the read rejects file."""
        with open(self.readRejectFilename, 'w') as reject_file:
            for item in self._read_rejects:
                line = f"{item} > {len(item)} columns\n"
                reject_file.write(line)
        return len(self._read_rejects)
    
    # Backward compatibility alias
    def dumpReadRejects(self) -> int:
        return self._dump_read_rejects()

    # =========================================================================
    # Validation Methods
    # =========================================================================
    
    def check3PKeys(self) -> Tuple[bool, str]:
        """
        Validate that all three mandatory columns exist in the dataset.
        
        Returns:
            Tuple of (success, error_message) where error_message is empty on success.
        """
        pfi_ok, sn_ok, t_ok = False, False, False
        msg = ""
        
        try:
            for col in self._dataset.columns:
                if col == self._keyname_PFI:
                    pfi_ok = True
                elif col == self._keyname_SN:
                    sn_ok = True
                elif col == self._keyname_T:
                    t_ok = True
                else:
                    self._potential_attributes.append(col)
            
            if not pfi_ok:
                msg += "Timeline ID column has not been found.\n"
            if not sn_ok:
                msg += "Event ID column has not been found.\n"
            if not t_ok:
                msg += "Timestamp column has not been found."
            
            return (pfi_ok and sn_ok and t_ok), msg
            
        except Exception as e:
            return False, f"Error while validating columns: {e}"
    
    def checkBPPIDateFormats(self) -> pd.DataFrame:
        """
        Check timestamps against all supported date formats.
        
        Returns:
            DataFrame with format strings and count of matching rows.
        """
        df = self._dataset.copy()
        result = []
        
        for i, fmt in enumerate(C.FMT):
            col_name = f"FMT_{i}"
            df[col_name] = df[self._keyname_T].apply(check_date_format, fmt=fmt)
            result.append(len(df[df[col_name] == True]))
        
        final = pd.DataFrame(columns=['Format', 'GoodRows'])
        final['Format'] = C.FMT
        final['GoodRows'] = result
        return final

    # =========================================================================
    # Analysis Methods
    # =========================================================================
    
    def head(self, n: int = 7) -> pd.DataFrame:
        """Get the first n rows of the dataset."""
        if self.isOpened():
            return self._dataset.head(n)
        return pd.DataFrame()
    
    def colsCount(self) -> int:
        """Get the number of columns."""
        return self._dataset.shape[1] if self.isOpened() else -1
    
    def rowsCount(self) -> int:
        """Get the number of rows."""
        return self._dataset.shape[0] if self.isOpened() else -1
    
    # Snake_case aliases
    def cols_count(self) -> int:
        return self.colsCount()
    
    def rows_count(self) -> int:
        return self.rowsCount()

    def getCountValuesForField(self, col: str, limit: int = 0) -> Optional[pd.DataFrame]:
        """
        Get value frequency distribution for a column.
        
        Args:
            col: Column name to analyze.
            limit: Maximum number of rows to return (0 = all).
        
        Returns:
            DataFrame with values and their frequencies, or None if not opened.
        """
        if not self.isOpened():
            return None
        
        counts = self._dataset[col].value_counts()
        result = pd.DataFrame({
            C.FLD_COL_VALUECOUNT: counts.index,
            C.FLD_FREQ_VALUECOUNT: counts.values
        })
        result = result.sort_values(by=[C.FLD_FREQ_VALUECOUNT], ascending=False)
        
        if limit > 0:
            result = result.head(min(limit, len(result)))
        
        return result
    
    def getSNCountPerPFISize(self) -> pd.DataFrame:
        """Get the distribution of timeline sizes (events per timeline)."""
        df = self.getCountValuesForField(self._keyname_PFI)
        dfagg = df[C.FLD_FREQ_VALUECOUNT].value_counts()
        
        result = pd.DataFrame({
            C.FLD_PFI_NB: dfagg.values,
            C.FLD_SN_NB: dfagg.index
        })
        return result.sort_values(by=[C.FLD_PFI_NB], ascending=False).reset_index(drop=True)

    def countDistinctValues(self, col: str) -> int:
        """Count distinct values in a column."""
        return len(self._dataset[col].value_counts())
    
    def countMissingValues(self, col: str) -> int:
        """Count missing values in a column."""
        return int(self._dataset[col].isnull().sum())
    
    def countUniqueValues(self, col: str) -> int:
        """Count unique values in a column."""
        return self._dataset[col].nunique()

    def missingValues(self) -> List[int]:
        """
        Count and remove rows with missing values in key columns.
        
        Returns:
            List of missing value counts [PFI, SN, T].
        """
        try:
            missing = [
                self.countMissingValues(self._keyname_PFI),
                self.countMissingValues(self._keyname_SN),
                self.countMissingValues(self._keyname_T)
            ]
            
            # Drop rows with missing key values
            for key in [self._keyname_PFI, self._keyname_SN, self._keyname_T]:
                self._dataset.drop(
                    self._dataset[self._dataset[key].isnull()].index,
                    inplace=True
                )
            
            return missing
        except Exception:
            return [0, 0, 0]

    def dump3KeysRejectFile(self) -> int:
        """
        Write rows with missing key values to the reject file.
        
        Returns:
            Number of rejected rows.
        """
        rejects = []
        
        # Collect rows with missing values
        df_pfi = self._dataset[self._dataset[self._keyname_PFI].isnull()].copy()
        if not df_pfi.empty:
            df_pfi.insert(0, C.REJECT_COL_NAME, "Timeline ID is Empty")
            rejects.append(df_pfi)
        
        df_sn = self._dataset[self._dataset[self._keyname_SN].isnull()].copy()
        if not df_sn.empty:
            df_sn.insert(0, C.REJECT_COL_NAME, "Event ID is Empty")
            rejects.append(df_sn)
        
        df_t = self._dataset[self._dataset[self._keyname_T].isnull()].copy()
        if not df_t.empty:
            df_t.insert(0, C.REJECT_COL_NAME, "Timestamp is Empty")
            rejects.append(df_t)
        
        if rejects:
            df_global = pd.concat(rejects)
            df_global.to_csv(self.keysRejectFilename)
            return df_global.shape[0]
        
        # Create empty reject file
        pd.DataFrame().to_csv(self.keysRejectFilename)
        return 0

    def checkDuplicatesCount(self) -> int:
        """Count duplicate rows based on the three key columns."""
        dups = self._dataset.duplicated(
            subset=[self._keyname_PFI, self._keyname_SN, self._keyname_T]
        )
        return int(dups.sum())

    def dumpUniqueEvents(self) -> int:
        """
        Export unique events with frequencies to a CSV file.
        
        Returns:
            Number of unique events.
        """
        df = self.getCountValuesForField(self.SN)
        if df is not None and not df.empty:
            events = SNList(df)
            events.cleanse()
            events.SNList.to_csv(self.uniqueEventsFilename, index=False)
            return events.SNList.shape[0]
        return 0


"""
Temporary file storage for pyDQA4ProcessMining.

Manages temporary files created during chart generation.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import os
from typing import List

from pydqa4pm.utils import constants as C


class ReportStore:
    """
    Manages temporary file storage for report generation.
    
    Creates a temporary folder for chart images and cleans up after
    the report is generated.
    
    Example:
        >>> store = ReportStore()
        >>> store.initialize()
        >>> chart_path = store.getPath("chart.png")
        >>> # ... generate chart to chart_path ...
        >>> store.finalize()  # Cleanup
    """
    
    def __init__(self, temp_path: str = None):
        """
        Initialize the report store.
        
        Args:
            temp_path: Custom temporary folder path (optional).
        """
        self._temp_path = temp_path or C.DEFAULT_STORE_FOLDER
        self._managed_files: List[str] = []

    @property
    def tempPath(self) -> str:
        """Get the temporary folder path."""
        return self._temp_path
    
    @tempPath.setter
    def tempPath(self, value: str):
        """Set the temporary folder path."""
        self._temp_path = value

    def getPath(self, filename: str) -> str:
        """
        Get the full path for a temporary file.
        
        Args:
            filename: The filename to create in temp folder.
        
        Returns:
            Full path to the temporary file.
        """
        full_path = os.path.join(self._temp_path, filename)
        self._managed_files.append(full_path)
        return full_path

    def isStoreFolderExist(self) -> bool:
        """Check if the temporary folder exists."""
        return os.path.isdir(self._temp_path)

    def initialize(self) -> bool:
        """
        Create the temporary folder if it doesn't exist.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            if not self.isStoreFolderExist():
                os.makedirs(self._temp_path, exist_ok=True)
            return True
        except Exception:
            return False

    def finalize(self) -> None:
        """
        Clean up all temporary files and the folder.
        
        Removes all managed files and the temporary folder.
        """
        try:
            # Remove managed files
            for filepath in self._managed_files:
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            # Remove the temp folder if empty
            if self.isStoreFolderExist():
                try:
                    os.rmdir(self._temp_path)
                except OSError:
                    pass  # Folder not empty or other issue
        except Exception:
            pass  # Ignore cleanup errors

    def cleanup(self) -> None:
        """Alias for finalize()."""
        self.finalize()


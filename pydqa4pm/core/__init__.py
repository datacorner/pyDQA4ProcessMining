"""
Core modules for pyDQA4ProcessMining.

This package contains:
- dqa: Main DQA processing orchestrator
- datasource: CSV data source handling and analysis
- report_data: Data container for DQA report results
"""

from pydqa4pm.core.dqa import Dqa4PM
from pydqa4pm.core.datasource import DataSource
from pydqa4pm.core.report_data import DQAReportData

__all__ = ["Dqa4PM", "DataSource", "DQAReportData"]


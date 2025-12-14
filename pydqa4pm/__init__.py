"""
pyDQA4ProcessMining - Data Quality Assessment Tool for Process Mining

A Python-based tool to validate and profile CSV datasets before importing
them into Process Mining solutions.

Author: Benoit CAYLA (benoit@datacorner.fr)
License: GPL
"""

__version__ = "1.0.0"
__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

# Public API
from pydqa4pm.core.dqa import Dqa4PM
from pydqa4pm.core.datasource import DataSource
from pydqa4pm.core.report_data import DQAReportData
from pydqa4pm.utils.logger import Logger
from pydqa4pm.utils import constants

__all__ = [
    "Dqa4PM",
    "DataSource", 
    "DQAReportData",
    "Logger",
    "constants",
    "__version__",
]


"""
Application constants and configuration for pyDQA4ProcessMining.

This module contains all configurable constants used throughout the application,
including logging settings, file naming conventions, date formats, and display limits.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import logging

# =============================================================================
# Logging Configuration
# =============================================================================
ENCODING = "utf-8"
TRACE_LEVEL = logging.DEBUG
TRACE_FORMAT = "%(asctime)s|%(name)s|%(levelname)s|%(message)s"
TRACE_FILENAME = "pydqa4pm.log"

# =============================================================================
# Display Limits
# =============================================================================
LIMIT_BARH_DISPLAY = 30  # Maximum number of bars to display in charts

# =============================================================================
# DataFrame Column Names
# =============================================================================
FLD_COL_VALUECOUNT = "Column"       # Column name for values
FLD_NEW_SN = "New Event"            # Column name for cleansed event names
FLD_FREQ_VALUECOUNT = "Frequency"   # Column name for frequency counts
FLD_PFI_NB = "Nb Of Timeline"       # Column name for timeline count
FLD_SN_NB = "Nb Of events"          # Column name for event count
REJECT_COL_NAME = "REJECT"          # Column name for reject reasons

# =============================================================================
# File and Path Constants
# =============================================================================
NO_FILE_CREATED = "NO FILE CREATED"     # Indicates chart creation failed
NO_CHART_FILE = "default.jpg"           # Default image when chart fails
DEFAULT_STORE_FOLDER = "temp-pydqa4pm/" # Temporary storage folder
DEFAULT_REPORT_FILE = "dqa-report"      # Default report name

# =============================================================================
# Output File Suffixes
# =============================================================================
SUFFIX_3KEYS_REJECT = "-3keys.rejects"  # Reject file for key validation errors
SUFFIX_REPORT = "-report.pdf"           # PDF report suffix
SUFFIX_READ_REJ = "-read.rejects"       # Reject file for read errors
SUFFIX_EVENTS = "-events.csv"           # Events list file suffix

# =============================================================================
# Temporary File Names
# =============================================================================
FILE_FORMAT_TABLE = "temp-fmt-table.jpg"
FILE_SAMPLES_TABLE = "temp-sample-table.jpg"
FILE_PFI_CHART = "temp-pfi-chart.jpg"
FILE_SNMOSTFQ_CHART = "temp-sn-mostfq-chart.jpg"
FILE_COUNTPFIEVTS_CHART = "temp-cnt-pfisn-chart.jpg"

# =============================================================================
# Supported Timestamp Formats
# =============================================================================
# Reference: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
# To add a new format, add it to the FMT list below

FMT_1 = "%d-%m-%Y %H:%M:%S"         # 25-12-2023 14:30:00
FMT_2 = "%d-%m-%Y %H:%M:%S %p"      # 25-12-2023 02:30:00 PM
FMT_3 = "%Y-%m-%d %H:%M:%S"         # 2023-12-25 14:30:00
FMT_4 = "%Y-%m-%d %H:%M:%S %p"      # 2023-12-25 02:30:00 PM
FMT_5 = "%m/%d/%YT%H:%M:%SZ"        # 12/25/2023T14:30:00Z
FMT_6 = "%m/%d/%Y %H:%M:%S"         # 12/25/2023 14:30:00
FMT_7 = "%Y-%m-%d %H:%M:%S.%f"      # 2023-12-25 14:30:00.123456
FMT_8 = "%Y-%m-%dT%H:%M:%S"         # 2023-12-25T14:30:00 (ISO format)
FMT_9 = "%Y-%m-%dT%H:%M:%S.%f"      # 2023-12-25T14:30:00.123456 (ISO with microseconds)
FMT_10 = "%Y-%m-%dT%H:%M:%SZ"       # 2023-12-25T14:30:00Z (ISO UTC)

FMT = [FMT_1, FMT_2, FMT_3, FMT_4, FMT_5, FMT_6, FMT_7, FMT_8, FMT_9, FMT_10]

# =============================================================================
# Text Processing
# =============================================================================
NOISE_CHARACTERS = ",?;.:/!§%*$£=+{}[]()<>&~#'-^@¨¢"


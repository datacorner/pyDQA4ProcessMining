import logging

# Logging
ENCODING = "utf-8"
TRACE_LEVEL = logging.DEBUG
TRACE_FORMAT = "%(asctime)s|%(name)s|%(levelname)s|%(message)s"
TRACE_FILENAME = "bppi-dqa.log"

# List here all the application constants
LIMIT_BARH_DISPLAY = 30             # limit of bar to be displayed
FLD_COL_VALUECOUNT = "Column"       # df freq column name
FLD_NEW_SN = "New Event"            # df freq column name for new event (FLD_COL_VALUECOUNT duplicate here)
FLD_FREQ_VALUECOUNT = "Frequency"   # df column name
FLD_PFI_NB = "Nb Of Timeline"       # df column PFI Number/count
FLD_SN_NB = "Nb Of events"          # df column SN Number/count
REJECT_COL_NAME = "REJECT"          # Name of the column for the Reject reason
NO_FILE_CREATED = "NO FILE CREATED" # Constants specifies the chart could not be created
NO_CHART_FILE = "default.jpg"       # Image to display by default (when impossible to generate a chart for ex)
DEFAULT_STORE_FOLDER = "temp-dqa4bppi/"  # default temp storage folder for the charts and other images
DEFAULT_REPORT_FILE = "bppireport"  # default report name
SUFFIX_3KEYS_REJECT = "-3keys.rejects" # Name of the reject file
SUFFIX_REPORT = "-report.pdf"       # Suffix for the DQA pdf report
SUFFIX_READ_REJ = "-read.rejects"   # Suffix for the read rejects file
SUFFIX_EVENTS = "-events.csv"     # Suffix for the events list (unique)

# Temporary Files names
FILE_FORMAT_TABLE = "temp-fmt-table.jpg"
FILE_SAMPLES_TABLE = "temp-sample-table.jpg"
FILE_PFI_CHART = "temp-pfi-chart.jpg"
FILE_SNMOSTFQ_CHART = "temp-sn-mostfq-chart.jpg"
FILE_COUNTPFIEVTS_CHART = "temp-cnt-pfisn-chart.jpg"

# Formats 
# https://docs.python.org/fr/3.6/library/datetime.html#strftime-and-strptime-behavior
# To add a new format support just add a new constant FMT_x and add it into the FMT python list
FMT_1 = "%d-%m-%Y %H:%M:%S"
FMT_2 = "%d-%m-%Y %H:%M:%S %p"
FMT_3 = "%Y-%m-%d %H:%M:%S"
FMT_4 = "%Y-%m-%d %H:%M:%S %p"
FMT_5 = "%m/%d/%YT%H:%M:%SZ"
FMT_6 = "%m/%d/%Y %H:%M:%S"
FMT_7 = "%Y-%m-%d %H:%M:%S.%f"
FMT = [ FMT_1, FMT_2, FMT_3, FMT_4, FMT_5, FMT_6, FMT_7 ]

# Noise characters
NOISE_CHARACTERS = ",?;.:/!§%*$£=+{}[]()<>&~#'-^@¨¢"
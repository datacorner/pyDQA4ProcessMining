# Configuration Guide

This guide explains how to customize pyDQA4ProcessMining for your specific needs.

## Table of Contents

- [Constants Configuration](#constants-configuration)
- [Date Format Configuration](#date-format-configuration)
- [Logging Configuration](#logging-configuration)
- [Report Customization](#report-customization)
- [Chart Customization](#chart-customization)

---

## Constants Configuration

All configurable constants are located in `pydqa4pm/utils/constants.py`.

### File Naming

```python
# Suffix for reject files containing key validation errors
SUFFIX_3KEYS_REJECT = "-3keys.rejects"

# Suffix for the PDF report
SUFFIX_REPORT = "-report.pdf"

# Suffix for read/parse rejection files
SUFFIX_READ_REJ = "-read.rejects"

# Suffix for the events frequency file
SUFFIX_EVENTS = "-events.csv"
```

**To customize:** Edit these values to change the naming convention of output files.

### Display Limits

```python
# Maximum number of bars to display in horizontal bar charts
LIMIT_BARH_DISPLAY = 30
```

**To show more/fewer values in charts:**
```python
# Show top 50 values instead of 30
LIMIT_BARH_DISPLAY = 50
```

### Noise Characters

```python
# Characters to remove when cleansing event names
NOISE_CHARACTERS = ",?;.:/!§%*$£=+{}[]()<>&~#'-^@¨¢"
```

**To preserve certain characters:**
```python
# Remove @ from noise list to preserve it
NOISE_CHARACTERS = ",?;.:/!§%*$£=+{}[]()<>&~#'-^¨¢"
```

---

## Date Format Configuration

### Supported Date Formats

The tool checks timestamps against these formats (in `constants.py`):

```python
FMT_1 = "%d-%m-%Y %H:%M:%S"         # 25-12-2023 14:30:00
FMT_2 = "%d-%m-%Y %H:%M:%S %p"      # 25-12-2023 02:30:00 PM
FMT_3 = "%Y-%m-%d %H:%M:%S"         # 2023-12-25 14:30:00
FMT_4 = "%Y-%m-%d %H:%M:%S %p"      # 2023-12-25 02:30:00 PM
FMT_5 = "%m/%d/%YT%H:%M:%SZ"        # 12/25/2023T14:30:00Z
FMT_6 = "%m/%d/%Y %H:%M:%S"         # 12/25/2023 14:30:00
FMT_7 = "%Y-%m-%d %H:%M:%S.%f"      # 2023-12-25 14:30:00.123456
FMT_8 = "%Y-%m-%dT%H:%M:%S"         # 2023-12-25T14:30:00 (ISO)
FMT_9 = "%Y-%m-%dT%H:%M:%S.%f"      # 2023-12-25T14:30:00.123456
FMT_10 = "%Y-%m-%dT%H:%M:%SZ"       # 2023-12-25T14:30:00Z (ISO UTC)

FMT = [FMT_1, FMT_2, FMT_3, FMT_4, FMT_5, FMT_6, FMT_7, FMT_8, FMT_9, FMT_10]
```

### Adding Custom Date Formats

Edit `pydqa4pm/utils/constants.py`:

```python
# Add your custom format
FMT_11 = "%Y/%m/%d %H:%M"         # 2023/12/25 14:30
FMT_12 = "%d.%m.%Y %H:%M:%S"      # 25.12.2023 14:30:00

# Include in the format list
FMT = [FMT_1, FMT_2, ..., FMT_10, FMT_11, FMT_12]
```

### Python Date Format Codes

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | 4-digit year | 2023 |
| `%y` | 2-digit year | 23 |
| `%m` | Month (01-12) | 12 |
| `%d` | Day (01-31) | 25 |
| `%H` | Hour 24h (00-23) | 14 |
| `%I` | Hour 12h (01-12) | 02 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%f` | Microsecond | 123456 |
| `%p` | AM/PM | PM |
| `%z` | UTC offset | +0000 |

**Reference:** [Python strftime documentation](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)

---

## Logging Configuration

### Log Settings

Located in `pydqa4pm/utils/constants.py`:

```python
import logging

# Character encoding for log file
ENCODING = "utf-8"

# Logging level
TRACE_LEVEL = logging.DEBUG

# Log message format
TRACE_FORMAT = "%(asctime)s|%(name)s|%(levelname)s|%(message)s"

# Log file name
TRACE_FILENAME = "pydqa4pm.log"
```

### Changing Log Level

```python
import logging

# Show only warnings and errors
TRACE_LEVEL = logging.WARNING

# Show info and above
TRACE_LEVEL = logging.INFO

# Show everything (verbose)
TRACE_LEVEL = logging.DEBUG
```

### Custom Log Format

```python
# Include file and line number
TRACE_FORMAT = "%(asctime)s|%(name)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s"

# Simpler format
TRACE_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
```

### Programmatic Logger Configuration

```python
from pydqa4pm import Logger

# Default logger
log = Logger("my_module")

# Log messages
log.info("Processing started")
log.debug("Detailed debug info")
log.warning("Warning message")
log.error("Error occurred")
```

---

## Report Customization

### PDF Report Settings

Located in `pydqa4pm/reports/pdf_builder.py`:

```python
class PDFReportBuilder(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210   # A4 width in mm
        self.HEIGHT = 297  # A4 height in mm
```

### Header Customization

```python
def header(self):
    # Logo - modify path or remove
    try:
        self.image("assets/pi.png", 10, 8, 50)
    except:
        pass
    
    # Title
    self.set_font('Arial', 'I', 8)
    self.cell(10, 1, 'Process Mining - Data Quality Report', 0, 0, 'L')
    self.ln(20)
```

**To customize the header:**

```python
def header(self):
    # Your custom logo
    self.image('path/to/your_logo.png', 10, 8, 60)
    
    # Custom title
    self.set_font('Arial', 'B', 12)
    self.cell(0, 10, 'Your Custom Report Title', 0, 0, 'C')
    self.ln(20)
```

### Footer Customization

```python
def footer(self):
    self.set_y(-15)
    self.set_font('Arial', 'I', 6)
    self.set_text_color(128)
    self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
```

**To add date to footer:**

```python
from datetime import datetime

def footer(self):
    self.set_y(-15)
    self.set_font('Arial', 'I', 8)
    
    # Left: Page number
    self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'L')
    
    # Right: Generation date
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    self.cell(0, 10, f'Generated: {now}', 0, 0, 'R')
```

---

## Chart Customization

### Chart Dimensions

Located in `pydqa4pm/core/dqa.py`:

```python
# Date format table
Chart(10, 2).CreateTable(...)

# Sample data table
Chart(20, 1).CreateTable(...)

# Bar charts
SeabornChart(10, 6).CreateBarH(...)

# Scatter plots
SeabornChart(10, 6).CreateScatter(...)
```

**Parameters:** `(width_inches, height_inches)`

**To create larger charts:**
```python
SeabornChart(14, 8).CreateBarH(...)
```

### Color Customization

Default color in chart classes:

```python
color = '#087E8B'  # Teal color
```

**To change chart colors:**

```python
# In chart method calls
chart.CreateBarH(filename, data, x, y, color='#FF5733')
```

### Seaborn Theme

Add to chart creation:

```python
import seaborn as sns

# Set style before creating charts
sns.set_style("whitegrid")  # Options: darkgrid, whitegrid, dark, white, ticks
sns.set_palette("husl")     # Options: deep, muted, bright, pastel, dark
```

### Table Styling

In `pydqa4pm/charts/base.py`:

```python
# Table column header colors
colColours=["palegreen"] * len(columns)

# To change:
colColours=["lightblue"] * len(columns)
colColours=["#E8E8E8"] * len(columns)  # Light gray
```

---

## Temporary Files Configuration

### Temp Folder Location

```python
DEFAULT_STORE_FOLDER = "temp-pydqa4pm/"
```

**To change temp folder:**

```python
import tempfile
DEFAULT_STORE_FOLDER = tempfile.gettempdir() + "/pydqa4pm/"
```

### Custom ReportStore

```python
from pydqa4pm.reports import ReportStore

# Custom temp path
store = ReportStore(temp_path="/custom/temp/path/")
store.initialize()
```

---

## Runtime Configuration

### Programmatic Constants Override

For runtime configuration without modifying source files:

```python
from pydqa4pm.utils import constants as C

# Override at runtime
C.LIMIT_BARH_DISPLAY = 50
C.TRACE_LEVEL = logging.INFO

# Add custom date format
C.FMT.append("%Y/%m/%d %H:%M")
```

### Environment-Based Configuration

Create a configuration wrapper:

```python
import os
from pydqa4pm.utils import constants as C

# Environment-based settings
if os.getenv('DQA_ENV') == 'production':
    C.TRACE_LEVEL = logging.WARNING
else:
    C.TRACE_LEVEL = logging.DEBUG
```

---

## Next Steps

- [Usage Examples](examples.md) - See configurations in action
- [API Reference](api-reference.md) - Detailed API documentation
- [Troubleshooting](troubleshooting.md) - Common issues

# API Reference

This document provides detailed information about the main classes and modules in pyDQA4ProcessMining for programmatic usage.

## Table of Contents

- [Package Overview](#package-overview)
- [Core Module](#core-module)
- [Charts Module](#charts-module)
- [Reports Module](#reports-module)
- [Utils Module](#utils-module)

---

## Package Overview

### Importing

```python
# Main exports
from pydqa4pm import Dqa4PM, DataSource, DQAReportData, Logger, constants

# Specific modules
from pydqa4pm.core import Dqa4PM, DataSource, DQAReportData
from pydqa4pm.charts import Chart, SeabornChart, MatplotlibChart
from pydqa4pm.reports import PDFReportBuilder, ReportStore
from pydqa4pm.utils import Logger, constants, SNList
```

### Version

```python
from pydqa4pm import __version__
print(__version__)  # "1.0.0"
```

---

## Core Module

### Dqa4PM Class

Main orchestrator for the DQA workflow.

**Location:** `pydqa4pm.core.dqa`

```python
from pydqa4pm import Dqa4PM, Logger

logger = Logger("my_app")
dqa = Dqa4PM(logger)
```

#### Methods

| Method | Description |
|--------|-------------|
| `process(filename, sep, pfi, sn, t)` | Run complete DQA workflow |
| `open_dataset(filename, sep, pfi, sn, t)` | Open and validate CSV |
| `make_dqa_checks(datasource)` | Perform quality checks |
| `build_charts(report_data, store)` | Generate visualizations |
| `generate_report(report_data, filename)` | Create PDF report |
| `create_alternative_data(datasource)` | Create events file |

#### Example

```python
from pydqa4pm import Dqa4PM, Logger

logger = Logger("analysis")
dqa = Dqa4PM(logger)

# Full workflow
dqa.process("data.csv", ",", "case_id", "activity", "timestamp")

# Or step by step
ds = dqa.open_dataset("data.csv", ",", "case_id", "activity", "timestamp")
if ds.is_opened():
    report_data = dqa.make_dqa_checks(ds)
    # ... continue processing
```

---

### DataSource Class

Manages CSV data loading, validation, and analysis.

**Location:** `pydqa4pm.core.datasource`

```python
from pydqa4pm.core import DataSource

ds = DataSource("data.csv", "case_id", "activity", "timestamp")
ds.open(",")
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `PFI` | str | Timeline ID column name |
| `SN` | str | Event ID column name |
| `T` | str | Timestamp column name |
| `filename` | str | CSV file path |
| `attributes` | List[str] | Non-key column names |
| `rejectRows` | int | Number of rejected rows |
| `readRejectsCount` | int | Rows rejected during reading |

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `open(sep)` | Tuple[bool, Exception] | Load CSV file |
| `is_opened()` | bool | Check if loaded successfully |
| `check3PKeys()` | Tuple[bool, str] | Validate mandatory columns |
| `rows_count()` | int | Total row count |
| `cols_count()` | int | Total column count |
| `checkDuplicatesCount()` | int | Count duplicate rows |
| `countMissingValues(col)` | int | Missing values in column |
| `countDistinctValues(col)` | int | Distinct values in column |
| `getCountValuesForField(col, limit)` | DataFrame | Frequency distribution |
| `checkBPPIDateFormats()` | DataFrame | Date format validation |
| `missingValues()` | List[int] | Missing counts [PFI,SN,T] |
| `dumpUniqueEvents()` | int | Export events to CSV |

#### Example

```python
from pydqa4pm.core import DataSource

ds = DataSource("data.csv", "case_id", "activity", "timestamp")
success, error = ds.open(",")

if ds.is_opened():
    print(f"Rows: {ds.rows_count()}")
    print(f"Columns: {ds.cols_count()}")
    print(f"Duplicates: {ds.checkDuplicatesCount()}")
    
    # Validate keys
    valid, message = ds.check3PKeys()
    if not valid:
        print(f"Error: {message}")
    
    # Get event frequencies
    events = ds.getCountValuesForField("activity", limit=10)
    print(events)
```

---

### DQAReportData Class

Container for all DQA results and metrics.

**Location:** `pydqa4pm.core.report_data`

```python
from pydqa4pm.core import DQAReportData

data = DQAReportData("data.csv", "case_id", "activity", "timestamp")
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `filename` | str | Source file name |
| `PFIKey`, `SNKey`, `TKey` | str | Column names |
| `RowCount`, `ColCount` | int | Dataset dimensions |
| `AllChecksOK` | bool | Overall check status |
| `attributes` | List[str] | Non-key attributes |
| `missings` | List[int] | Missing values [PFI,SN,T] |
| `uniques` | List[int] | Unique values [PFI,SN,T] |
| `duplicates` | str | Duplicate count with % |
| `rejects` | str | Reject count with % |
| `distinctPFI`, `distinctSN` | str | Distinct counts with % |

---

## Charts Module

### Chart Class (Base)

Base class for chart generation.

**Location:** `pydqa4pm.charts.base`

```python
from pydqa4pm.charts import Chart

chart = Chart(width_inch=10, height_inch=4)
chart.CreateTable("output.jpg", dataframe)
```

#### Methods

| Method | Description |
|--------|-------------|
| `CreateTable(filename, data, max_cols)` | Create table image |
| `CreateLine(filename, data, x, y, ...)` | Line chart (override) |
| `CreateBarH(filename, data, x, y, ...)` | Horizontal bar (override) |
| `CreateBarV(filename, data, x, y, ...)` | Vertical bar (override) |

---

### SeabornChart Class

Seaborn-based chart generator.

**Location:** `pydqa4pm.charts.seaborn_chart`

```python
from pydqa4pm.charts import SeabornChart

chart = SeabornChart(10, 6)
chart.CreateBarH("output.png", df, "Category", "Value", label_y="Count")
```

#### Methods

| Method | Description |
|--------|-------------|
| `CreateBarH(filename, data, x, y, ...)` | Horizontal bar chart |
| `CreateBarV(filename, data, x, y, ...)` | Vertical bar chart |
| `CreateLine(filename, data, x, y, ...)` | Line chart |
| `CreateScatter(filename, data, x, y, ...)` | Scatter plot |

---

### MatplotlibChart Class

Pure Matplotlib chart generator.

**Location:** `pydqa4pm.charts.matplotlib_chart`

```python
from pydqa4pm.charts import MatplotlibChart

chart = MatplotlibChart(10, 6)
chart.CreateLine("output.png", df, "X", "Y")
```

---

## Reports Module

### PDFReportBuilder Class

Generates PDF reports from DQA results.

**Location:** `pydqa4pm.reports.pdf_builder`

```python
from pydqa4pm.reports import PDFReportBuilder

builder = PDFReportBuilder()
builder.create(dqa_report_data)
builder.output("report.pdf", "F")
```

#### Methods

| Method | Description |
|--------|-------------|
| `create(dqa)` | Build complete report |
| `output(filename, "F")` | Save to file |
| `insert_title(text)` | Add section title |
| `insert_image(title, path)` | Add image |
| `insert_text_and_value(label, value)` | Add label-value pair |

---

### ReportStore Class

Manages temporary file storage.

**Location:** `pydqa4pm.reports.store`

```python
from pydqa4pm.reports import ReportStore

store = ReportStore()
store.initialize()
chart_path = store.getPath("chart.png")
# ... generate chart ...
store.finalize()  # Cleanup
```

#### Methods

| Method | Description |
|--------|-------------|
| `initialize()` | Create temp folder |
| `getPath(filename)` | Get full path for temp file |
| `finalize()` | Remove all temp files |

---

## Utils Module

### Logger Class

Logging utility with console and file output.

**Location:** `pydqa4pm.utils.logger`

```python
from pydqa4pm import Logger

log = Logger("my_module")
log.info("Processing started")
log.debug("Debug information")
log.warning("Warning message")
log.error("Error occurred")
```

#### Methods

| Method | Description |
|--------|-------------|
| `info(*messages)` | Log info message |
| `debug(*messages)` | Log debug message |
| `warning(*messages)` | Log warning message |
| `error(*messages)` | Log error message |

**Log File:** `pydqa4pm.log`

---

### SNList Class

Event list management with cleansing.

**Location:** `pydqa4pm.utils.events`

```python
from pydqa4pm.utils import SNList

events_df = datasource.getCountValuesForField("activity")
sn_list = SNList(events_df)
sn_list.cleanse()
sn_list.SNList.to_csv("events.csv")
```

#### Methods

| Method | Description |
|--------|-------------|
| `cleanse()` | Remove noise from event names |
| `remove_noise(text)` | Clean individual text |

---

### Constants Module

Configuration constants.

**Location:** `pydqa4pm.utils.constants`

```python
from pydqa4pm.utils import constants as C

print(C.LIMIT_BARH_DISPLAY)  # 30
print(C.FMT)  # List of date formats
```

#### Key Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `LIMIT_BARH_DISPLAY` | 30 | Max bars in charts |
| `FMT` | List | Supported date formats |
| `SUFFIX_REPORT` | "-report.pdf" | Report file suffix |
| `SUFFIX_EVENTS` | "-events.csv" | Events file suffix |

---

## Complete Example

```python
#!/usr/bin/env python3
"""Complete programmatic usage example."""

from pydqa4pm import Dqa4PM, Logger
from pydqa4pm.core import DataSource
from pydqa4pm.reports import ReportStore
from pydqa4pm.utils import constants as C

def analyze_file(filepath: str, pfi: str, sn: str, t: str):
    """Run complete DQA analysis on a file."""
    
    # Initialize
    logger = Logger("analysis")
    dqa = Dqa4PM(logger)
    
    # Open dataset
    ds = dqa.open_dataset(filepath, ",", pfi, sn, t)
    
    if not ds.is_opened():
        logger.error("Failed to open file")
        return None
    
    # Initialize storage
    store = ReportStore()
    store.initialize()
    
    # Run checks
    report_data = dqa.make_dqa_checks(ds)
    dqa.create_alternative_data(ds)
    
    if report_data.AllChecksOK:
        # Generate report
        dqa.build_charts(report_data, store)
        report_name = ds.filenameWithoutExt + C.SUFFIX_REPORT
        dqa.generate_report(report_data, report_name)
    
    # Cleanup
    store.finalize()
    
    # Return summary
    return {
        "filename": filepath,
        "rows": report_data.RowCount,
        "columns": report_data.ColCount,
        "duplicates": report_data.duplicates,
        "success": report_data.AllChecksOK
    }

if __name__ == "__main__":
    result = analyze_file(
        "samples/data.csv",
        pfi="id",
        sn="concept:name",
        t="time:timestamp"
    )
    print(result)
```

---

## Next Steps

- [Configuration Guide](configuration.md) - Customize settings
- [Usage Examples](examples.md) - More practical examples
- [Troubleshooting](troubleshooting.md) - Common issues

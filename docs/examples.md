# Usage Examples

This guide provides practical examples for using pyDQA4ProcessMining with various datasets and scenarios.

## Table of Contents

- [Command Line Usage](#command-line-usage)
- [Python API Usage](#python-api-usage)
- [Common Scenarios](#common-scenarios)
- [Working with Different CSV Formats](#working-with-different-csv-formats)
- [Interpreting Results](#interpreting-results)
- [Batch Processing](#batch-processing)

---

## Command Line Usage

### Basic Command

```bash
python pmdqa.py -filename <path/to/file.csv> -pfi <timeline_column> -sn <event_column> -t <timestamp_column>
```

### Example with Sample Data

```bash
python pmdqa.py -filename samples/InternationalDeclarations.csv -pfi id -sn "concept:name" -t "time:timestamp"
```

**Output:**
```
Info> ============================================================
Info> pyDQA4ProcessMining v1.0.0
Info> ============================================================
Info> Starting Analysis
Info> Opening dataset ...
Info> Lines rejected (structure issues): <0> | File: <samples/InternationalDeclarations-read.rejects>
Info> Data Quality Check for file: <samples/InternationalDeclarations.csv>
Info> Mandatory fields identified: PFI->id, SN->concept:name, T->time:timestamp
Info> Lines rejected (key validation): <0> | File: <samples/InternationalDeclarations-3keys.rejects>
Info> Performing data quality checks
Info> Performing data quality checks ...
Info> Dataset checks completed successfully
Info> Creating supplementary files
Info> Events file created: <samples/InternationalDeclarations-events.csv> with <16> unique events
Info> Building charts
Info> Generating charts and tables ...
Info> Charts generated successfully
Info> Generating report: samples/InternationalDeclarations-report.pdf
Info> Report created: samples/InternationalDeclarations-report.pdf
Info> Cleaning up temporary files
Info> Analysis Complete
```

---

## Python API Usage

### Basic Usage

```python
from pydqa4pm import Dqa4PM, Logger

# Initialize logger and DQA processor
logger = Logger("my_analysis")
dqa = Dqa4PM(logger)

# Run complete analysis
dqa.process(
    dataset_filename="data.csv",
    separator=",",
    pfi_key="case_id",
    sn_key="activity",
    t_key="timestamp"
)
```

### Step-by-Step Analysis

```python
from pydqa4pm import Dqa4PM, Logger
from pydqa4pm.reports import ReportStore
from pydqa4pm.utils import constants as C

logger = Logger("detailed_analysis")
dqa = Dqa4PM(logger)

# Step 1: Open and validate dataset
ds = dqa.open_dataset(
    filename="data.csv",
    sep=",",
    pfi="case_id",
    sn="activity",
    t="timestamp"
)

if ds.is_opened():
    # Step 2: Initialize storage
    store = ReportStore()
    store.initialize()
    
    # Step 3: Perform DQA checks
    report_data = dqa.make_dqa_checks(ds)
    
    # Step 4: Create events file
    dqa.create_alternative_data(ds)
    
    if report_data.AllChecksOK:
        # Step 5: Build charts
        dqa.build_charts(report_data, store)
        
        # Step 6: Generate PDF report
        report_name = ds.filenameWithoutExt + C.SUFFIX_REPORT
        dqa.generate_report(report_data, report_name)
    
    # Cleanup
    store.finalize()
```

### Direct DataSource Access

```python
from pydqa4pm.core import DataSource

# Open a dataset directly
ds = DataSource("data.csv", "case_id", "activity", "timestamp")
ds.open(",")

if ds.is_opened():
    # Access statistics
    print(f"Rows: {ds.rows_count()}")
    print(f"Columns: {ds.cols_count()}")
    print(f"Duplicates: {ds.checkDuplicatesCount()}")
    print(f"Missing Timeline IDs: {ds.countMissingValues('case_id')}")
    
    # Get event frequency
    events = ds.getCountValuesForField("activity", limit=10)
    print(events)
    
    # Check date formats
    date_check = ds.checkBPPIDateFormats()
    print(date_check)
```

---

## Common Scenarios

### Scenario 1: Simple CSV with Standard Columns

**Dataset: `sales_process.csv`**
```csv
case_id,activity,timestamp,customer_type,amount
C001,Order Received,2023-01-15 09:30:00,Premium,1500.00
C001,Payment Processed,2023-01-15 10:00:00,Premium,1500.00
C002,Order Received,2023-01-15 11:00:00,Standard,250.00
```

**Command:**
```bash
python pmdqa.py -filename sales_process.csv -pfi case_id -sn activity -t timestamp
```

**Python:**
```python
from pydqa4pm import Dqa4PM, Logger

logger = Logger("sales")
dqa = Dqa4PM(logger)
dqa.process("sales_process.csv", ",", "case_id", "activity", "timestamp")
```

### Scenario 2: Semicolon-Separated CSV (European Format)

**Dataset: `process_data.csv`**
```csv
process_id;step_name;date_time;operator
P100;Start;2023-06-01 08:00:00;John
P100;Review;2023-06-01 09:30:00;Mary
```

**Command:**
```bash
python pmdqa.py -filename process_data.csv -pfi process_id -sn step_name -t date_time -separator ";"
```

### Scenario 3: Column Names with Special Characters

**Dataset: `event_log.csv`**
```csv
"case:concept:name","time:timestamp","concept:name","org:resource"
"Case_001","2023-03-20 10:00:00","Submit Application","User_A"
```

**Command:**
```bash
python pmdqa.py -filename event_log.csv -pfi "case:concept:name" -sn "concept:name" -t "time:timestamp"
```

### Scenario 4: ISO Format Timestamps

The tool now supports ISO 8601 timestamps:

```csv
case_id,activity,timestamp
C001,Start,2023-12-25T14:30:00
C001,End,2023-12-25T15:00:00.123456
```

```bash
python pmdqa.py -filename data.csv -pfi case_id -sn activity -t timestamp
```

---

## Working with Different CSV Formats

### Standard Comma-Separated

```bash
python pmdqa.py -filename data.csv -pfi id -sn event -t timestamp
```

### Semicolon-Separated

```bash
python pmdqa.py -filename data.csv -pfi id -sn event -t timestamp -separator ";"
```

### Pipe-Separated

```bash
python pmdqa.py -filename data.csv -pfi id -sn event -t timestamp -separator "|"
```

### Tab-Separated

```bash
python pmdqa.py -filename data.tsv -pfi id -sn event -t timestamp -separator $'\t'
```

---

## Interpreting Results

### Generated Files

| File | Description |
|------|-------------|
| `*-report.pdf` | Main DQA report with visualizations |
| `*-3keys.rejects` | Rows with issues in mandatory columns |
| `*-read.rejects` | Rows that couldn't be parsed correctly |
| `*-events.csv` | List of unique events with frequencies |

### Understanding the PDF Report

The PDF report contains:

1. **Dataset Information** - File details, column mappings, statistics
2. **Sample Data** - First 5 rows preview
3. **Timeline ID Analysis** - Unique timelines, frequency chart
4. **Event ID Analysis** - Unique events, frequency distribution, timeline sizes
5. **Timestamp Analysis** - Date format validation results

### Events CSV Format

The events CSV contains:
- **Column**: Original event name
- **New Event**: Cleansed event name (noise removed)
- **Frequency**: Number of occurrences

---

## Batch Processing

### Shell Script (Linux/macOS)

```bash
#!/bin/bash
for file in data/*.csv; do
    echo "Processing: $file"
    python pmdqa.py -filename "$file" -pfi case_id -sn activity -t timestamp
done
echo "Complete!"
```

### Python Batch Script

```python
#!/usr/bin/env python3
"""Batch process multiple CSV files."""

from pathlib import Path
from pydqa4pm import Dqa4PM, Logger

# Configuration
INPUT_DIR = Path("./data")
PFI = "case_id"
SN = "activity"
T = "timestamp"

def main():
    logger = Logger("batch")
    dqa = Dqa4PM(logger)
    
    csv_files = list(INPUT_DIR.glob("*.csv"))
    print(f"Found {len(csv_files)} files")
    
    for i, filepath in enumerate(csv_files, 1):
        print(f"[{i}/{len(csv_files)}] Processing: {filepath.name}")
        try:
            dqa.process(str(filepath), ",", PFI, SN, T)
            print(f"  ✓ Complete")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("Batch processing finished!")

if __name__ == "__main__":
    main()
```

---

## Tips and Best Practices

### 1. Check Column Names First

```python
import pandas as pd
df = pd.read_csv("your_file.csv", nrows=1)
print(df.columns.tolist())
```

### 2. Handle Large Files

For very large files, the tool processes them efficiently but consider:
- Running on a machine with adequate RAM
- Using SSD storage for better I/O

### 3. Review Reject Files

Always check reject files to understand data quality issues:
- `*-read.rejects`: Structural CSV problems
- `*-3keys.rejects`: Missing mandatory values

### 4. Use the Events File

The `*-events.csv` file helps identify:
- Inconsistent event naming
- Rare/unusual events
- Potential data entry errors

---

## Next Steps

- [API Reference](api-reference.md) - Detailed class documentation
- [Configuration Guide](configuration.md) - Customize settings
- [Troubleshooting](troubleshooting.md) - Common issues

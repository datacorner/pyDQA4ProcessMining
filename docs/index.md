# pyDQA4ProcessMining Documentation

Welcome to the documentation for **pyDQA4ProcessMining** - a data quality assessment tool for Process Mining data.

## Quick Links

| Document | Description |
|----------|-------------|
| [Installation Guide](installation.md) | System requirements, installation steps, and setup verification |
| [Usage Examples](examples.md) | Practical examples for CLI and Python API usage |
| [API Reference](api-reference.md) | Detailed documentation for programmatic usage |
| [Configuration](configuration.md) | How to customize date formats, logging, and reports |
| [Troubleshooting](troubleshooting.md) | Solutions for common issues |

## What is pyDQA4ProcessMining?

pyDQA4ProcessMining is a Python-based tool designed to validate and profile CSV datasets before importing them into Process Mining solutions. It performs comprehensive data quality checks and generates detailed PDF reports with visualizations.

## Key Features

- **CSV Validation** - Verify file structure and parsing
- **Key Field Detection** - Validate Timeline ID, Event ID, and Timestamp columns
- **Null Value Detection** - Identify missing values in mandatory fields
- **Duplicate Analysis** - Find duplicates based on key combinations
- **Date Format Validation** - Check timestamps against 10+ supported formats
- **PDF Reports** - Generate comprehensive visual reports with charts
- **Events Export** - Export unique events with frequency distribution

## Getting Started

### 1. Install the Package

```bash
git clone https://github.com/datacorner/pyDQA4ProcessMining.git
cd pyDQA4ProcessMining
pip install .
```

### 2. Run Your First Analysis

**Command Line:**
```bash
python pmdqa.py -filename samples/data.csv -pfi id -sn "concept:name" -t "time:timestamp"
```

**Python API:**
```python
from pydqa4pm import Dqa4PM, Logger

logger = Logger("my_analysis")
dqa = Dqa4PM(logger)
dqa.process("data.csv", ",", "case_id", "activity", "timestamp")
```

### 3. Review the Report

Open the generated PDF report in the same directory as your input file.

## Process Mining Keys

The tool validates three mandatory columns required for process mining:

| Key | Full Name | Description |
|-----|-----------|-------------|
| **PFI** | Process Flow Identifier | Unique identifier for each process instance (case/timeline) |
| **SN** | Step Name | Name of the activity/event in the process |
| **T** | Timestamp | Date and time when the event occurred |

## Output Files

| Extension | Description |
|-----------|-------------|
| `-report.pdf` | Main DQA report with charts and metrics |
| `-3keys.rejects` | Rows with missing mandatory values |
| `-read.rejects` | Rows with parsing errors |
| `-events.csv` | Unique events with frequency distribution |

## Package Structure

```
pydqa4pm/
├── __init__.py           # Package exports
├── core/                 # Core functionality
│   ├── dqa.py            # Main DQA orchestrator
│   ├── datasource.py     # CSV data handling
│   └── report_data.py    # Report data container
├── charts/               # Chart generation
│   ├── base.py           # Base chart class
│   ├── seaborn_chart.py  # Seaborn implementations
│   └── matplotlib_chart.py
├── reports/              # Report generation
│   ├── pdf_builder.py    # PDF report builder
│   └── store.py          # Temp file management
└── utils/                # Utilities
    ├── constants.py      # Configuration
    ├── logger.py         # Logging
    └── events.py         # Event list handling
```

## Supported Date Formats

The tool supports 10 common timestamp formats:

- `%Y-%m-%d %H:%M:%S` → 2023-12-25 14:30:00
- `%Y-%m-%dT%H:%M:%S` → 2023-12-25T14:30:00 (ISO)
- `%Y-%m-%dT%H:%M:%SZ` → 2023-12-25T14:30:00Z (ISO UTC)
- `%Y-%m-%d %H:%M:%S.%f` → 2023-12-25 14:30:00.123456
- `%d-%m-%Y %H:%M:%S` → 25-12-2023 14:30:00
- And more...

See [Configuration Guide](configuration.md) to add custom formats.

## Version

Current version: **1.0.0**

```python
from pydqa4pm import __version__
print(__version__)  # "1.0.0"
```

## Support

- **GitHub Issues:** [Report a bug](https://github.com/datacorner/pyDQA4ProcessMining/issues)
- **Email:** benoit@datacorner.fr

## License

This project is licensed under the GPL License.

## Author

**Benoit CAYLA** - benoit@datacorner.fr

---

[← Back to README](../README.md)

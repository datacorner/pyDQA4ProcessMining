# pyDQA4ProcessMining

<p align="center">
  <img src="assets/pi.png" alt="pyDQA4ProcessMining Logo" width="200"/>
</p>

<p align="center">
  <strong>Data Quality Assessment Tool for Process Mining</strong>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL-green.svg" alt="License: GPL"></a>
  <a href="#installation"><img src="https://img.shields.io/badge/pip-installable-orange.svg" alt="pip installable"></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#license">License</a>
</p>

---

## Overview

**pyDQA4ProcessMining** is a Python-based data quality assessment tool designed to validate and profile CSV datasets before importing them into Process Mining solutions. By profiling your data beforehand, you can avoid technical issues and misunderstandings that commonly arise during the import process.

The tool generates a comprehensive PDF report containing all control results, charts, and quality metrics for your process mining data.

## Features

- ✅ **CSV Validation** - Verify that CSV files can be opened and parsed correctly
- ✅ **Key Field Detection** - Validate the presence of the 3 mandatory process mining keys:
  - **PFI** (Process Flow Identifier / Timeline ID)
  - **SN** (Step Name / Event ID)
  - **T** (Timestamp)
- ✅ **Null Value Detection** - Identify and report missing values in mandatory fields
- ✅ **Duplicate Analysis** - Count duplicates based on the 3 key fields
- ✅ **Date Format Validation** - Check timestamp formats against multiple accepted patterns
- ✅ **Statistical Profiling** - Row/column counts, unique values, frequency distributions
- ✅ **PDF Report Generation** - Comprehensive visual report with charts and tables
- ✅ **Reject File Generation** - Export problematic rows for review

## Installation

### Prerequisites

- Python 3.10 or higher

### Method 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/datacorner/pyDQA4ProcessMining.git
cd pyDQA4ProcessMining

# Install the package
pip install .

# Or install in development mode
pip install -e .
```

### Method 2: Install Dependencies Only

```bash
pip install -r requirements.txt
```

### Required Packages

| Package | Version | Description |
|---------|---------|-------------|
| pandas | ≥1.5.0 | Data manipulation and analysis |
| numpy | ≥1.23.0 | Numerical computing |
| matplotlib | ≥3.6.0 | Chart generation |
| seaborn | ≥0.12.0 | Statistical data visualization |
| fpdf | ≥1.7.2 | PDF report generation |

## Quick Start

### Command Line Usage

```bash
python pmdqa.py -filename <csv_file> -pfi <timeline_id_column> -sn <event_id_column> -t <timestamp_column>
```

### Example

```bash
python pmdqa.py -filename samples/InternationalDeclarations.csv -pfi id -sn "concept:name" -t "time:timestamp"
```

### Python API Usage

```python
from pydqa4pm import Dqa4PM, Logger

# Initialize
logger = Logger("my_analysis")
dqa = Dqa4PM(logger)

# Run analysis
dqa.process(
    dataset_filename="data.csv",
    separator=",",
    pfi_key="case_id",
    sn_key="activity",
    t_key="timestamp"
)
```

### Command Line Arguments

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `-filename` | Yes | Path to the CSV file to analyze | - |
| `-pfi` | Yes | Column name for Timeline ID (Process Flow Identifier) | - |
| `-sn` | Yes | Column name for Event ID (Step Name) | - |
| `-t` | Yes | Column name for Timestamp | - |
| `-separator` | No | CSV field separator | `,` (comma) |
| `--version` | No | Show version and exit | - |

## Output Files

The tool generates several output files in the same directory as the input file:

| File | Description |
|------|-------------|
| `[filename]-report.pdf` | Comprehensive DQA report with charts and metrics |
| `[filename]-3keys.rejects` | Rows with issues in one of the 3 mandatory keys |
| `[filename]-read.rejects` | Rows rejected during file reading (structural issues) |
| `[filename]-events.csv` | Unique events list with frequency distribution |

## Data Quality Checks

### 1. File Structure Validation
- Verifies CSV can be parsed correctly
- Identifies and logs structural issues (malformed rows)

### 2. Key Field Validation
- Confirms all 3 mandatory columns exist
- Reports missing values in each key field
- Generates reject files for problematic rows

### 3. Duplicate Detection
- Counts duplicate rows based on the combination of PFI + SN + T
- Reports duplicate ratio as percentage of total rows

### 4. Timestamp Format Validation
Checks timestamps against these accepted formats:

| Format | Example |
|--------|---------|
| `%d-%m-%Y %H:%M:%S` | 25-12-2023 14:30:00 |
| `%Y-%m-%d %H:%M:%S` | 2023-12-25 14:30:00 |
| `%Y-%m-%dT%H:%M:%S` | 2023-12-25T14:30:00 |
| `%Y-%m-%d %H:%M:%S.%f` | 2023-12-25 14:30:00.123456 |
| `%m/%d/%Y %H:%M:%S` | 12/25/2023 14:30:00 |

### 5. Statistical Analysis
- Total row and column counts
- Distinct value counts for each key field
- Frequency distribution of events
- Timeline size distribution

## Sample Reports

Pre-generated sample reports are available in the `samples/` directory:

- [International Declarations Report](samples/InternationalDeclarations-report.pdf)
- [Simple Data Report](samples/data-report.pdf)

## Documentation

For detailed documentation, examples, and advanced usage, see the [docs/](docs/) folder:

- [Installation Guide](docs/installation.md) - System requirements and setup
- [Usage Examples](docs/examples.md) - Practical examples and scenarios
- [API Reference](docs/api-reference.md) - Programmatic usage documentation
- [Configuration](docs/configuration.md) - Customization options
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

## Project Structure

```
pyDQA4ProcessMining/
├── pydqa4pm/                  # Main package
│   ├── __init__.py            # Package initialization
│   ├── core/                  # Core functionality
│   │   ├── dqa.py             # Main DQA orchestrator
│   │   ├── datasource.py      # CSV data handling
│   │   └── report_data.py     # Report data container
│   ├── charts/                # Chart generation
│   │   ├── base.py            # Base chart class
│   │   ├── seaborn_chart.py   # Seaborn implementations
│   │   └── matplotlib_chart.py # Matplotlib implementations
│   ├── reports/               # Report generation
│   │   ├── pdf_builder.py     # PDF report builder
│   │   └── store.py           # Temporary file management
│   └── utils/                 # Utilities
│       ├── constants.py       # Configuration constants
│       ├── logger.py          # Logging utilities
│       └── events.py          # Event list management
├── assets/                    # Static assets (logo)
├── docs/                      # Documentation
├── samples/                   # Sample datasets and reports
├── pmdqa.py                   # CLI entry point
├── setup.py                   # Package installation
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/datacorner/pyDQA4ProcessMining.git
cd pyDQA4ProcessMining
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black pydqa4pm/
flake8 pydqa4pm/
```

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) file for details.

## Author

**Benoit CAYLA**

- Email: benoit@datacorner.fr
- GitHub: [datacorner](https://github.com/datacorner)

## Changelog

### v1.0.0
- Complete code reorganization into proper Python package structure
- Added pip installation support via setup.py
- Improved documentation and examples
- Added type hints and docstrings
- Enhanced error handling and logging
- Added 3 additional ISO timestamp formats
- Backward compatibility with legacy API

## Acknowledgments

- Built for Process Mining data preparation
- Inspired by data quality best practices in process mining workflows

# Installation Guide

This guide covers the complete installation process for pyDQA4ProcessMining.

## System Requirements

### Operating System
- **Windows** 10/11
- **macOS** 10.15 (Catalina) or later
- **Linux** Ubuntu 18.04+, CentOS 7+, or equivalent

### Python Version
- Python **3.10** or higher is required
- Download from: [python.org](https://www.python.org/downloads/)

### Verify Python Installation

```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.10.x` or higher

## Installation Methods

### Method 1: Install as Package (Recommended)

```bash
# Clone the repository
git clone https://github.com/datacorner/pyDQA4ProcessMining.git

# Navigate to the project directory
cd pyDQA4ProcessMining

# Install the package
pip install .
```

### Method 2: Development Installation

For development work where you want changes to take effect immediately:

```bash
git clone https://github.com/datacorner/pyDQA4ProcessMining.git
cd pyDQA4ProcessMining
pip install -e .
```

### Method 3: Dependencies Only

If you just want to run the scripts without installing:

```bash
git clone https://github.com/datacorner/pyDQA4ProcessMining.git
cd pyDQA4ProcessMining
pip install -r requirements.txt
```

## Virtual Environment (Recommended)

Using a virtual environment is recommended to avoid conflicts with other Python projects.

### Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Install in Virtual Environment

```bash
pip install .
```

### Deactivate Virtual Environment

```bash
deactivate
```

## Dependencies

The following packages will be installed automatically:

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | ≥1.5.0 | Data manipulation and CSV handling |
| numpy | ≥1.23.0 | Numerical operations |
| matplotlib | ≥3.6.0 | Chart generation (base) |
| seaborn | ≥0.12.0 | Statistical visualizations |
| fpdf | ≥1.7.2 | PDF report generation |

### Development Dependencies

For development work:

```bash
pip install -e ".[dev]"
```

This includes:
- pytest - Testing framework
- pytest-cov - Coverage reporting
- flake8 - Code linting
- black - Code formatting
- mypy - Type checking

## Verify Installation

### After Package Installation

```bash
python -c "from pydqa4pm import __version__; print(f'pydqa4pm v{__version__}')"
```

### Check CLI

```bash
python pmdqa.py --version
python pmdqa.py --help
```

Expected output:
```
usage: pmdqa [-h] -filename FILENAME -pfi PFI -sn SN -t T [-separator SEPARATOR] [--version]

Data Quality Assessment Tool for Process Mining

options:
  -h, --help            show this help message and exit
  -filename FILENAME    Path to the CSV file to analyze
  -pfi PFI              Column name for Timeline ID (Process Flow Identifier)
  -sn SN                Column name for Event ID (Step Name)
  -t T                  Column name for Timestamp
  -separator SEPARATOR  CSV field separator (default: comma)
  --version             show program's version number and exit
```

## Test with Sample Data

Verify everything works by running an analysis on the included sample data:

```bash
python pmdqa.py -filename samples/data.csv -pfi id -sn "concept:name" -t "time:timestamp"
```

This should generate:
- `samples/data-report.pdf`
- `samples/data-3keys.rejects`
- `samples/data-read.rejects`
- `samples/data-events.csv`

## Troubleshooting Installation

### Common Issues

**Issue: `pip` command not found**
```bash
# Try using pip3
pip3 install .
```

**Issue: Permission denied**
```bash
# Install for current user only
pip install --user .
```

**Issue: SSL Certificate errors**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org .
```

**Issue: Package version conflicts**
```bash
# Upgrade pip first
pip install --upgrade pip
pip install .
```

**Issue: Import errors after installation**
```bash
# Reinstall in development mode
pip uninstall pydqa4pm
pip install -e .
```

### Getting Help

If you encounter issues:
1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Open an issue on [GitHub](https://github.com/datacorner/pyDQA4ProcessMining/issues)
3. Contact: benoit@datacorner.fr

## Upgrading

To upgrade to the latest version:

```bash
cd pyDQA4ProcessMining
git pull
pip install --upgrade .
```

## Uninstalling

```bash
pip uninstall pydqa4pm
```

## Next Steps

After successful installation:
1. Read the [Usage Examples](examples.md) for practical examples
2. Review the [Configuration Guide](configuration.md) for customization options
3. Check the [API Reference](api-reference.md) for programmatic usage

# Troubleshooting Guide

This guide helps you resolve common issues when using pyDQA4ProcessMining.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Import Errors](#import-errors)
- [Runtime Errors](#runtime-errors)
- [Data Quality Issues](#data-quality-issues)
- [Report Generation Issues](#report-generation-issues)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### Python Version Error

**Error:**
```
SyntaxError: invalid syntax
```

**Cause:** Python version is too old.

**Solution:**
```bash
# Check your Python version
python --version

# Upgrade to Python 3.10+
# Download from https://www.python.org/downloads/
```

---

### pip Not Found

**Error:**
```
'pip' is not recognized as an internal or external command
```

**Solution (Windows):**
```bash
py -m pip install .
```

**Solution (Linux/macOS):**
```bash
pip3 install .
# or
python3 -m pip install .
```

---

### Package Installation Fails

**Error:**
```
ERROR: Could not install packages due to an OSError
```

**Solution 1:** Install for current user only
```bash
pip install --user .
```

**Solution 2:** Upgrade pip first
```bash
pip install --upgrade pip
pip install .
```

**Solution 3:** Use virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install .
```

---

## Import Errors

### ModuleNotFoundError: pydqa4pm

**Error:**
```
ModuleNotFoundError: No module named 'pydqa4pm'
```

**Cause:** Package not installed or wrong Python environment.

**Solution 1:** Install the package
```bash
cd pyDQA4ProcessMining
pip install .
```

**Solution 2:** Verify installation
```bash
pip list | grep pydqa
```

**Solution 3:** Check Python path
```python
import sys
print(sys.path)
```

---

### ImportError After Package Update

**Error:**
```
ImportError: cannot import name 'X' from 'pydqa4pm'
```

**Cause:** Old cached files or incomplete update.

**Solution:**
```bash
pip uninstall pydqa4pm
pip cache purge
pip install .
```

---

## Runtime Errors

### File Not Found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```

**Solution:**
1. Check the file path is correct
2. Use absolute path:
```bash
python pmdqa.py -filename /full/path/to/data.csv -pfi id -sn event -t timestamp
```

---

### Column Not Found

**Error:**
```
Error> Timeline ID column has not been found.
```

**Cause:** Column name doesn't match exactly (case-sensitive).

**Solution:**
1. Check exact column names:
```python
import pandas as pd
df = pd.read_csv("your_file.csv", nrows=1)
print(df.columns.tolist())
```

2. Use exact column names:
```bash
python pmdqa.py -filename data.csv -pfi "Case ID" -sn "Activity Name" -t "Timestamp"
```

---

### Encoding Error

**Error:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Cause:** File uses different encoding (e.g., Latin-1).

**Solution:**
Convert file to UTF-8:
```python
import pandas as pd

# Read with detected encoding
df = pd.read_csv("data.csv", encoding="latin-1")

# Save as UTF-8
df.to_csv("data_utf8.csv", encoding="utf-8", index=False)
```

Then analyze the converted file.

---

### Memory Error

**Error:**
```
MemoryError
```

**Cause:** Dataset too large for available memory.

**Solution:**
1. Sample the data first:
```python
import pandas as pd
df = pd.read_csv("large_file.csv")
df.sample(n=100000).to_csv("sampled.csv", index=False)
```

2. Use a machine with more RAM

---

### Separator Issue

**Error:**
```
Error> The 3 mandatory fields/columns have not been identified
```

**Cause:** Wrong separator specified.

**Solution:**
Specify correct separator:
```bash
# For semicolon-separated files
python pmdqa.py -filename data.csv -pfi id -sn event -t timestamp -separator ";"

# For tab-separated files
python pmdqa.py -filename data.tsv -pfi id -sn event -t timestamp -separator $'\t'
```

---

## Data Quality Issues

### All Timestamps Show 0 Matches

**Issue:** Date format check shows 0 matches for all formats.

**Cause:** Your timestamp format is not in the supported list.

**Solution:**
1. Check your timestamp format:
```python
import pandas as pd
df = pd.read_csv("data.csv", nrows=5)
print(df["timestamp_column"].head())
```

2. Add your format to `pydqa4pm/utils/constants.py`:
```python
FMT_11 = "%Y/%m/%d %H:%M"  # Your format
FMT.append(FMT_11)
```

---

### Too Many Rejected Rows

**Issue:** High number of rows in reject files.

**Diagnosis:**
1. Check `*-read.rejects` for structural issues
2. Check `*-3keys.rejects` for missing values

**Common causes:**
- Inconsistent number of columns
- Missing values in mandatory fields
- Incorrect separator

**Solution:**
```python
# Check for inconsistent rows
with open("data.csv", "r") as f:
    for i, line in enumerate(f.readlines()[:100]):
        print(f"Line {i}: {len(line.split(','))} columns")
```

---

### Duplicate Count Wrong

**Issue:** Duplicate count doesn't match expectations.

**Explanation:** Duplicates are counted based on all 3 keys (PFI + SN + T).

**To verify:**
```python
import pandas as pd

df = pd.read_csv("data.csv")
dups = df.duplicated(subset=["case_id", "activity", "timestamp"])
print(f"Duplicates: {dups.sum()}")
print(df[dups])
```

---

## Report Generation Issues

### PDF Not Generated

**Error:**
```
Error> Failed to create date format table
```

**Cause:** Chart generation failed.

**Solution:**
1. Check log file `pydqa4pm.log` for details
2. Ensure temp folder can be created:
```python
import os
os.makedirs("temp-pydqa4pm", exist_ok=True)
```

3. Check matplotlib backend:
```python
import matplotlib
matplotlib.use('Agg')
```

---

### Logo Not Found

**Error:**
```
RuntimeError: cannot open resource
```

**Cause:** `assets/pi.png` file missing.

**Solution:**
1. Ensure assets folder exists in project root
2. Or modify `pdf_builder.py` to remove logo

---

### Empty or Corrupted PDF

**Issue:** PDF file is empty or cannot be opened.

**Solution:**
1. Delete existing PDF and regenerate
2. Check disk space
3. Ensure no other process is accessing the file

---

## Performance Issues

### Analysis Takes Too Long

**Issue:** Processing takes many minutes.

**Solutions:**

1. **Sample your data:**
```python
import pandas as pd
df = pd.read_csv("large_file.csv")
df.sample(n=100000).to_csv("sampled.csv", index=False)
```

2. **Reduce chart limit:**
In `constants.py`:
```python
LIMIT_BARH_DISPLAY = 15
```

3. **Use SSD storage**

---

### High Memory Usage

**Issue:** Process uses too much RAM.

**Solutions:**

1. Close other applications
2. Sample the data before analysis
3. Use 64-bit Python
4. Process files sequentially, not in parallel

---

## Getting More Help

### Check the Log File

```bash
cat pydqa4pm.log
tail -100 pydqa4pm.log
```

### Enable Debug Mode

```python
from pydqa4pm.utils import constants as C
import logging
C.TRACE_LEVEL = logging.DEBUG
```

### Report an Issue

Gather information:
- Python version (`python --version`)
- OS and version
- Error message (full traceback)
- Log file contents
- Sample data (anonymized)

Open a GitHub issue:
[https://github.com/datacorner/pyDQA4ProcessMining/issues](https://github.com/datacorner/pyDQA4ProcessMining/issues)

Or contact: benoit@datacorner.fr

---

## Quick Reference

| Error | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| `FileNotFoundError` | Wrong file path | Use absolute path |
| `Column not found` | Case mismatch | Check exact names |
| `UnicodeDecodeError` | Wrong encoding | Convert to UTF-8 |
| `MemoryError` | File too large | Sample data |
| `0 date matches` | Unknown format | Add format to constants |
| `PDF not created` | Chart error | Check log file |
| `ModuleNotFoundError` | Not installed | Run `pip install .` |

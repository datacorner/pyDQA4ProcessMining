# Project pyDQA4ProcessMining
This program aims to check the data (given by a CSV file) before importing a Process Mining solition (like Blue Prism Process Intelligence, alias BPPI). It's strongly recommended to profile the data before importing them into the Process Mining solution so as to avoid any issues(technical or worse misunderstanding on the data). 
The program provides as output (in the same directory) a pdf report with all the control results and charts.
# Requirements (Python)
* [Python 3.10.x minimum](https://www.python.org/downloads/release/python-3100)
* Python library: Several Python packages are necessary, to install them just execute the command below
```
pip install -r requirements.txt
```
# Data Quality Checks performed (DQA)
These are the data checks performed on the given dataset:
  * Check if the CSV can be opened successfully
  * Check if the 3 keys exist in the CSV file
  * Check if there are Null Values in the 3 keys (mandatory) --> Create a reject files accordindly with the bad rows, and remove them from the the next profiling analysis
  * Count the rows, columns, Number of duplicates (3 keys)
  * Validate the Date formats (Timestamp must satisfy specific date formats for BPPI)
# Files generated:
  * **[filename]-3keys.rejects** contains all the liens with issues in one of the 3 keys
  * **[filename]-read.rejects** contains all the rejected lines (while reading the file, these rejects are due to structural issues)
  * **[filename]-report.pdf** this is the summary report in a pdf format
  * **[filename]-events.csv** this file contains all the unique events (unduplicates) with their frequency
Note: [filename] is the name (with folder) of the source (dataset) file analysed.
# Command line Execution/Arguments
Program name dqa4bppi.py  
* **-filename** file to analyze (always csv)
* **-pfi** PFI key (Timeline ID)
* **-sn** SN key (Event ID)
* **-t** T key (Timestamp)
* **-separator** [ Optional | Default is comma]: CSV file Separator
# Example
Launch the program in the command line like this:
```
$ python3 main.py InternationalDeclarations.csv id concept:name time:timestamp
```
# Sample reports
* [International Declarations](https://github.com/datacorner/pyDQA4ProcessMining/tree/main/samples/InternationalDeclarations-report.pdf)
* [Very simple report](https://github.com/datacorner/pyDQA4ProcessMining/tree/main/samples/data-report.pdf)

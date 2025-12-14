#!/usr/bin/env python3
"""
pyDQA4ProcessMining - Data Quality Assessment Tool for Process Mining

This program validates and profiles CSV datasets before importing them
into Process Mining solutions. It generates a comprehensive PDF report
with quality metrics, charts, and statistics.

Author: Benoit CAYLA (benoit@datacorner.fr)
License: GPL

Usage:
    python pmdqa.py -filename <csv_file> -pfi <timeline_id> -sn <event_id> -t <timestamp>

Example:
    python pmdqa.py -filename data.csv -pfi case_id -sn activity -t timestamp
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import argparse
import sys

from pydqa4pm import Dqa4PM, Logger, __version__


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="pmdqa",
        description="Data Quality Assessment Tool for Process Mining",
        epilog="For more information, visit: https://github.com/datacorner/pyDQA4ProcessMining"
    )
    
    parser.add_argument(
        "-filename",
        help="Path to the CSV file to analyze",
        required=True
    )
    parser.add_argument(
        "-pfi",
        help="Column name for Timeline ID (Process Flow Identifier)",
        required=True
    )
    parser.add_argument(
        "-sn",
        help="Column name for Event ID (Step Name)",
        required=True
    )
    parser.add_argument(
        "-t",
        help="Column name for Timestamp",
        required=True
    )
    parser.add_argument(
        "-separator",
        help="CSV field separator (default: comma)",
        default=","
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    return parser


def main() -> int:
    """Main entry point for the DQA tool."""
    parser = create_parser()
    
    try:
        args = parser.parse_args()
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1
    
    # Initialize logger and DQA processor
    logger = Logger(__name__)
    dqa = Dqa4PM(logger)
    
    # Run analysis
    logger.info("=" * 60)
    logger.info(f"pyDQA4ProcessMining v{__version__}")
    logger.info("=" * 60)
    logger.info("Starting Analysis")
    
    try:
        dqa.process(
            args.filename,
            args.separator,
            args.pfi,
            args.sn,
            args.t
        )
        logger.info("Analysis Complete")
        return 0
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

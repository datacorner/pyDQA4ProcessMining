"""
PDF report builder for pyDQA4ProcessMining.

Generates comprehensive PDF reports from DQA analysis results.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import os
from fpdf import FPDF

from pydqa4pm.core.report_data import DQAReportData


class PDFReportBuilder(FPDF):
    """
    Generates PDF reports from DQA analysis results.
    
    Creates a multi-page PDF document with:
    - Dataset information and statistics
    - Sample data preview
    - Timeline ID analysis with charts
    - Event ID analysis with frequency distribution
    - Timestamp format validation results
    
    Example:
        >>> builder = PDFReportBuilder()
        >>> builder.create(dqa_report_data)
        >>> builder.output("report.pdf", "F")
    """
    
    # Path to logo relative to package
    LOGO_PATH = "assets/pi.png"
    
    def __init__(self):
        """Initialize the PDF report builder."""
        super().__init__()
        self.WIDTH = 210   # A4 width in mm
        self.HEIGHT = 297  # A4 height in mm
        
        # Find logo path (relative to project root)
        self._logo_path = self._find_logo()
    
    def _find_logo(self) -> str:
        """Find the logo file path."""
        # Try relative to current working directory
        if os.path.exists(self.LOGO_PATH):
            return self.LOGO_PATH
        
        # Try relative to package location
        package_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logo_path = os.path.join(package_dir, self.LOGO_PATH)
        if os.path.exists(logo_path):
            return logo_path
        
        return self.LOGO_PATH  # Return default, may fail

    def header(self) -> None:
        """Render the page header with logo and title."""
        try:
            self.image(self._logo_path, 10, 8, 50)
        except Exception:
            pass  # Skip logo if not found
        
        self.set_font('Arial', 'I', 8)
        self.cell(self.WIDTH - 80)
        self.cell(10, 1, 'Process Mining - Data Quality Assessment Report', 0, 0, 'L')
        self.ln(20)

    def footer(self) -> None:
        """Render the page footer with page number."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 6)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def insert_title(self, text: str) -> None:
        """Insert a section title."""
        self.set_font('Arial', 'BU', 11)
        self.set_text_color(0)
        self.cell(0, 10, text, 0, 0, 'L')
        self.ln('')
    
    # Backward compatibility alias
    def insertTitle(self, text):
        self.insert_title(text)

    def insert_image_title(self, text: str) -> None:
        """Insert a title above an image."""
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0)
        self.cell(0, 10, text, 0, 0, 'L')
        self.ln('')
    
    # Backward compatibility alias
    def insertImageTitle(self, text):
        self.insert_image_title(text)

    def insert_head_text(self, text: str) -> None:
        """Insert bold label text."""
        self.set_font('Arial', 'B', 8)
        self.set_text_color(0)
        self.cell(50, 0, text, 0, 0, 'L')
    
    # Backward compatibility alias
    def insertHeadText(self, text):
        self.insert_head_text(text)

    def insert_value_text(self, text: str) -> None:
        """Insert normal value text."""
        self.set_font('Arial', '', 8)
        self.set_text_color(0)
        self.cell(0, 0, text, 0, 0, 'L')
    
    # Backward compatibility alias
    def insertValueText(self, text):
        self.insert_value_text(text)

    def insert_text_and_value(self, label: str, value: str) -> None:
        """Insert a label-value pair."""
        self.insert_head_text(label)
        self.insert_value_text(value)
        self.add_break()
    
    # Backward compatibility alias
    def insertTextAndValue(self, text, value):
        self.insert_text_and_value(text, value)

    def add_break(self) -> None:
        """Add a line break."""
        self.ln(5)
    
    # Backward compatibility alias
    def addBreak(self):
        self.add_break()

    def insert_image(self, title: str, filename: str) -> None:
        """Insert an image with a title."""
        self.insert_image_title(title)
        try:
            self.image(filename, None, None, self.WIDTH - 30)
        except Exception:
            self.insert_value_text(f"[Image not available: {filename}]")
        self.ln('')
    
    # Backward compatibility alias
    def insertImage(self, _title, _filename):
        self.insert_image(_title, _filename)

    def build_report(self, dqa: DQAReportData) -> None:
        """
        Build the complete report content.
        
        Args:
            dqa: DQAReportData containing all analysis results.
        """
        # Dataset Information Section
        self.insert_title("Dataset Information")
        self.insert_text_and_value("Filename:", dqa.filename)
        self.insert_text_and_value("(PFI) Timeline ID:", dqa.PFIKey)
        self.insert_text_and_value("(SN) Event ID:", dqa.SNKey)
        self.insert_text_and_value("(T) Timestamp:", dqa.TKey)
        
        # Attributes list
        self.insert_head_text("Additional Attributes:")
        self.add_break()
        for attr in dqa.attributes:
            self.insert_value_text(f"      - {attr}")
            self.add_break()
        self.add_break()
        
        # Statistics
        self.insert_text_and_value("Number of Columns:", str(dqa.ColCount))
        self.insert_text_and_value("Number of Rows:", str(dqa.RowCount))
        self.add_break()
        
        # Quality metrics
        self.insert_text_and_value("Rejected Rows:", str(dqa.rejects))
        self.insert_text_and_value("- Missing Timeline ID:", str(dqa.missings[0]))
        self.insert_text_and_value("- Missing Event ID:", str(dqa.missings[1]))
        self.insert_text_and_value("- Missing Timestamp:", str(dqa.missings[2]))
        self.insert_text_and_value("Duplicate Rows:", str(dqa.duplicates))
        
        # Sample Data
        self.insert_image("Sample Data (First 5 Rows)", dqa.tableSampleData)
        
        # Timeline ID Analysis
        self.insert_title("(PFI) TIMELINE ID Analysis")
        self.insert_text_and_value("Distinct Timelines:", str(dqa.distinctPFI))
        self.insert_image("Most Frequent Timeline IDs", dqa.chartPFIValCount)
        
        # Event ID Analysis
        self.insert_title("(SN) EVENT ID Analysis")
        self.insert_text_and_value("Distinct Events:", str(dqa.distinctSN))
        self.insert_image("Event Frequency Distribution", dqa.chartSNValCount)
        self.insert_image("Events per Timeline Size", dqa.chartAggSNPerPFISIze)
        
        # Timestamp Analysis
        self.insert_title("(T) TIMESTAMP Analysis")
        self.insert_image("Date Format Validation", dqa.chartDatesFormat)
    
    # Backward compatibility alias
    def buildReport(self, dqa):
        self.build_report(dqa)

    def create(self, dqa: DQAReportData) -> None:
        """
        Create the PDF report.
        
        Args:
            dqa: DQAReportData containing all analysis results.
        """
        self.add_page()
        self.build_report(dqa)
    
    # Backward compatibility alias
    def Create(self, dqa):
        self.create(dqa)


# Backward compatibility alias
DQA4BPPIReportBuilder = PDFReportBuilder


__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from fpdf.fpdf import FPDF

#from dqareport import DQAReport
# https://pyfpdf.readthedocs.io/en/latest/

# This class builds and generates the PDF report
class DQA4BPPIReportBuilder(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        self.image('assets/pi.png', 10, 8, 50)
        self.set_font('Arial', 'I', 8)
        self.cell(self.WIDTH - 80)
        self.cell(10, 1, 'Blue Prism Process Intelligence - Data Quality Report', 0, 0, 'L')
        self.ln(20)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 6)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
    
    def insertTitle(self, text):
        self.set_font('Arial', 'BU', 11)
        self.set_text_color(0)
        self.cell(0, 10, text, 0, 0, 'L')
        self.ln('')
        
    def insertImageTitle(self, text):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0)
        self.cell(0, 10, text, 0, 0, 'L')
        self.ln('')
        
    def insertHeadText(self, text):
        self.set_font('Arial', 'B' , 8)
        self.set_text_color(0)
        self.cell(50, 0, text, 0, 0, 'L')

    def insertValueText(self, text):
        self.set_font('Arial', '' , 8)
        self.set_text_color(0)
        self.cell(0, 0, text, 0, 0, 'L')
        
    def insertTextAndValue(self, text, value):
        self.insertHeadText(text)
        self.insertValueText(value)
        self.addBreak()
        
    def addBreak(self):
        self.ln(5)

    def insertImage(self, _title, _filename):
        self.insertImageTitle(_title)
        self.image(_filename, None, None, self.WIDTH - 30)
        self.ln('')

    # Build the final report :
    def buildReport(self, dqa):
        # Global informations
        self.insertTitle("Dataset informations")
        self.insertTextAndValue("Filename (dataset):", dqa.filename )
        self.insertTextAndValue("(PFI) Timeline ID:", dqa.PFIKey )
        self.insertTextAndValue("(SN) Event ID:", dqa.SNKey )
        self.insertTextAndValue("(T) Timestamp:", dqa.TKey )
        self.insertHeadText("Potential attributes:")
        self.addBreak()
        str_attr = ""
        for att in dqa.attributes:
            self.insertValueText("      - " + att)
            self.addBreak()
        self.addBreak()
        self.insertTextAndValue("Number of Columns:", str(dqa.ColCount) )
        self.insertTextAndValue("Number of Rows:", str(dqa.RowCount) )
        self.addBreak()
        self.insertTextAndValue("Number of Rejected rows:", str(dqa.rejects) )
        self.insertTextAndValue("- Missing Timeline ID:", str(dqa.missings[0]))
        self.insertTextAndValue("- Missing Event ID:", str(dqa.missings[1]))
        self.insertTextAndValue("- Missing Timestamp:", str(dqa.missings[2]))
        self.insertTextAndValue("Number of duplicates:", str(dqa.duplicates))
        
        # Sample data (first 5 rows)
        self.insertImage("Sample data", dqa.tableSampleData)
        
        # Per mandatory fields : PFI
        self.insertTitle("(PFI) TIMELINE ID")
        self.insertTextAndValue("Number Timelines (PFI):", str(dqa.distinctPFI) )
        self.insertImage("Most common values", dqa.chartPFIValCount)
        # Per mandatory fields : SN
        self.insertTitle("(SN) EVENT ID")
        self.insertTextAndValue("Number of events (SN):", str(dqa.distinctSN) )
        self.insertImage("All Events by Frequency distribution", dqa.chartSNValCount)
        self.insertImage("Number of events per Timeline size", dqa.chartAggSNPerPFISIze)
        
        # Per mandatory fields : T
        self.insertTitle("(T) TIMESTAMP")
        self.insertImage("Date Format Check for BPPI", dqa.chartDatesFormat)

    def Create(self, dqa):
        self.add_page()
        self.buildReport(dqa)
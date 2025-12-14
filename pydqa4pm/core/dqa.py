"""
Main DQA processing orchestrator for pyDQA4ProcessMining.

Provides the Dqa4PM class that coordinates the entire data quality assessment workflow.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from pydqa4pm.core.datasource import DataSource
from pydqa4pm.core.report_data import DQAReportData
from pydqa4pm.charts.seaborn_chart import SeabornChart
from pydqa4pm.charts.base import Chart
from pydqa4pm.reports.store import ReportStore
from pydqa4pm.reports.pdf_builder import PDFReportBuilder
from pydqa4pm.utils import constants as C


class Dqa4PM:
    """
    Main orchestrator for the Data Quality Assessment process.
    
    This class coordinates the entire DQA workflow:
    1. Open and validate the CSV dataset
    2. Perform data quality checks
    3. Generate charts and visualizations
    4. Create the PDF report
    
    Example:
        >>> from pydqa4pm import Dqa4PM, Logger
        >>> 
        >>> log = Logger("main")
        >>> dqa = Dqa4PM(log)
        >>> dqa.process("data.csv", ",", "case_id", "activity", "timestamp")
    """
    
    def __init__(self, trace):
        """
        Initialize the DQA processor.
        
        Args:
            trace: Logger instance for output messages.
        """
        self._trace = trace
    
    @property
    def T(self):
        """Get the logger instance."""
        return self._trace
    
    def open_dataset(self, filename: str, sep: str, pfi: str, sn: str, t: str) -> DataSource:
        """
        Open and validate the CSV dataset.
        
        Args:
            filename: Path to the CSV file.
            sep: Field separator character.
            pfi: Timeline ID column name.
            sn: Event ID column name.
            t: Timestamp column name.
        
        Returns:
            DataSource instance (check is_opened() for success).
        """
        ds = DataSource(filename, pfi, sn, t)
        
        self.T.info("Opening dataset ...")
        ds.open(sep)
        
        self.T.info(
            "Lines rejected (structure issues): <", ds.readRejectsCount, 
            "> | File: <", ds.readRejectFilename, ">"
        )
        
        if ds.isOpened():
            self.T.info("Data Quality Check for file: <", filename, ">")
            check, message = ds.check3PKeys()
            
            if check:
                self.T.info(
                    "Mandatory fields identified: PFI->", pfi, 
                    ", SN->", sn, ", T->", t
                )
                key_reject_count = ds.dump3KeysRejectFile()
                self.T.info(
                    "Lines rejected (key validation): <", key_reject_count,
                    "> | File: <", ds.keysRejectFilename, ">"
                )
            else:
                self.T.error(message)
                self.T.info("Mandatory columns not found. Please check column names.")
        else:
            self.T.error("Error while opening the file.")
        
        return ds
    
    # Backward compatibility alias
    def OpenDataset(self, filename, sep, pfi, sn, t):
        return self.open_dataset(filename, sep, pfi, sn, t)

    def make_dqa_checks(self, ds: DataSource) -> DQAReportData:
        """
        Perform all data quality checks on the dataset.
        
        Args:
            ds: The opened DataSource instance.
        
        Returns:
            DQAReportData containing all check results.
        """
        dqa = DQAReportData(ds.filename, ds.PFI, ds.SN, ds.T)
        
        try:
            self.T.info("Performing data quality checks ...")
            
            dqa.attributes = ds.attributes
            dqa.missings = ds.missingValues()
            dqa.rejects = ds.rejectRows
            dqa.dateFormatsCheck = ds.checkBPPIDateFormats()
            dqa.ColCount = ds.colsCount()
            dqa.RowCount = ds.rowsCount()
            dqa.duplicates = ds.checkDuplicatesCount()
            dqa.uniques = [
                ds.countUniqueValues(ds.PFI),
                ds.countUniqueValues(ds.SN),
                ds.countUniqueValues(ds.T)
            ]
            dqa.distinctPFI = ds.countDistinctValues(ds.PFI)
            dqa.distinctSN = ds.countDistinctValues(ds.SN)
            dqa.PFIMostFreq = ds.getCountValuesForField(ds.PFI, C.LIMIT_BARH_DISPLAY)
            dqa.SNValues = ds.getCountValuesForField(ds.SN, C.LIMIT_BARH_DISPLAY)
            dqa.firstData = ds.head(5)
            dqa.PFICountPerSN = ds.getSNCountPerPFISize()
            
            self.T.info("Dataset checks completed successfully")
            dqa.AllChecksOK = True
            
        except Exception as e:
            self.T.error("Error during checks: {}".format(e))
            dqa.AllChecksOK = False
        
        return dqa
    
    # Backward compatibility alias
    def MakeDQAChecks(self, ds):
        return self.make_dqa_checks(ds)

    def build_charts(self, dqa: DQAReportData, store: ReportStore) -> bool:
        """
        Generate all charts and tables for the report.
        
        Args:
            dqa: The DQAReportData containing analysis results.
            store: The ReportStore for temporary file management.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.T.info("Generating charts and tables ...")
            
            # Date format check table
            dqa.chartDatesFormat = Chart(10, 2).CreateTable(
                store.getPath(C.FILE_FORMAT_TABLE),
                dqa.dateFormatsCheck
            )
            if dqa.chartDatesFormat == C.NO_FILE_CREATED:
                self.T.error("Failed to create date format table")
            
            # Sample data table
            dqa.tableSampleData = Chart(20, 1).CreateTable(
                store.getPath(C.FILE_SAMPLES_TABLE),
                dqa.firstData
            )
            if dqa.tableSampleData == C.NO_FILE_CREATED:
                self.T.error("Failed to create sample data table")
            
            # PFI frequency chart
            dqa.chartPFIValCount = SeabornChart(10, 6).CreateBarH(
                store.getPath(C.FILE_PFI_CHART),
                dqa.PFIMostFreq,
                C.FLD_COL_VALUECOUNT,
                C.FLD_FREQ_VALUECOUNT,
                "",
                "Lines per Timeline"
            )
            if dqa.chartPFIValCount == C.NO_FILE_CREATED:
                self.T.error("Failed to create PFI frequency chart")
            
            # SN frequency chart
            dqa.chartSNValCount = SeabornChart(10, 6).CreateBarH(
                store.getPath(C.FILE_SNMOSTFQ_CHART),
                dqa.SNValues,
                C.FLD_COL_VALUECOUNT,
                C.FLD_FREQ_VALUECOUNT,
                "",
                "Event Frequency"
            )
            if dqa.chartSNValCount == C.NO_FILE_CREATED:
                self.T.error("Failed to create SN frequency chart")
            
            # Timeline size distribution scatter plot
            dqa.chartAggSNPerPFISIze = SeabornChart(10, 6).CreateScatter(
                store.getPath(C.FILE_COUNTPFIEVTS_CHART),
                dqa.PFICountPerSN,
                C.FLD_SN_NB,
                C.FLD_PFI_NB,
                C.FLD_SN_NB,
                C.FLD_PFI_NB
            )
            if dqa.chartAggSNPerPFISIze == C.NO_FILE_CREATED:
                self.T.error("Failed to create timeline size chart")
            
            self.T.info("Charts generated successfully")
            return True
            
        except Exception as e:
            self.T.error("Error generating charts: {}".format(e))
            return False
    
    # Backward compatibility alias
    def BuildCharts(self, dqa, store):
        return self.build_charts(dqa, store)

    def generate_report(self, dqa: DQAReportData, report_name: str) -> None:
        """
        Generate the PDF report.
        
        Args:
            dqa: The DQAReportData containing all results.
            report_name: Output path for the PDF file.
        """
        pdf = PDFReportBuilder()
        pdf.create(dqa)
        pdf.output(report_name, 'F')
        self.T.info("Report created: " + report_name)
    
    # Backward compatibility alias
    def GenerateReport(self, dqa, reportname):
        self.generate_report(dqa, reportname)

    def create_alternative_data(self, ds: DataSource) -> None:
        """
        Create supplementary output files (events list).
        
        Args:
            ds: The DataSource instance.
        """
        num_events = ds.dumpUniqueEvents()
        self.T.info(
            "Events file created: <", ds.uniqueEventsFilename,
            "> with <", num_events, "> unique events"
        )
    
    # Backward compatibility alias
    def CreateAlternativeData(self, ds):
        self.create_alternative_data(ds)

    def process(self, dataset_filename: str, separator: str, 
                pfi_key: str, sn_key: str, t_key: str) -> None:
        """
        Run the complete DQA workflow.
        
        Args:
            dataset_filename: Path to the CSV file.
            separator: Field separator character.
            pfi_key: Timeline ID column name.
            sn_key: Event ID column name.
            t_key: Timestamp column name.
        """
        # Open and validate dataset
        ds = self.open_dataset(dataset_filename, separator, pfi_key, sn_key, t_key)
        
        if not ds.isOpened():
            return
        
        # Initialize temporary storage
        store = ReportStore()
        self.T.debug("Initializing temporary storage")
        store.initialize()
        
        # Perform DQA checks
        self.T.info("Performing data quality checks")
        dqa = self.make_dqa_checks(ds)
        
        # Generate events file
        self.T.info("Creating supplementary files")
        self.create_alternative_data(ds)
        
        if dqa.AllChecksOK:
            # Generate charts
            self.T.info("Building charts")
            if self.build_charts(dqa, store):
                # Generate PDF report
                report_name = ds.filenameWithoutExt + C.SUFFIX_REPORT
                self.T.info("Generating report: {}".format(report_name))
                self.generate_report(dqa, report_name)
        
        # Cleanup
        self.T.info("Cleaning up temporary files")
        store.finalize()
    
    # Backward compatibility alias
    def Process(self, dataset_filename, separator, pfi_key, ps_key, t_key):
        self.process(dataset_filename, separator, pfi_key, ps_key, t_key)


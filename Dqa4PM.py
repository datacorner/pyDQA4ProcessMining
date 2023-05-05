import sys
from log import log
from datasource import DataSource
from matplotlibChart import MatplotlibChart
from seabornChart import SeabornChart
from chart import Chart
from DQAReportData import DQAReportData
from reportstore import ReportStore
from pdfreportbuilder import DQA4BPPIReportBuilder
import constants as C

class Dqa4PM:
    def __init__(self, trace):
        self.__trace = trace
        return
    
    @property
    def T(self):
        return self.__trace
    
    # Open the CSV file - dataset - in entry
    def OpenDataset(self, filename, sep, pfi, sn, t):
        ds = DataSource(filename, pfi, sn, t)
        self.T.info ("Open dataset ...")
        ds.open(sep)
        self.T.info ("Number or lines rejected (Structure issues) < ", ds.readRejectsCount, " > | dump in file < ", ds.readRejectFilename, " >" )
        if (ds.isOpened()):
            self.T.info ("Data Quality Check for the file < ", filename, " >" )
            check, message = ds.check3PKeys()
            if (check):
                self.T.info("The 3 mandatory (PFI->", pfi, ", SN->", sn, ", T->", t,") fields have been identified successfully in the dataset")
                keyRejCount = ds.dump3KeysRejectFile()  # Generate the reject file with the bad rows
                self.T.info ("Number or lines rejected (3 mandatory keys validity) < ", keyRejCount, " > | dump in file < ", ds.keysRejectFilename, " >" )
            else:
                self.T.error(message)
                self.T.info("The 3 mandatory fields/columns have not been identified in the dataset, please specify 3 existing columns")
        else:
            self.T.error("Error while opening the file.")
        return ds

    # Make the checks & calculations
    def MakeDQAChecks(self, ds):
        dqa = DQAReportData(ds.filename, ds.PFI, ds.SN, ds.T)
        try:
            self.T.info("Making checks and validation of the dataset ...")
            dqa.attributes = ds.attributes
            dqa.missings = ds.missingValues()                   # set missing values for the three columns
            dqa.rejects = ds.rejectRows                         # Get rejected rows
            dqa.dateFormatsCheck = ds.checkBPPIDateFormats()    # Check the timestamp date format (for all the accepted formats)
            dqa.ColCount = ds.colsCount()                       # Column Count
            dqa.RowCount = ds.rowsCount()                       # Row Count
            dqa.duplicates = ds.checkDuplicatesCount()          # Number of duplicates (3 keys)
            dqa.uniques = [ ds.countUniqueValues(ds.PFI), ds.countUniqueValues(ds.SN), ds.countUniqueValues(ds.T) ]  # set the number of unique values for the 3 keys
            dqa.distinctPFI = ds.countDistinctValues(ds.PFI)    # Set the Number of distinct values for PFI
            dqa.distinctSN = ds.countDistinctValues(ds.SN)      # Set the Number of distinct values for SN
            dqa.PFIMostFreq = ds.getCountValuesForField(ds.PFI, C.LIMIT_BARH_DISPLAY)   # Get the 30 most frequent PFI values (Timeline ID)
            dqa.SNValues = ds.getCountValuesForField(ds.SN, C.LIMIT_BARH_DISPLAY)       # Get (all) the most frequent PS values (Event ID)
            dqa.firstData = ds.head(5)                          # first data rows
            dqa.PFICountPerSN = ds.getSNCountPerPFISize()       # Count the Nb of timelines with their nb of events
            self.T.info("Dataset processed successfully")
            dqa.AllChecksOK = True
        except Exception as e:
            self.T.error("Error while making checks, error= {}".str(e))
            dqa.AllChecksOK = False
            return dqa
        return dqa

    # Build the charts & Tables
    def BuildCharts(self, dqa, store):
        try:
            # Build table with Date formats checks
            self.T.info("Build table and charts ...")
            dqa.chartDatesFormat = Chart(10, 2).CreateTable(store.getPath(C.FILE_FORMAT_TABLE), dqa.dateFormatsCheck)
            if (dqa.chartDatesFormat == C.NO_FILE_CREATED):
                dqa.chartDatesFormat ("Impossible to create the date format checks chart.")
            # Build Table Sample data
            dqa.tableSampleData = Chart(20, 1).CreateTable(store.getPath(C.FILE_SAMPLES_TABLE), dqa.firstData)
            if (dqa.tableSampleData == C.NO_FILE_CREATED):
                self.T.error ("Impossible to create the sample dataset table.")
            # Build the chart for the 10 most frequent PFI values (Timeline ID)
            dqa.chartPFIValCount = SeabornChart(10, 6).CreateBarH(store.getPath(C.FILE_PFI_CHART), dqa.PFIMostFreq, C.FLD_COL_VALUECOUNT, C.FLD_FREQ_VALUECOUNT, "", "Nb of lines / Timeline")
            if (dqa.chartPFIValCount == C.NO_FILE_CREATED):
                self.T.error ("Impossible to create the PFI most frequent value bar chart.")
            # Build the chart for the 10 most frequent PS values (Event ID)
            dqa.chartSNValCount = SeabornChart(10, 6).CreateBarH(store.getPath(C.FILE_SNMOSTFQ_CHART), dqa.SNValues, C.FLD_COL_VALUECOUNT, C.FLD_FREQ_VALUECOUNT, "", "Events Frequency")
            if (dqa.chartSNValCount == C.NO_FILE_CREATED):
                self.T.error ("Impossible to create the SN most frequent value bar chart.")
            # Count the Nb of timelines with their nb of events
            dqa.chartAggSNPerPFISIze = SeabornChart(10, 6).CreateScatter(store.getPath(C.FILE_COUNTPFIEVTS_CHART), dqa.PFICountPerSN, C.FLD_SN_NB, C.FLD_PFI_NB, C.FLD_SN_NB, C.FLD_PFI_NB)
            if (dqa.chartAggSNPerPFISIze == C.NO_FILE_CREATED):
                self.T.error ("Impossible to create the Nb Of events per Timeline size chart.")
            self.T.info("Table and charts processed successfully")
        except Exception as e:
            self.T.error("Error while generating charts, error= {}".str(e))
            return False
        return True

    # Generate the output PDF report
    def GenerateReport(self, dqa, reportname):
        pdf = DQA4BPPIReportBuilder()
        pdf.Create(dqa)
        pdf.output(reportname, 'F')
        self.T.info("The report (" + reportname + ") has been created successfully")
        return
    
    # Create alternative files
    #   - Create a file with all the events and their freq distribution
    def CreateAlternativeData(self, ds):
        nbevents = ds.dumpUniqueEvents()
        self.T.info ("A file < ", ds.uniqueEventsFilename ," > with all the < ", nbevents, " > unique events has been created")
        return
    
    # Main call (process everything)
    def Process(self, dataset_filename, separator, pfi_key, ps_key, t_key):
        ds = self.OpenDataset(dataset_filename, separator, pfi_key, ps_key, t_key)   # Open the Dataset
        if (ds.isOpened()):
            store = ReportStore()
            self.T.debug("Initialize the storage area (temporary)")
            store.initialize()
            self.T.info("Make the checks & calculations on the data")
            dqa = self.MakeDQAChecks(ds)
            self.T.info("Build external files to facilitate the analysis (events list, etc.)")
            self.CreateAlternativeData(ds)
            if (dqa.AllChecksOK):
                self.T.info("Build the charts")
                if (self.BuildCharts(dqa, store)):
                    reportname =  ds.filenameWithoutExt + C.SUFFIX_REPORT
                    self.T.info("Build the report {}".format(reportname))
                    self.GenerateReport(dqa, reportname)
            self.T.info("Cleaning temporary files")
            store.finalize() # Cleanse the temp stuff
        return
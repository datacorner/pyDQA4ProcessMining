import constants as C
import pandas as pd

# This class aims at storing all the necessary data to provide the DQA report
class DQAReportData:
    def __init__(self, p_filename, p_pfi, p_sn, p_t):
        self.__filename = p_filename
        self.__PFIKey = p_pfi
        self.__SNKey = p_sn
        self.__TKey = p_t
        self.__RowCount = 0
        self.__ColCount = 0
        self.__chartPFIValCount = C.NO_CHART_FILE
        self.__chartSNValCount = C.NO_CHART_FILE
        self.__tableSampleData = C.NO_CHART_FILE
        self.__chartDatesFormat = C.NO_CHART_FILE
        self.__chartAggSNPerPFISIze = C.NO_CHART_FILE
        self.__PFINbOfDistinctValue = 0
        self.__SNNbOfDistinctValue = 0
        self.__DuplicateCount = 0
        self.__rejects = 0
        self.__dataFormatsCheck = pd.DataFrame()
        self.__firstData = pd.DataFrame()
        self.__missingValues = [0, 0, 0] # 0 -> PFI, 1 -> SN, 2 -> T
        self.__uniquesValues = [0, 0, 0] # 0 -> PFI, 1 -> SN, 2 -> T
        self.__attributes = []
        self.__allchecksOK = False
        self.__SNValues = pd.DataFrame()
        self.__PFIMostFreq = pd.DataFrame()
        self.__PFICountPerSN = pd.DataFrame()

    @property
    def PFICountPerSN(self):
        return self.__PFICountPerSN
    @PFICountPerSN.setter   
    def PFICountPerSN(self, value):
        self.__PFICountPerSN = value

    @property
    def PFIMostFreq(self):
        return self.__PFIMostFreq
    @PFIMostFreq.setter   
    def PFIMostFreq(self, value):
        self.__PFIMostFreq = value

    @property
    def SNValues(self):
        return self.__SNValues
    @SNValues.setter   
    def SNValues(self, value):
        self.__SNValues = value

    @property
    def firstData(self):
        return self.__firstData
    @firstData.setter   
    def firstData(self, value):
        self.__firstData = value

    @property
    def AllChecksOK(self):
        return self.__allchecksOK
    @AllChecksOK.setter   
    def AllChecksOK(self, value):
        self.__allchecksOK = value

    # List of attributes (out of the 3 keys)
    @property
    def attributes(self):
        return self.__attributes
    @attributes.setter   
    def attributes(self, value):
        self.__attributes = value

    # Format check table
    @property
    def dateFormatsCheck(self):
        return self.__dataFormatsCheck
    @dateFormatsCheck.setter   
    def dateFormatsCheck(self, value):
        self.__dataFormatsCheck = value

    # dataset filename (CSV file)
    @property
    def filename(self):
        return self.__filename
    
    # Get fields/key names
    @property
    def PFIKey(self):
        return self.__PFIKey
    @property
    def SNKey(self):
        return self.__SNKey
    @property
    def TKey(self):
        return self.__TKey

    # Number of rejected lines/rows
    @property
    def rejects(self):
        return self.getRatioValCount(self.__rejects)
    @rejects.setter   
    def rejects(self, value):
        self.__rejects = value

    # Number of duplicates (3 mandatory keys)
    @property
    def duplicates(self):
        return self.getRatioValCount(self.__DuplicateCount)
    @duplicates.setter   
    def duplicates(self, value):
        self.__DuplicateCount = value

    # Number or rows/lines
    @property
    def RowCount(self):
        return self.__RowCount
    @RowCount.setter   
    def RowCount(self, value):
        self.__RowCount = value

    # Number of Columns
    @property
    def ColCount(self):
        return self.__ColCount
    @ColCount.setter   
    def ColCount(self, value):
        self.__ColCount = value

    # Chart's filename showing the agg number of events per timeline size
    @property
    def chartAggSNPerPFISIze(self):
        return self.__chartAggSNPerPFISIze
    @chartAggSNPerPFISIze.setter   
    def chartAggSNPerPFISIze(self, value):
        self.__chartAggSNPerPFISIze = value

    # Chart's filename showing the Nb of values per PFI
    @property
    def chartPFIValCount(self):
        return self.__chartPFIValCount
    @chartPFIValCount.setter   
    def chartPFIValCount(self, value):
        self.__chartPFIValCount = value
    
    # Chart's filename showing the Nb of values per SN
    @property
    def chartSNValCount(self):
        return self.__chartSNValCount
    @chartSNValCount.setter   
    def chartSNValCount(self, value):
        self.__chartSNValCount = value

    # table's filename showing the 5 first lines
    @property
    def tableSampleData(self):
        return self.__tableSampleData
    @tableSampleData.setter   
    def tableSampleData(self, value):
        self.__tableSampleData = value

    # table's filename showing the date format checks
    @property
    def chartDatesFormat(self):
        return self.__chartDatesFormat
    @chartDatesFormat.setter   
    def chartDatesFormat(self, value):
        self.__chartDatesFormat = value

    # Table with uniques values [ PFI, SN, T ]
    @property
    def uniques(self):
        return self.__uniquesValues
    @uniques.setter   
    def uniques(self, value):
        self.__uniquesValues = value

    # Table with missing values [ PFI, SN, T ]
    @property
    def missings(self):
        return self.__missingValues
    @missings.setter   
    def missings(self, value):
        self.__missingValues = value
    
    # display the value and the ratio in % / global count
    def getRatioValCount(self, p_value):
        txt = str(p_value) + " / " + str(self.__RowCount) + " (" + str(round(p_value / self.__RowCount * 100, 2)) + "%)"
        return txt
    
    # Number of distinct values (field + Nb of values) for PFI
    @property
    def distinctPFI(self):
        return self.getRatioValCount(self.__PFINbOfDistinctValue)
    @distinctPFI.setter   
    def distinctPFI(self, value):
        self.__PFINbOfDistinctValue = value
    
    # Number of distinct values (field + Nb of values) for SN
    @property
    def distinctSN(self):
        return self.getRatioValCount(self.__SNNbOfDistinctValue)
    @distinctSN.setter
    def distinctSN(self, value):
        self.__SNNbOfDistinctValue = value

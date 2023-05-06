__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import pandas as pd
import constants as C
from datetime import datetime
from events import SNList

# utility Check Date format
def checkDateFormat(date, fmt):
    try:
        dummydate = datetime.strptime(date, fmt)
        return True
    except:
        return False

# This class manages the datasource by doing all the calculations & analytics on the data
class DataSource:
    def __init__(self, p_filename, p_pfi, p_sn, p_t):
        self.__filename = p_filename
        self.__dataset = pd.DataFrame()
        self.__keyname_PFI = p_pfi
        self.__keyname_SN = p_sn
        self.__keyname_T = p_t
        self.__initialNbRows = 0
        self.__potentialAttributes = []
        self.__rejectsReadLine = []

    # returns the Number of reject lines (whicle reading / structure issues)
    @property
    def readRejectsCount(self):
        return len(self.__rejectsReadLine)
    
    @property
    def readRejectFilename(self):
        return self.filenameWithoutExt + C.SUFFIX_READ_REJ
    @property
    def keysRejectFilename(self):
        return self.filenameWithoutExt + C.SUFFIX_3KEYS_REJECT
    @property
    def uniqueEventsFilename(self):
        return self.filenameWithoutExt + C.SUFFIX_EVENTS

    @property
    def PFI(self):
        return self.__keyname_PFI
    @property
    def SN(self):
        return self.__keyname_SN
    @property
    def T(self):
        return self.__keyname_T
    @property
    def filename(self):
        return self.__filename
    
    @property
    def attributes(self):
        return self.__potentialAttributes
    
    @property
    def filenameWithoutExt(self):
        try:
            return '.'.join(self.__filename.split('.')[:-1])
        except:
            return C.DEFAULT_REPORT_FILE
        
    @property
    def rejectRows(self):
        return self.__initialNbRows - self.__dataset.shape[0]
    
    # Returns True if the dataset is opened
    def isOpened(self):
        return not self.__dataset.empty
    
    # Return a DataFrame with the number of date which matches with the given formats (See the C.FMT array)
    def checkBPPIDateFormats(self):
        df = self.__dataset.copy()
        result = []
        # Check the date formats on the timestamp column
        for i in range(len(C.FMT)):
            df["FMT_" + str(i)] = df[self.__keyname_T].apply(checkDateFormat, fmt = C.FMT[i])
            # Count the good formats
            result.append(len(df[df["FMT_" + str(i)] == True]))
        final = pd.DataFrame(columns=['Format', 'GoodRows'])
        final['Format'] = C.FMT
        final['GoodRows'] = result
        return final
    
    # dump the rejected (read) lines in a file
    def dumpReadRejects(self):
        with open(self.readRejectFilename, 'w') as reject_file:
            for item in self.__rejectsReadLine:
                line = str(item) + " > " +str(len(item)) + " columns\n"
                reject_file.write(line)
        return len(self.__rejectsReadLine)

    # Add a new read reject line
    def addReadRejectLine(self, x):
        self.__rejectsReadLine.append(x)
        return
    
    # open the datasource and create a DataFrame accordingly
    def open(self, sep=","):
        try:
            self.__dataset = pd.read_csv(self.__filename, on_bad_lines=self.addReadRejectLine, engine='python', sep = sep)
            self.__initialNbRows = self.__dataset.shape[0]
            self.dumpReadRejects()
            return True, None
        except Exception as e:
            return False, e
        
    # Check if the 3 fields really exists into the dataset
    def check3PKeys(self):
        pfi_ok, sn_ok, t_ok = False, False, False
        pot_attr = []
        msg = ""
        try:
            for col in self.__dataset.columns:
                if (col == self.__keyname_PFI):
                    pfi_ok = True
                elif (col == self.__keyname_SN):
                    sn_ok = True
                elif (col == self.__keyname_T):
                    t_ok = True
                else:
                    self.__potentialAttributes.append(col)
            if (not pfi_ok):
                msg = msg + "Timeline ID column has not been found.\n"
            if (not sn_ok):
                msg = msg + "Event ID column has not been found.\n"
            if (not t_ok):
                msg = msg + "Timestamp column has not been found."
            return (pfi_ok and sn_ok and t_ok), msg
        except Exception as e:
            msg = "Error while opening the file, error is " + e
            return False, msg
    
    # return a data sample with always the 3 keys in first
    def head(self, p_first = 7):
        if (self.isOpened):
            return self.__dataset.head(p_first)
        else:
            return -1
    
    # return the Number of Fields/columns
    def colsCount(self):
        if (self.isOpened):
            return self.__dataset.shape[1]
        else:
            return -1
    
    # return the Number of rows
    def rowsCount(self):
        if (self.isOpened):
            return self.__dataset.shape[0]
        else:
            return -1

    # returns a dataframe with each column value and its number of uses (freq. distribution)
    # if limit equals to 0, no limitation on the dataset size, otherwise get the firsts (limit)
    def getCountValuesForField(self, p_col, p_limit = 0) -> pd.DataFrame: 
        if (self.isOpened):
            #Limit the number of data to display/store here
            df = self.__dataset.copy()
            counts = df[p_col].value_counts()
            colName = counts.index
            colFreq = counts
            res = pd.DataFrame(columns=[C.FLD_COL_VALUECOUNT, C.FLD_FREQ_VALUECOUNT])
            res[C.FLD_COL_VALUECOUNT] = colName
            res[C.FLD_FREQ_VALUECOUNT] = colFreq.values
            res = res.sort_values(by=[C.FLD_FREQ_VALUECOUNT], ascending=False)
            if (p_limit > 0):
                limit = p_limit if (res.shape[0] > p_limit) else res.shape[0]
                res = res.head(limit)
            return res
        else:
            return None

    # Count the Number of rows(events) grouped per timeline size (PFI)
    def getSNCountPerPFISize(self):
        df = self.getCountValuesForField(self.__keyname_PFI)
        dfagg = df[C.FLD_FREQ_VALUECOUNT].value_counts()
        colName = dfagg.index
        colFreq = dfagg
        res = pd.DataFrame(columns=[C.FLD_PFI_NB, C.FLD_SN_NB])
        res[C.FLD_PFI_NB] = colFreq.values
        res[C.FLD_SN_NB] = colName
        res = res.sort_values(by=[C.FLD_PFI_NB], ascending=False).reset_index(drop=True)
        return res

    # returns the number of distinct values for the column in parameter
    def countDistinctValues(self, p_colName):
        return len(self.__dataset[p_colName].value_counts())
    
    # Count the number of missing values per column
    def countMissingValues(self, p_colName):
        df = self.__dataset
        myCount = df[p_colName].isnull().sum().sum()
        return myCount
    
    # Count the number of missing values per column
    def countUniqueValues(self, p_colName):
        return self.__dataset[p_colName].nunique()
    
    # Calculate the number of rejects and remove the bad lines
    def missingValues(self):
        try:
            missing = []
            # Calculate the number of missing values for the 3 keys
            missing.append(self.countMissingValues(self.__keyname_PFI))
            missing.append(self.countMissingValues(self.__keyname_SN))
            missing.append(self.countMissingValues(self.__keyname_T))
            # drop the lines with empty key values to no false the next analysis
            self.__dataset.drop(self.__dataset[self.__dataset[self.__keyname_PFI].isnull()].index ,inplace=True)
            self.__dataset.drop(self.__dataset[self.__dataset[self.__keyname_SN].isnull()].index ,inplace=True)
            self.__dataset.drop(self.__dataset[self.__dataset[self.__keyname_T].isnull()].index ,inplace=True)
            return missing
        except:
            return [0, 0, 0]
        
    # Extract the rows with missing values in on of the three columns and put the bad rows/lines in a reject file
    def dump3KeysRejectFile(self):
        df_pfi = self.__dataset[self.__dataset[self.__keyname_PFI].isnull()]
        if (not df_pfi.empty):
            df_pfi.insert(0, C.REJECT_COL_NAME, "BPPI Timeline ID is Empty")
        df_sn = self.__dataset[self.__dataset[self.__keyname_SN].isnull()]
        if (not df_sn.empty):
            df_sn.insert(0, C.REJECT_COL_NAME,  "BPPI Event ID is Empty")
        df_t = self.__dataset[self.__dataset[self.__keyname_T].isnull()]
        if (not df_t.empty):
            df_t.insert(0, C.REJECT_COL_NAME,  "BPPI Timestamp is Empty")
        df_global = pd.concat([df_pfi, df_sn, df_t])
        df_global.to_csv(self.keysRejectFilename)
        return df_global.shape[0]
        
    # return the number of Duplicates considering the 3 mandatory fields
    def checkDuplicatesCount(self):
        dups = self.__dataset.duplicated(subset=[self.__keyname_PFI, self.__keyname_SN, self.__keyname_T])
        return len(dups[dups == True])
    
    # Get the event
    def dumpUniqueEvents(self):
        df = self.getCountValuesForField(self.SN)
        if (not df.empty):
            evts = SNList(df)
            evts.Cleanse()
            evts.SNList.to_csv(self.uniqueEventsFilename, index=False)
        return evts.SNList.shape[0]
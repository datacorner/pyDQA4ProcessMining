__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import pandas as pd
import constants as C
import re

# This class manages the Events/SN list
# Storage in __SNList (DataFrame)
#   * FLD_COL_VALUECOUNT: Original Column
#   * FLD_FREQ_VALUECOUNT: Frequency of the Event/SN value
#   * FLD_NEW_SN: New column created with the [FLD_COL_VALUECOUNT] cleansed / Proposal
class SNList:
    def __init__(self, df_events_list):
        self.__SNList = df_events_list
        if (not self.__SNList.empty):
            # Duplicate the SN/Event column value for the event workshop
            self.SNList.insert(1, C.FLD_NEW_SN, self.__SNList[C.FLD_COL_VALUECOUNT])     
        return
    
    @property   # DataFrame with all the events (SN)
    def SNList(self):
        return self.__SNList
    
    # Remove the noise characters from the events / SN
    def removeNoise(self, _str, _noise = True, _multiplespaces = True):
        # remove noise (punctuation) if asked (by default yes)
        if _noise:
            for car in list(C.NOISE_CHARACTERS):
                _str = _str.replace(car, "")
        # replace multiple spaces by one in string if requested (default yes)
        if _multiplespaces:
            _str = re.sub("\s+", " ", _str).strip()
        return _str.strip().capitalize()
    
    def Cleanse(self):
        # remove noise
        self.SNList[C.FLD_NEW_SN] = self.SNList[C.FLD_COL_VALUECOUNT].apply(self.removeNoise)
        return

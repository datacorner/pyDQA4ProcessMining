__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import constants as C
from chart import Chart

# This class manages the charts generation by using matplotlib (from the data to a file)
class MatplotlibChart(Chart):
    
    # Create a LINE chart by using the DataFramce and the 2 columns (X& Y) in parameter.        
    def CreateLine(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        try: 
            plt.grid(color='#F2F2F2', alpha=1, zorder=0)
            plt.plot(p_data[p_colX], p_data[p_colY], color=p_color, lw=3, zorder=5)
            self.addAxisInfos(p_colX, p_colY, p_labelX, p_labelY)
            plt.savefig(p_filename, dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
            return p_filename
        except:
            return C.NO_FILE_CREATED
        
    # Create a HORIZONTAL BAR chart by using the DataFramce and the 2 columns (X& Y) in parameter.
    def CreateBarH(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        #nbY = _data[_colX].shape[0] # Nb of H bars
        try: 
            plt.barh(p_data[p_colX], p_data[p_colY], color = p_color)
            self.addlabels(p_data[p_colY])
            self.addAxisInfos(p_colX, p_colY, p_labelY, p_labelX)
            plt.savefig(p_filename, dpi=300)
            plt.close()
            return p_filename
        except:
            return C.NO_FILE_CREATED
        
    # Create a VERTICAL BAR chart by using the DataFramce and the 2 columns (X& Y) in parameter.
    def CreateBarV(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        try:
            plt.barh(p_data[p_colX], p_data[p_colY], color = p_color)
            self.addAxisInfos(p_colX, p_colY, p_labelX, p_labelY)
            plt.savefig(p_filename, dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
            return p_filename
        except:
            return C.NO_FILE_CREATED
__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import constants as C

# This class manages the charts generation (from the data to a file)
class Chart:
    def __init__(self, p_widthInch = 12, p_heightInch = 4):
        rcParams['axes.spines.top'] = False
        rcParams['axes.spines.right'] = False
        rcParams["figure.autolayout"] = True
        rcParams["axes.labelpad"] = 4.0
        self.setFigureSize(p_widthInch, p_heightInch)
        return
        
    # Add axis informations
    def addAxisInfos(self, p_colX, p_colY, p_labelX, p_labelY):
        labelX = p_colX if p_labelX==None else p_labelX
        labelY = p_colY if p_labelY==None else p_labelY
        plt.xlabel(labelX, fontsize=13)
        plt.xticks(fontsize=9)
        plt.ylabel(labelY, fontsize=13)
        plt.yticks(fontsize=9)
        plt.xticks(rotation=45)

    # Add the labels for all the values in the chart
    def addlabels(self, p_y):
        for i, v in enumerate(p_y):
            plt.text(v + 3, i + .25, str(v), color='black')

    # Specify the size of the global chart
    def setFigureSize(self, p_widthInch, p_heightInch):
        self.m_widthInch = p_widthInch
        self.m_heightInch = p_heightInch
        plt.figure(figsize=(p_widthInch, p_heightInch)) # Width, height in inches

    # Create a LINE chart by using the DataFramce and the 2 columns (X& Y) in parameter.        
    def CreateLine(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        return C.NO_FILE_CREATED
        
    # Create a HORIZONTAL BAR chart by using the DataFramce and the 2 columns (X& Y) in parameter.
    def CreateBarH(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        return C.NO_FILE_CREATED
        
    # Create a VERTICAL BAR chart by using the DataFramce and the 2 columns (X& Y) in parameter.
    def CreateBarV(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        return C.NO_FILE_CREATED
    
    # Create a table with only the <p_maxColDisplay> first columns
    # If the number of columns is > p_maxColDisplay, then split the table and create several
    # tables (each table with p_maxColDisplay columns max)
    def CreateTable(self, p_filename, p_data, p_maxColDisplay = 5 ):
        #only display the first 5 columns
        try:
            # Display Maximum x columns per sub-tables
            maxColView = p_maxColDisplay
            if (len(p_data.columns)<maxColView):
                maxColView = len(p_data.columns)
            nbIter = int(len(p_data.columns) / p_maxColDisplay) + (1 if int(len(p_data.columns) % p_maxColDisplay) > 0 else 0)
            idx = 0

            if (nbIter == 1):
                # Need only to display one table
                table = np.asarray(p_data)
                fig = plt.figure(figsize=(self.m_widthInch, self.m_heightInch))
                ax = plt.Axes(fig, [0., 0., 1., 1.])
                ax.set_axis_off()
                fig.add_axes(ax)
                plt.table(cellText=table, colLabels=p_data.columns, cellLoc='center', loc='center')
                fig.set_tight_layout(False)
            else:
                # create the sub tables. Create one new table per p_maxColDisplay iteration:
                fig, axTables = plt.subplots(nrows=nbIter, ncols=1, figsize=(self.m_widthInch, self.m_heightInch*nbIter*2))
                for i in range(nbIter):
                    _mydata = p_data[ p_data.columns[idx:idx+p_maxColDisplay] ]
                    header = _mydata.columns
                    table = np.asarray(_mydata)
                    axTables[i].axis('tight')
                    axTables[i].axis('off')
                    axTables[i].table(cellText=table, colLabels=header, cellLoc='center', loc='center', colColours=["palegreen"] * 10)
                    fig.set_tight_layout(False)
                    idx += p_maxColDisplay

            plt.savefig(p_filename, dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
            return p_filename
        except Exception as e:
            return C.NO_FILE_CREATED
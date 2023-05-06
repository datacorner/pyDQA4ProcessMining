__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import constants as C
from chart import Chart
import seaborn as sns
import pandas as pd 

# This class manages the charts generation by using matplotlib (from the data to a file)
class SeabornChart(Chart):
    # Show the labels in the chart
    def show_values(self, axs, orient="v", space=.01):
        def _single(ax):
            if orient == "v":
                for p in ax.patches:
                    _x = p.get_x() + p.get_width() / 2
                    _y = p.get_y() + p.get_height() + (p.get_height()*0.01)
                    value = '{:.0f}'.format(p.get_height())
                    ax.text(_x, _y, value, ha="center") 
            elif orient == "h":
                for p in ax.patches:
                    _x = p.get_x() + p.get_width() + float(space)
                    _y = p.get_y() + p.get_height() - (p.get_height()*0.5)
                    value = '{:.0f}'.format(p.get_width())
                    ax.text(_x, _y, value, ha="left")

        if isinstance(axs, np.ndarray):
            for idx, ax in np.ndenumerate(axs):
                _single(ax)
        else:
            _single(axs)

    # Create a HORIZONTAL BAR chart by using the DataFramce and the 2 columns (X& Y) in parameter.
    def CreateBarH(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        try: 
            ax = sns.barplot(x=p_data[p_colY], y=p_data[p_colX], orient='h', order=p_data[p_colX])
            self.show_values(ax, "h")
            self.addAxisInfos(p_colX, p_colY, p_labelY, p_labelX)
            plt.savefig(p_filename)
            return p_filename
        except Exception as e:
            return C.NO_FILE_CREATED
        
    # Create a VERTICAL BAR chart by using the DataFramce and the 2 columns (X& Y) in parameter.
    def CreateBarV(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        try: 
            ax = sns.barplot(x=p_data[p_colX], y=p_data[p_colY], orient='v', order=p_data[p_colX])
            self.show_values(ax, "v")
            self.addAxisInfos(p_colX, p_colY, p_labelX, p_labelY)
            plt.savefig(p_filename)
            return p_filename
        except Exception as e:
            return C.NO_FILE_CREATED
        
    def CreateLine(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        try: 
            ax = sns.lineplot(p_data, x=p_colX, y=p_colY, sort=True)
            self.addAxisInfos(p_colX, p_colY, p_labelX, p_labelY)
            plt.savefig(p_filename)
            return p_filename
        except Exception as e:
            return C.NO_FILE_CREATED

    def CreateScatter(self, p_filename, p_data, p_colX, p_colY, p_labelX=None, p_labelY=None, p_color ='#087E8B'):
        try: 
            ax = sns.scatterplot(data=p_data, x=p_colX, y=p_colY)
            self.addAxisInfos(p_colX, p_colY, p_labelX, p_labelY)
            plt.savefig(p_filename)
            return p_filename
        except Exception as e:
            return C.NO_FILE_CREATED
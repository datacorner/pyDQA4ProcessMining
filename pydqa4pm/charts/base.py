"""
Base chart class for pyDQA4ProcessMining.

Provides the base Chart class with common functionality and table generation.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from typing import Optional

import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd

from pydqa4pm.utils import constants as C


class Chart:
    """
    Base class for chart generation.
    
    Provides common chart functionality and table generation capabilities.
    Subclasses (SeabornChart, MatplotlibChart) implement specific chart types.
    
    Attributes:
        m_widthInch: Chart width in inches.
        m_heightInch: Chart height in inches.
    
    Example:
        >>> chart = Chart(10, 4)
        >>> chart.CreateTable("output.jpg", dataframe)
    """
    
    def __init__(self, width_inch: float = 12, height_inch: float = 4):
        """
        Initialize the chart with given dimensions.
        
        Args:
            width_inch: Width in inches.
            height_inch: Height in inches.
        """
        rcParams['axes.spines.top'] = False
        rcParams['axes.spines.right'] = False
        rcParams["figure.autolayout"] = True
        rcParams["axes.labelpad"] = 4.0
        self.set_figure_size(width_inch, height_inch)
    
    def set_figure_size(self, width_inch: float, height_inch: float) -> None:
        """Set the figure size for charts."""
        self.m_widthInch = width_inch
        self.m_heightInch = height_inch
        plt.figure(figsize=(width_inch, height_inch))
    
    # Backward compatibility alias
    def setFigureSize(self, p_widthInch, p_heightInch):
        self.set_figure_size(p_widthInch, p_heightInch)

    def add_axis_info(self, col_x: str, col_y: str, 
                      label_x: Optional[str] = None, 
                      label_y: Optional[str] = None) -> None:
        """Add axis labels and formatting to the chart."""
        x_label = col_x if label_x is None else label_x
        y_label = col_y if label_y is None else label_y
        
        plt.xlabel(x_label, fontsize=13)
        plt.xticks(fontsize=9)
        plt.ylabel(y_label, fontsize=13)
        plt.yticks(fontsize=9)
        plt.xticks(rotation=45)
    
    # Backward compatibility alias
    def addAxisInfos(self, p_colX, p_colY, p_labelX, p_labelY):
        self.add_axis_info(p_colX, p_colY, p_labelX, p_labelY)

    def add_labels(self, y_values) -> None:
        """Add value labels to horizontal bar chart."""
        for i, v in enumerate(y_values):
            plt.text(v + 3, i + 0.25, str(v), color='black')
    
    # Backward compatibility alias
    def addlabels(self, p_y):
        self.add_labels(p_y)

    def CreateLine(self, filename: str, data: pd.DataFrame, 
                   col_x: str, col_y: str,
                   label_x: Optional[str] = None, 
                   label_y: Optional[str] = None,
                   color: str = '#087E8B') -> str:
        """Create a line chart. Override in subclasses."""
        return C.NO_FILE_CREATED
    
    def CreateBarH(self, filename: str, data: pd.DataFrame,
                   col_x: str, col_y: str,
                   label_x: Optional[str] = None,
                   label_y: Optional[str] = None,
                   color: str = '#087E8B') -> str:
        """Create a horizontal bar chart. Override in subclasses."""
        return C.NO_FILE_CREATED
    
    def CreateBarV(self, filename: str, data: pd.DataFrame,
                   col_x: str, col_y: str,
                   label_x: Optional[str] = None,
                   label_y: Optional[str] = None,
                   color: str = '#087E8B') -> str:
        """Create a vertical bar chart. Override in subclasses."""
        return C.NO_FILE_CREATED

    def CreateTable(self, filename: str, data: pd.DataFrame, 
                    max_cols_per_view: int = 5) -> str:
        """
        Create a table image from a DataFrame.
        
        If the DataFrame has more columns than max_cols_per_view,
        it will be split into multiple sub-tables.
        
        Args:
            filename: Output file path.
            data: DataFrame to display.
            max_cols_per_view: Maximum columns per sub-table.
        
        Returns:
            The filename if successful, NO_FILE_CREATED otherwise.
        """
        try:
            num_cols = len(data.columns)
            cols_to_show = min(max_cols_per_view, num_cols)
            num_tables = (num_cols + max_cols_per_view - 1) // max_cols_per_view

            if num_tables == 1:
                # Single table
                table_data = np.asarray(data)
                fig = plt.figure(figsize=(self.m_widthInch, self.m_heightInch))
                ax = plt.Axes(fig, [0., 0., 1., 1.])
                ax.set_axis_off()
                fig.add_axes(ax)
                plt.table(
                    cellText=table_data,
                    colLabels=data.columns,
                    cellLoc='center',
                    loc='center'
                )
                fig.set_tight_layout(False)
            else:
                # Multiple sub-tables
                fig, axes = plt.subplots(
                    nrows=num_tables,
                    ncols=1,
                    figsize=(self.m_widthInch, self.m_heightInch * num_tables * 2)
                )
                
                idx = 0
                for i in range(num_tables):
                    subset = data[data.columns[idx:idx + max_cols_per_view]]
                    table_data = np.asarray(subset)
                    
                    axes[i].axis('tight')
                    axes[i].axis('off')
                    axes[i].table(
                        cellText=table_data,
                        colLabels=subset.columns,
                        cellLoc='center',
                        loc='center',
                        colColours=["palegreen"] * len(subset.columns)
                    )
                    
                    idx += max_cols_per_view
                
                fig.set_tight_layout(False)

            plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
            return filename
            
        except Exception as e:
            return C.NO_FILE_CREATED


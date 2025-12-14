"""
Matplotlib-based chart implementations for pyDQA4ProcessMining.

Provides basic visualizations using pure Matplotlib.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from pydqa4pm.charts.base import Chart
from pydqa4pm.utils import constants as C


class MatplotlibChart(Chart):
    """
    Pure Matplotlib chart generator.
    
    Provides bar charts and line charts using Matplotlib without Seaborn.
    
    Example:
        >>> chart = MatplotlibChart(10, 6)
        >>> chart.CreateLine("output.png", df, "X", "Y")
    """

    def CreateLine(self, filename: str, data: pd.DataFrame,
                   col_x: str, col_y: str,
                   label_x: Optional[str] = None,
                   label_y: Optional[str] = None,
                   color: str = '#087E8B') -> str:
        """
        Create a line chart.
        
        Args:
            filename: Output file path.
            data: DataFrame with the data.
            col_x: Column name for x-axis.
            col_y: Column name for y-axis.
            label_x: Optional x-axis label.
            label_y: Optional y-axis label.
            color: Line color.
        
        Returns:
            Filename if successful, NO_FILE_CREATED otherwise.
        """
        try:
            plt.figure(figsize=(self.m_widthInch, self.m_heightInch))
            plt.grid(color='#F2F2F2', alpha=1, zorder=0)
            plt.plot(data[col_x], data[col_y], color=color, lw=3, zorder=5)
            self.add_axis_info(col_x, col_y, label_x, label_y)
            plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
            return filename
        except Exception:
            plt.close()
            return C.NO_FILE_CREATED

    def CreateBarH(self, filename: str, data: pd.DataFrame,
                   col_x: str, col_y: str,
                   label_x: Optional[str] = None,
                   label_y: Optional[str] = None,
                   color: str = '#087E8B') -> str:
        """
        Create a horizontal bar chart.
        
        Args:
            filename: Output file path.
            data: DataFrame with the data.
            col_x: Column name for categories.
            col_y: Column name for values.
            label_x: Optional x-axis label.
            label_y: Optional y-axis label.
            color: Bar color.
        
        Returns:
            Filename if successful, NO_FILE_CREATED otherwise.
        """
        try:
            plt.figure(figsize=(self.m_widthInch, self.m_heightInch))
            plt.barh(data[col_x], data[col_y], color=color)
            self.add_labels(data[col_y])
            self.add_axis_info(col_x, col_y, label_y, label_x)
            plt.savefig(filename, dpi=300)
            plt.close()
            return filename
        except Exception:
            plt.close()
            return C.NO_FILE_CREATED

    def CreateBarV(self, filename: str, data: pd.DataFrame,
                   col_x: str, col_y: str,
                   label_x: Optional[str] = None,
                   label_y: Optional[str] = None,
                   color: str = '#087E8B') -> str:
        """
        Create a vertical bar chart.
        
        Args:
            filename: Output file path.
            data: DataFrame with the data.
            col_x: Column name for categories.
            col_y: Column name for values.
            label_x: Optional x-axis label.
            label_y: Optional y-axis label.
            color: Bar color.
        
        Returns:
            Filename if successful, NO_FILE_CREATED otherwise.
        """
        try:
            plt.figure(figsize=(self.m_widthInch, self.m_heightInch))
            plt.bar(data[col_x], data[col_y], color=color)
            self.add_axis_info(col_x, col_y, label_x, label_y)
            plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
            return filename
        except Exception:
            plt.close()
            return C.NO_FILE_CREATED


"""
Seaborn-based chart implementations for pyDQA4ProcessMining.

Provides statistical visualizations using the Seaborn library.
"""

__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "GPL"

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from pydqa4pm.charts.base import Chart
from pydqa4pm.utils import constants as C


class SeabornChart(Chart):
    """
    Seaborn-based chart generator.
    
    Provides bar charts, line charts, and scatter plots using Seaborn.
    
    Example:
        >>> chart = SeabornChart(10, 6)
        >>> chart.CreateBarH("output.png", df, "Category", "Value")
    """
    
    def _show_values(self, axes, orient: str = "v", space: float = 0.01) -> None:
        """
        Add value labels to bar chart patches.
        
        Args:
            axes: Matplotlib axes or array of axes.
            orient: Orientation - "v" for vertical, "h" for horizontal.
            space: Spacing factor for label positioning.
        """
        def _single(ax):
            if orient == "v":
                for patch in ax.patches:
                    x = patch.get_x() + patch.get_width() / 2
                    y = patch.get_y() + patch.get_height() + (patch.get_height() * 0.01)
                    value = '{:.0f}'.format(patch.get_height())
                    ax.text(x, y, value, ha="center")
            elif orient == "h":
                for patch in ax.patches:
                    x = patch.get_x() + patch.get_width() + float(space)
                    y = patch.get_y() + patch.get_height() - (patch.get_height() * 0.5)
                    value = '{:.0f}'.format(patch.get_width())
                    ax.text(x, y, value, ha="left")

        if isinstance(axes, np.ndarray):
            for idx, ax in np.ndenumerate(axes):
                _single(ax)
        else:
            _single(axes)
    
    # Backward compatibility alias
    def show_values(self, axs, orient="v", space=.01):
        self._show_values(axs, orient, space)

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
            col_x: Column name for categories (y-axis in horizontal bar).
            col_y: Column name for values (x-axis in horizontal bar).
            label_x: Optional x-axis label.
            label_y: Optional y-axis label.
            color: Bar color (default: teal).
        
        Returns:
            Filename if successful, NO_FILE_CREATED otherwise.
        """
        try:
            plt.figure(figsize=(self.m_widthInch, self.m_heightInch))
            ax = sns.barplot(
                x=data[col_y],
                y=data[col_x],
                orient='h',
                order=data[col_x]
            )
            self._show_values(ax, "h")
            self.add_axis_info(col_x, col_y, label_y, label_x)
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
            return filename
        except Exception as e:
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
            col_x: Column name for categories (x-axis).
            col_y: Column name for values (y-axis).
            label_x: Optional x-axis label.
            label_y: Optional y-axis label.
            color: Bar color.
        
        Returns:
            Filename if successful, NO_FILE_CREATED otherwise.
        """
        try:
            plt.figure(figsize=(self.m_widthInch, self.m_heightInch))
            ax = sns.barplot(
                x=data[col_x],
                y=data[col_y],
                orient='v',
                order=data[col_x]
            )
            self._show_values(ax, "v")
            self.add_axis_info(col_x, col_y, label_x, label_y)
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
            return filename
        except Exception as e:
            plt.close()
            return C.NO_FILE_CREATED

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
            ax = sns.lineplot(data=data, x=col_x, y=col_y, sort=True)
            self.add_axis_info(col_x, col_y, label_x, label_y)
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
            return filename
        except Exception as e:
            plt.close()
            return C.NO_FILE_CREATED

    def CreateScatter(self, filename: str, data: pd.DataFrame,
                      col_x: str, col_y: str,
                      label_x: Optional[str] = None,
                      label_y: Optional[str] = None,
                      color: str = '#087E8B') -> str:
        """
        Create a scatter plot.
        
        Args:
            filename: Output file path.
            data: DataFrame with the data.
            col_x: Column name for x-axis.
            col_y: Column name for y-axis.
            label_x: Optional x-axis label.
            label_y: Optional y-axis label.
            color: Point color.
        
        Returns:
            Filename if successful, NO_FILE_CREATED otherwise.
        """
        try:
            plt.figure(figsize=(self.m_widthInch, self.m_heightInch))
            ax = sns.scatterplot(data=data, x=col_x, y=col_y)
            self.add_axis_info(col_x, col_y, label_x, label_y)
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
            return filename
        except Exception as e:
            plt.close()
            return C.NO_FILE_CREATED


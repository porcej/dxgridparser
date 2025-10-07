"""
dxgridparser - A Python library to parse DevExpress ASPxGridView tables from BeautifulSoup objects
"""

from .parser import ASPxGridView, find_all_grids

__version__ = "0.1.0"
__all__ = ["ASPxGridView", "find_all_grids"]


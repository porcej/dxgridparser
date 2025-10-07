"""
Parser module for DevExpress ASPxGridView tables
"""

from typing import List, Dict, Any, Optional, Union
import pandas as pd
from bs4 import BeautifulSoup, Tag


class ASPxGridView:
    """
    A class to represent a parsed DevExpress ASPxGridView table.
    
    Attributes:
        data (List[Dict[str, Any]]): The table data as a list of dictionaries
        headers (List[str]): The column headers
        metadata (Dict[str, Any]): Additional metadata about the table
    """
    
    def __init__(self, soup_element: Tag):
        """
        Initialize ASPxGridView from a BeautifulSoup Tag element.
        
        Args:
            soup_element: A BeautifulSoup Tag representing the ASPxGridView table
        """
        self.soup_element = soup_element
        self.headers: List[str] = []
        self.data: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}
        
        # Parse the table
        self._parse()
    
    def _parse(self):
        """Parse the ASPxGridView table structure."""
        # Extract metadata
        self._extract_metadata()
        
        # Find the main table element
        table = self._find_main_table()
        
        if table:
            # Extract headers
            self.headers = self._extract_headers(table)
            
            # Extract data rows
            self.data = self._extract_data(table)
    
    def _extract_metadata(self):
        """Extract metadata from the grid element."""
        # Store the grid ID if available
        if self.soup_element.get('id'):
            self.metadata['grid_id'] = self.soup_element.get('id')
        
        # Store CSS classes
        if self.soup_element.get('class'):
            self.metadata['classes'] = self.soup_element.get('class')
        
        # Store any data attributes
        for attr, value in self.soup_element.attrs.items():
            if attr.startswith('data-'):
                self.metadata[attr] = value
    
    def _find_main_table(self) -> Optional[Tag]:
        """
        Find the main table element within the ASPxGridView.
        
        Returns:
            The main table Tag or None if not found
        """
        # ASPxGridView typically uses table elements
        # Look for table with specific classes or within the grid div
        table = self.soup_element.find('table')
        
        if not table and self.soup_element.name == 'table':
            table = self.soup_element
        
        return table
    
    def _extract_headers(self, table: Tag) -> List[str]:
        """
        Extract column headers from the table.
        
        Args:
            table: The table Tag element
            
        Returns:
            List of header names
        """
        headers = []
        
        # Look for thead section
        thead = table.find('thead')
        if thead:
            header_row = thead.find('tr')
            if header_row:
                headers = self._extract_header_cells(header_row)
        
        # If no thead, look for the first row with th elements
        if not headers:
            first_row = table.find('tr')
            if first_row:
                th_cells = first_row.find_all('th')
                if th_cells:
                    headers = self._extract_header_cells(first_row)
        
        # If still no headers, look for rows with specific ASPxGridView header classes
        if not headers:
            header_row = table.find('tr', class_=lambda x: x and any(
                cls in str(x).lower() for cls in ['header', 'dxgvheader', 'gridheader']
            ))
            if header_row:
                headers = self._extract_header_cells(header_row)
        
        return headers
    
    def _extract_header_cells(self, row: Tag) -> List[str]:
        """
        Extract text from header cells in a row.
        
        Args:
            row: The header row Tag
            
        Returns:
            List of header text values
        """
        headers = []
        
        # Try th elements first
        cells = row.find_all('th')
        
        # Fall back to td if no th elements
        if not cells:
            cells = row.find_all('td')
        
        for cell in cells:
            # Get text content, strip whitespace
            text = cell.get_text(strip=True)
            
            # Handle empty headers
            if not text:
                text = f"Column_{len(headers)}"
            
            headers.append(text)
        
        return headers
    
    def _extract_data(self, table: Tag) -> List[Dict[str, Any]]:
        """
        Extract data rows from the table.
        
        Args:
            table: The table Tag element
            
        Returns:
            List of dictionaries representing rows
        """
        data = []
        
        # Find tbody or use the table directly
        tbody = table.find('tbody')
        rows_container = tbody if tbody else table
        
        # Get all rows
        all_rows = rows_container.find_all('tr', recursive=False)
        
        # Filter out header rows
        data_rows = self._filter_data_rows(all_rows)
        
        for row in data_rows:
            row_data = self._extract_row_data(row)
            if row_data:
                data.append(row_data)
        
        return data
    
    def _filter_data_rows(self, rows: List[Tag]) -> List[Tag]:
        """
        Filter out header rows and keep only data rows.
        
        Args:
            rows: List of row Tags
            
        Returns:
            List of data row Tags
        """
        data_rows = []
        
        for row in rows:
            # Skip rows that are likely headers
            classes = row.get('class', [])
            class_str = ' '.join(classes).lower() if classes else ''
            
            # Skip header rows
            if any(cls in class_str for cls in ['header', 'dxgvheader']):
                continue
            
            # Skip rows with only th elements
            if row.find_all('th') and not row.find_all('td'):
                continue
            
            # Skip empty rows
            if not row.find_all(['td', 'th']):
                continue
            
            data_rows.append(row)
        
        return data_rows
    
    def _extract_row_data(self, row: Tag) -> Optional[Dict[str, Any]]:
        """
        Extract data from a single row.
        
        Args:
            row: The row Tag element
            
        Returns:
            Dictionary mapping headers to cell values
        """
        cells = row.find_all('td')
        
        if not cells:
            return None
        
        row_data = {}
        
        for i, cell in enumerate(cells):
            # Get the header name for this column
            header = self.headers[i] if i < len(self.headers) else f"Column_{i}"
            
            # Extract cell value
            value = self._extract_cell_value(cell)
            
            row_data[header] = value
        
        return row_data
    
    def _extract_cell_value(self, cell: Tag) -> Any:
        """
        Extract the value from a table cell.
        
        Args:
            cell: The cell Tag element
            
        Returns:
            The cell value (attempts to parse numbers, otherwise returns string)
        """
        # Check for input elements (for editable grids)
        input_elem = cell.find('input')
        if input_elem and input_elem.get('value'):
            return input_elem.get('value')
        
        # Check for select elements
        select_elem = cell.find('select')
        if select_elem:
            selected = select_elem.find('option', selected=True)
            if selected:
                return selected.get_text(strip=True)
        
        # Get text content
        text = cell.get_text(strip=True)
        
        # Try to convert to number
        if text:
            # Try integer
            try:
                return int(text.replace(',', ''))
            except ValueError:
                pass
            
            # Try float
            try:
                return float(text.replace(',', ''))
            except ValueError:
                pass
        
        return text
    
    def to_dicts(self) -> List[Dict[str, Any]]:
        """
        Convert the table data to a list of dictionaries.
        
        Returns:
            List of dictionaries, where each dict represents a row
        """
        return self.data.copy()
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert the table data to a pandas DataFrame.
        
        Returns:
            A pandas DataFrame containing the table data
        """
        if not self.data:
            # Return empty DataFrame with headers if available
            return pd.DataFrame(columns=self.headers)
        
        return pd.DataFrame(self.data)
    
    def __repr__(self) -> str:
        """String representation of the ASPxGridView."""
        return f"ASPxGridView(rows={len(self.data)}, columns={len(self.headers)})"
    
    def __str__(self) -> str:
        """String representation of the ASPxGridView."""
        return f"ASPxGridView with {len(self.data)} rows and {len(self.headers)} columns"


def find_all_grids(soup: Union[BeautifulSoup, Tag]) -> List[ASPxGridView]:
    """
    Find all DevExpress ASPxGridView tables in a BeautifulSoup object.
    
    This function searches for common patterns used by ASPxGridView:
    - Elements with class containing 'dxgv' (DevExpress GridView)
    - Elements with class containing 'aspxgridview'
    - Tables with specific DevExpress attributes
    
    Args:
        soup: A BeautifulSoup object or Tag to search within
        
    Returns:
        List of ASPxGridView objects
    """
    grids = []
    
    # Search for elements with DevExpress GridView classes
    # Common patterns: dxgvControl, dxgvTable, ASPxGridView, etc.
    grid_elements = []
    
    # Pattern 1: Class contains 'dxgv'
    grid_elements.extend(soup.find_all(class_=lambda x: x and 'dxgv' in str(x).lower()))
    
    # Pattern 2: Class contains 'aspxgridview'
    grid_elements.extend(soup.find_all(class_=lambda x: x and 'aspxgridview' in str(x).lower()))
    
    # Pattern 3: Tables with specific data attributes
    grid_elements.extend(soup.find_all('table', attrs=lambda x: isinstance(x, dict) and any(
        key.startswith('data-') for key in x.keys()
    )))
    
    # Pattern 4: Divs with ID containing 'grid' or 'GridView'
    grid_elements.extend(soup.find_all(id=lambda x: x and ('grid' in str(x).lower() or 'gridview' in str(x).lower())))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_elements = []
    for elem in grid_elements:
        elem_id = id(elem)
        if elem_id not in seen:
            seen.add(elem_id)
            unique_elements.append(elem)
    
    # Create ASPxGridView objects
    for element in unique_elements:
        try:
            grid = ASPxGridView(element)
            # Only include grids that have data or headers
            if grid.data or grid.headers:
                grids.append(grid)
        except Exception as e:
            # Skip elements that can't be parsed
            continue
    
    return grids


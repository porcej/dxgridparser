# dxgridparser

A Python library for parsing DevExpress ASPxGridView tables from BeautifulSoup objects into structured Python objects, lists, and pandas DataFrames.

## Features

- 🔍 Automatically find all ASPxGridView tables in a BeautifulSoup object
- 📊 Parse table data with headers and metadata
- 🐼 Export to pandas DataFrame with `.to_dataframe()`
- 📝 Export to list of dictionaries with `.to_dicts()`
- 🎯 Handle various ASPxGridView rendering patterns
- 🛡️ Robust parsing with error handling

## Installation

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

## Quick Start

```python
from bs4 import BeautifulSoup
import dxgridparser

# Load your HTML content
html = """
<div class="dxgvControl">
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Age</th>
                <th>City</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>John Doe</td>
                <td>30</td>
                <td>New York</td>
            </tr>
            <tr>
                <td>Jane Smith</td>
                <td>25</td>
                <td>Los Angeles</td>
            </tr>
        </tbody>
    </table>
</div>
"""

# Parse with BeautifulSoup
soup = BeautifulSoup(html, 'lxml')

# Find all ASPxGridView tables
grids = dxgridparser.find_all_grids(soup)

print(f"Found {len(grids)} grid(s)")

# Work with the first grid
if grids:
    grid = grids[0]
    
    # Get as list of dictionaries
    data = grid.to_dicts()
    print(data)
    # [
    #     {'Name': 'John Doe', 'Age': 30, 'City': 'New York'},
    #     {'Name': 'Jane Smith', 'Age': 25, 'City': 'Los Angeles'}
    # ]
    
    # Get as pandas DataFrame
    df = grid.to_dataframe()
    print(df)
    #          Name  Age         City
    # 0    John Doe   30     New York
    # 1  Jane Smith   25  Los Angeles
    
    # Access metadata
    print(grid.metadata)
    # {'classes': ['dxgvControl']}
    
    # Access headers
    print(grid.headers)
    # ['Name', 'Age', 'City']
```

## Usage Examples

### Example 1: Parse a Single Grid

```python
from bs4 import BeautifulSoup
from dxgridparser import ASPxGridView

html = "<table class='dxgvTable'>...</table>"
soup = BeautifulSoup(html, 'lxml')

# Parse a specific grid element
grid_element = soup.find('table', class_='dxgvTable')
grid = ASPxGridView(grid_element)

# Convert to dictionary list
records = grid.to_dicts()

# Convert to DataFrame
df = grid.to_dataframe()
```

### Example 2: Find All Grids on a Page

```python
from bs4 import BeautifulSoup
from dxgridparser import find_all_grids

# Load HTML from file
with open('page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')

# Find all grids
grids = find_all_grids(soup)

# Process each grid
for i, grid in enumerate(grids):
    print(f"Grid {i + 1}:")
    print(f"  Rows: {len(grid.data)}")
    print(f"  Columns: {len(grid.headers)}")
    print(f"  Headers: {grid.headers}")
    
    # Export to CSV using pandas
    df = grid.to_dataframe()
    df.to_csv(f'grid_{i + 1}.csv', index=False)
```

### Example 3: Working with Grid Metadata

```python
from dxgridparser import find_all_grids

grids = find_all_grids(soup)

for grid in grids:
    # Access grid ID
    grid_id = grid.metadata.get('grid_id', 'Unknown')
    print(f"Processing grid: {grid_id}")
    
    # Access CSS classes
    classes = grid.metadata.get('classes', [])
    print(f"CSS classes: {classes}")
    
    # Access data attributes
    for key, value in grid.metadata.items():
        if key.startswith('data-'):
            print(f"{key}: {value}")
```

### Example 4: Data Analysis with Pandas

```python
from dxgridparser import find_all_grids
import pandas as pd

grids = find_all_grids(soup)

if grids:
    grid = grids[0]
    df = grid.to_dataframe()
    
    # Perform pandas operations
    print(df.describe())
    print(df.head())
    
    # Filter data
    filtered = df[df['Age'] > 25]
    
    # Group by
    grouped = df.groupby('City').mean()
    
    # Save to Excel
    df.to_excel('grid_data.xlsx', index=False)
```

## API Reference

### `ASPxGridView`

The main class representing a parsed ASPxGridView table.

**Attributes:**
- `headers` (List[str]): Column headers
- `data` (List[Dict[str, Any]]): Table data as list of dictionaries
- `metadata` (Dict[str, Any]): Grid metadata (ID, classes, data attributes)
- `soup_element` (Tag): Original BeautifulSoup element

**Methods:**

#### `to_dicts() -> List[Dict[str, Any]]`
Returns the table data as a list of dictionaries.

```python
data = grid.to_dicts()
# [{'col1': 'value1', 'col2': 'value2'}, ...]
```

#### `to_dataframe() -> pd.DataFrame`
Returns the table data as a pandas DataFrame.

```python
df = grid.to_dataframe()
```

### `find_all_grids(soup) -> List[ASPxGridView]`

Find all ASPxGridView tables in a BeautifulSoup object.

**Parameters:**
- `soup` (BeautifulSoup | Tag): BeautifulSoup object or Tag to search

**Returns:**
- List[ASPxGridView]: List of parsed grid objects

**Example:**
```python
grids = find_all_grids(soup)
```

## Supported DevExpress Patterns

The library automatically detects ASPxGridView tables using multiple patterns:

- Elements with class containing `dxgv` (e.g., `dxgvControl`, `dxgvTable`)
- Elements with class containing `aspxgridview`
- Tables with DevExpress data attributes
- Elements with IDs containing `grid` or `GridView`

## Requirements

- Python >= 3.7
- beautifulsoup4 >= 4.9.0
- pandas >= 1.0.0
- lxml >= 4.6.0 (recommended parser)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 0.1.0
- Initial release
- Basic ASPxGridView parsing
- Support for `to_dicts()` and `to_dataframe()`
- Automatic grid detection with `find_all_grids()`

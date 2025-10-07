# Quick Usage Guide

## Installation

```bash
# Activate your virtual environment
workon scraper  # or source /Users/porcej/.venv/scraper/bin/activate

# Install the package in development mode
cd /Users/porcej/dev/scraper/dxgridparser
pip install -e .

# Install lxml parser (recommended)
pip install lxml
```

## Basic Usage

### Import the library

```python
from bs4 import BeautifulSoup
import dxgridparser
```

### Parse HTML and find all grids

```python
# Load your HTML
html = open('page.html').read()
soup = BeautifulSoup(html, 'lxml')

# Find all ASPxGridView tables
grids = dxgridparser.find_all_grids(soup)

print(f"Found {len(grids)} grid(s)")
```

### Work with individual grids

```python
for grid in grids:
    # Get grid information
    print(f"Grid ID: {grid.metadata.get('grid_id', 'N/A')}")
    print(f"Headers: {grid.headers}")
    print(f"Rows: {len(grid.data)}")
    
    # Export to list of dictionaries
    data = grid.to_dicts()
    
    # Export to pandas DataFrame
    df = grid.to_dataframe()
    
    # Save to CSV
    df.to_csv('output.csv', index=False)
```

### Parse a specific grid element

```python
# If you already have a specific grid element
grid_element = soup.find('div', id='MyGrid')
grid = dxgridparser.ASPxGridView(grid_element)

# Access the data
print(grid.to_dicts())
```

## Supported DevExpress Patterns

The library automatically detects:
- Elements with class `dxgv*` (e.g., `dxgvControl`, `dxgvTable`)
- Elements with class `aspxgridview`
- Elements with IDs containing `grid` or `GridView`
- Tables with data attributes

## Data Types

The parser automatically converts:
- Integer strings → `int`
- Float strings → `float`
- Everything else → `str`

## Examples

Run the example script:
```bash
python examples/example_usage.py
```

Run tests:
```bash
python -m unittest tests/test_parser.py -v
```

## Common Patterns

### Export all grids to separate CSV files
```python
grids = dxgridparser.find_all_grids(soup)
for i, grid in enumerate(grids):
    df = grid.to_dataframe()
    df.to_csv(f'grid_{i+1}.csv', index=False)
```

### Combine multiple grids into one DataFrame
```python
import pandas as pd

grids = dxgridparser.find_all_grids(soup)
all_data = []
for grid in grids:
    all_data.extend(grid.to_dicts())

combined_df = pd.DataFrame(all_data)
```

### Filter and analyze grid data
```python
grid = grids[0]
df = grid.to_dataframe()

# Filter
filtered = df[df['Price'] > 100]

# Group by
grouped = df.groupby('Category').mean()

# Statistics
print(df.describe())
```


"""
Example usage of the dxgridparser library
"""

from bs4 import BeautifulSoup
import sys
import os

# Add parent directory to path to import dxgridparser
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dxgridparser


def example1_basic_usage():
    """Example 1: Basic usage with a simple grid"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
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
                <tr>
                    <td>Bob Johnson</td>
                    <td>35</td>
                    <td>Chicago</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    
    soup = BeautifulSoup(html, 'lxml')
    grids = dxgridparser.find_all_grids(soup)
    
    print(f"Found {len(grids)} grid(s)\n")
    
    if grids:
        grid = grids[0]
        print(f"Grid info: {grid}")
        print(f"Headers: {grid.headers}")
        print(f"Number of rows: {len(grid.data)}\n")
        
        print("Data as dictionaries:")
        for row in grid.to_dicts():
            print(f"  {row}")
        
        print("\nData as DataFrame:")
        print(grid.to_dataframe())
        print()


def example2_multiple_grids():
    """Example 2: Finding multiple grids on a page"""
    print("=" * 60)
    print("Example 2: Multiple Grids")
    print("=" * 60)
    
    html = """
    <html>
        <body>
            <div id="ProductGrid" class="dxgvControl">
                <table>
                    <tr class="dxgvHeader">
                        <th>Product</th>
                        <th>Price</th>
                    </tr>
                    <tr>
                        <td>Widget</td>
                        <td>19.99</td>
                    </tr>
                    <tr>
                        <td>Gadget</td>
                        <td>29.99</td>
                    </tr>
                </table>
            </div>
            
            <div id="CustomerGrid" class="aspxgridview">
                <table>
                    <thead>
                        <tr>
                            <th>Customer</th>
                            <th>Country</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Acme Corp</td>
                            <td>USA</td>
                        </tr>
                        <tr>
                            <td>Tech Inc</td>
                            <td>Canada</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """
    
    soup = BeautifulSoup(html, 'lxml')
    grids = dxgridparser.find_all_grids(soup)
    
    print(f"Found {len(grids)} grid(s)\n")
    
    for i, grid in enumerate(grids):
        print(f"Grid {i + 1}:")
        print(f"  ID: {grid.metadata.get('grid_id', 'N/A')}")
        print(f"  Headers: {grid.headers}")
        print(f"  Rows: {len(grid.data)}")
        print(f"  Data: {grid.to_dicts()}")
        print()


def example3_metadata():
    """Example 3: Working with metadata"""
    print("=" * 60)
    print("Example 3: Grid Metadata")
    print("=" * 60)
    
    html = """
    <div id="MyGrid" class="dxgvControl dxgvTable" data-grid-name="MainGrid" data-page-size="10">
        <table>
            <tr>
                <th>ID</th>
                <th>Status</th>
            </tr>
            <tr>
                <td>1</td>
                <td>Active</td>
            </tr>
        </table>
    </div>
    """
    
    soup = BeautifulSoup(html, 'lxml')
    grids = dxgridparser.find_all_grids(soup)
    
    if grids:
        grid = grids[0]
        print(f"Grid metadata:")
        for key, value in grid.metadata.items():
            print(f"  {key}: {value}")
        print()


def example4_pandas_operations():
    """Example 4: Pandas DataFrame operations"""
    print("=" * 60)
    print("Example 4: Pandas Operations")
    print("=" * 60)
    
    html = """
    <table class="dxgvTable">
        <thead>
            <tr>
                <th>Product</th>
                <th>Category</th>
                <th>Price</th>
                <th>Quantity</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Laptop</td>
                <td>Electronics</td>
                <td>1200</td>
                <td>5</td>
            </tr>
            <tr>
                <td>Mouse</td>
                <td>Electronics</td>
                <td>25</td>
                <td>50</td>
            </tr>
            <tr>
                <td>Desk</td>
                <td>Furniture</td>
                <td>350</td>
                <td>10</td>
            </tr>
            <tr>
                <td>Chair</td>
                <td>Furniture</td>
                <td>200</td>
                <td>15</td>
            </tr>
        </tbody>
    </table>
    """
    
    soup = BeautifulSoup(html, 'lxml')
    grids = dxgridparser.find_all_grids(soup)
    
    if grids:
        grid = grids[0]
        df = grid.to_dataframe()
        
        print("Original DataFrame:")
        print(df)
        print()
        
        print("Summary statistics:")
        print(df.describe())
        print()
        
        print("Group by Category:")
        grouped = df.groupby('Category').agg({
            'Price': 'mean',
            'Quantity': 'sum'
        })
        print(grouped)
        print()
        
        print("Filter: Products with Price > 100:")
        expensive = df[df['Price'] > 100]
        print(expensive)
        print()


def main():
    """Run all examples"""
    try:
        example1_basic_usage()
        example2_multiple_grids()
        example3_metadata()
        example4_pandas_operations()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


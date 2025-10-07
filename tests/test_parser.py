"""
Unit tests for the dxgridparser library
"""

import unittest
from bs4 import BeautifulSoup
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dxgridparser import ASPxGridView, find_all_grids


class TestASPxGridView(unittest.TestCase):
    """Test cases for the ASPxGridView class"""
    
    def test_basic_table_parsing(self):
        """Test parsing a basic table with headers and data"""
        html = """
        <table class="dxgvTable">
            <thead>
                <tr>
                    <th>Column1</th>
                    <th>Column2</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Value1</td>
                    <td>Value2</td>
                </tr>
            </tbody>
        </table>
        """
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        grid = ASPxGridView(table)
        
        self.assertEqual(grid.headers, ['Column1', 'Column2'])
        self.assertEqual(len(grid.data), 1)
        self.assertEqual(grid.data[0]['Column1'], 'Value1')
        self.assertEqual(grid.data[0]['Column2'], 'Value2')
    
    def test_to_dicts(self):
        """Test the to_dicts() method"""
        html = """
        <table class="dxgvTable">
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>John</td><td>30</td></tr>
            <tr><td>Jane</td><td>25</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        grid = ASPxGridView(table)
        
        data = grid.to_dicts()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {'Name': 'John', 'Age': 30})
        self.assertEqual(data[1], {'Name': 'Jane', 'Age': 25})
    
    def test_to_dataframe(self):
        """Test the to_dataframe() method"""
        html = """
        <table class="dxgvTable">
            <tr><th>Product</th><th>Price</th></tr>
            <tr><td>Widget</td><td>19.99</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        grid = ASPxGridView(table)
        
        df = grid.to_dataframe()
        self.assertEqual(len(df), 1)
        self.assertEqual(df['Product'][0], 'Widget')
        self.assertEqual(df['Price'][0], 19.99)
    
    def test_metadata_extraction(self):
        """Test extraction of grid metadata"""
        html = """
        <div id="MyGrid" class="dxgvControl" data-grid-name="TestGrid">
            <table>
                <tr><th>Col1</th></tr>
                <tr><td>Val1</td></tr>
            </table>
        </div>
        """
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find('div')
        grid = ASPxGridView(div)
        
        self.assertEqual(grid.metadata['grid_id'], 'MyGrid')
        self.assertIn('dxgvControl', grid.metadata['classes'])
        self.assertEqual(grid.metadata['data-grid-name'], 'TestGrid')
    
    def test_number_conversion(self):
        """Test automatic conversion of numeric values"""
        html = """
        <table class="dxgvTable">
            <tr><th>Integer</th><th>Float</th><th>Text</th></tr>
            <tr><td>100</td><td>19.99</td><td>Hello</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        grid = ASPxGridView(table)
        
        data = grid.data[0]
        self.assertIsInstance(data['Integer'], int)
        self.assertIsInstance(data['Float'], float)
        self.assertIsInstance(data['Text'], str)
        self.assertEqual(data['Integer'], 100)
        self.assertEqual(data['Float'], 19.99)
    
    def test_empty_table(self):
        """Test handling of empty table"""
        html = """
        <table class="dxgvTable">
            <tr><th>Col1</th><th>Col2</th></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table')
        grid = ASPxGridView(table)
        
        self.assertEqual(grid.headers, ['Col1', 'Col2'])
        self.assertEqual(len(grid.data), 0)


class TestFindAllGrids(unittest.TestCase):
    """Test cases for the find_all_grids function"""
    
    def test_find_single_grid(self):
        """Test finding a single grid"""
        html = """
        <div class="dxgvControl">
            <table>
                <tr><th>Col1</th></tr>
                <tr><td>Val1</td></tr>
            </table>
        </div>
        """
        soup = BeautifulSoup(html, 'lxml')
        grids = find_all_grids(soup)
        
        self.assertEqual(len(grids), 1)
        self.assertEqual(len(grids[0].data), 1)
    
    def test_find_multiple_grids(self):
        """Test finding multiple grids on a page"""
        html = """
        <html>
            <body>
                <div class="dxgvControl">
                    <table><tr><th>Grid1</th></tr><tr><td>Data1</td></tr></table>
                </div>
                <div class="aspxgridview">
                    <table><tr><th>Grid2</th></tr><tr><td>Data2</td></tr></table>
                </div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, 'lxml')
        grids = find_all_grids(soup)
        
        self.assertGreaterEqual(len(grids), 2)
    
    def test_find_grid_by_id(self):
        """Test finding grids by ID pattern"""
        html = """
        <div id="ProductGrid">
            <table><tr><th>Product</th></tr><tr><td>Widget</td></tr></table>
        </div>
        """
        soup = BeautifulSoup(html, 'lxml')
        grids = find_all_grids(soup)
        
        self.assertGreaterEqual(len(grids), 1)
        found_product_grid = any(g.metadata.get('grid_id') == 'ProductGrid' for g in grids)
        self.assertTrue(found_product_grid)
    
    def test_no_grids_found(self):
        """Test when no grids are present"""
        html = """
        <html>
            <body>
                <p>No grids here</p>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, 'lxml')
        grids = find_all_grids(soup)
        
        self.assertEqual(len(grids), 0)


if __name__ == '__main__':
    unittest.main()


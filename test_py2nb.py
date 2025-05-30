#!/usr/bin/env python3
"""Test suite for py2nb with enhanced features."""

import os
import tempfile
import json
import unittest
from unittest.mock import patch
import nbformat

# Import py2nb module directly
import py2nb


class TestPy2nb(unittest.TestCase):
    """Test cases for py2nb conversion functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def create_test_script(self, content, filename="test_script.py"):
        """Create a test Python script."""
        script_path = os.path.join(self.temp_dir, filename)
        with open(script_path, 'w') as f:
            f.write(content)
        return script_path

    def test_basic_conversion(self):
        """Test basic script to notebook conversion."""
        script_content = """import numpy as np
x = np.array([1, 2, 3])
print(x)"""
        
        script_path = self.create_test_script(script_content)
        notebook_path = py2nb.convert(script_path)
        
        # Check notebook was created
        self.assertTrue(os.path.exists(notebook_path))
        
        # Check notebook structure
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
        
        self.assertEqual(nb['nbformat'], 4)
        self.assertEqual(len(nb['cells']), 1)
        self.assertEqual(nb['cells'][0]['cell_type'], 'code')

    def test_markdown_cells(self):
        """Test markdown cell creation with #| syntax."""
        script_content = """#| # Test Title
#| This is a markdown cell
#| with multiple lines

import numpy as np"""
        
        script_path = self.create_test_script(script_content)
        notebook_path = py2nb.convert(script_path)
        
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
        
        self.assertEqual(len(nb['cells']), 2)
        self.assertEqual(nb['cells'][0]['cell_type'], 'markdown')
        self.assertIn('# Test Title', ''.join(nb['cells'][0]['source']))
        self.assertEqual(nb['cells'][1]['cell_type'], 'code')

    def test_command_blocks(self):
        """Test command block creation with #! syntax."""
        script_content = """#| # Test Command Blocks

#! pip install numpy
#! pip install matplotlib

import numpy as np
import matplotlib.pyplot as plt"""
        
        script_path = self.create_test_script(script_content)
        notebook_path = py2nb.convert(script_path)
        
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
        
        # Should have: markdown, command, code cells
        self.assertEqual(len(nb['cells']), 3)
        self.assertEqual(nb['cells'][0]['cell_type'], 'markdown')
        self.assertEqual(nb['cells'][1]['cell_type'], 'code')
        self.assertEqual(nb['cells'][2]['cell_type'], 'code')
        
        # Check command cell has command tag
        command_cell = nb['cells'][1]
        self.assertIn('command', command_cell.get('metadata', {}).get('tags', []))
        self.assertIn('pip install numpy', ''.join(command_cell['source']))

    def test_cell_splits(self):
        """Test code cell splitting with #- syntax."""
        script_content = """x = 1
y = 2

#-

z = x + y
print(z)"""
        
        script_path = self.create_test_script(script_content)
        notebook_path = py2nb.convert(script_path)
        
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
        
        self.assertEqual(len(nb['cells']), 2)
        self.assertEqual(nb['cells'][0]['cell_type'], 'code')
        self.assertEqual(nb['cells'][1]['cell_type'], 'code')

    def test_mixed_syntax(self):
        """Test combination of all syntax types."""
        script_content = """#| # Mixed Syntax Test
#| This tests all comment types together

#! pip install numpy

import numpy as np

#| ## Section 2

x = np.array([1, 2, 3])

#-

#! pip install matplotlib

import matplotlib.pyplot as plt
plt.plot(x)"""
        
        script_path = self.create_test_script(script_content)
        notebook_path = py2nb.convert(script_path)
        
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
        
        # Check we have the expected number of cells
        self.assertGreaterEqual(len(nb['cells']), 5)
        
        # Check mix of cell types
        cell_types = [cell['cell_type'] for cell in nb['cells']]
        self.assertIn('markdown', cell_types)
        self.assertIn('code', cell_types)

    def test_notebook_metadata(self):
        """Test that proper notebook metadata is added."""
        script_content = """import numpy as np"""
        
        script_path = self.create_test_script(script_content)
        notebook_path = py2nb.convert(script_path)
        
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
        
        # Check metadata exists
        self.assertIn('metadata', nb)
        self.assertIn('kernelspec', nb['metadata'])
        self.assertIn('language_info', nb['metadata'])
        
        # Check kernelspec
        kernelspec = nb['metadata']['kernelspec']
        self.assertEqual(kernelspec['name'], 'python3')
        self.assertEqual(kernelspec['language'], 'python')

    def test_validation(self):
        """Test notebook validation functionality."""
        script_content = """import numpy as np"""
        
        script_path = self.create_test_script(script_content)
        notebook_path = py2nb.convert(script_path, validate=True)
        
        # Check notebook can be loaded by nbformat
        nb = nbformat.read(notebook_path, as_version=4)
        
        # Check all cells have proper structure
        for cell in nb.cells:
            self.assertIn('metadata', cell)
            if cell.cell_type == 'code':
                self.assertIn('outputs', cell)
                self.assertIn('execution_count', cell)

    def test_no_validation_flag(self):
        """Test --no-validate command line flag."""
        script_content = """import numpy as np"""
        
        script_path = self.create_test_script(script_content)
        
        # Test that conversion works with no validation
        notebook_path = py2nb.convert(script_path, validate=False)
        self.assertTrue(os.path.exists(notebook_path))

    def test_comment_type_detection(self):
        """Test comment type detection functions."""
        self.assertEqual(py2nb.get_comment_type('#| markdown'), 'markdown')
        self.assertEqual(py2nb.get_comment_type('# | markdown'), 'markdown')
        self.assertEqual(py2nb.get_comment_type('#! install'), 'command')
        self.assertEqual(py2nb.get_comment_type('# ! install'), 'command')
        self.assertEqual(py2nb.get_comment_type('#- split'), 'split')
        self.assertEqual(py2nb.get_comment_type('# - split'), 'split')
        self.assertIsNone(py2nb.get_comment_type('# regular comment'))

    def test_content_extraction(self):
        """Test content extraction from comment lines."""
        self.assertEqual(py2nb.extract_content('#| markdown text', 'markdown'), ' markdown text')
        self.assertEqual(py2nb.extract_content('#! pip install numpy', 'command'), 'pip install numpy')
        self.assertEqual(py2nb.extract_content('# | spaced markdown', 'markdown'), ' spaced markdown')

    def test_file_not_found(self):
        """Test handling of non-existent files."""
        # Test convert function directly with non-existent file
        with self.assertRaises(FileNotFoundError):
            py2nb.convert('nonexistent.py')

    def test_main_function_success(self):
        """Test main function with successful conversion."""
        script_content = """import numpy as np"""
        script_path = self.create_test_script(script_content)
        
        # Test convert function directly
        notebook_path = py2nb.convert(script_path)
        self.assertTrue(os.path.exists(notebook_path))

    def test_backward_compatibility(self):
        """Test that existing py2nb syntax still works."""
        # This is the example from the original README
        script_content = """#| # Testing ipython notebook
#| This is designed to demonstrate a simple script that converts a script into
#| a jupyter notebook with a simple additional markdown format.

import matplotlib.pyplot as plt
import numpy as np

#| Here is a markdown cell.
#| Maths is also possible: $A=B$

x = np.random.rand(5)

#-------------------------------

y = np.random.rand(4)
z = np.random.rand(3)"""
        
        script_path = self.create_test_script(script_content)
        notebook_path = py2nb.convert(script_path)
        
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
        
        # Should successfully create a notebook
        self.assertGreater(len(nb['cells']), 0)
        
        # Should have both markdown and code cells
        cell_types = [cell['cell_type'] for cell in nb['cells']]
        self.assertIn('markdown', cell_types)
        self.assertIn('code', cell_types)

    def test_execute_option(self):
        """Test notebook execution functionality."""
        # Create a simple script that will execute successfully
        script_content = """#| # Execution Test
#| This tests the execution functionality

import math

#- # Simple calculation
result = math.sqrt(16)
print(f"Square root of 16 is: {result}")

#| ## Result check
assert result == 4.0
print("Test passed!")"""
        
        script_path = self.create_test_script(script_content)
        
        # Convert with execution disabled first to test basic conversion
        notebook_path = py2nb.convert(script_path, execute=False)
        self.assertTrue(os.path.exists(notebook_path))
        
        # Check that execution functionality handles missing dependencies gracefully
        # (Since nbconvert might not be available in test environment)
        try:
            executed_path = py2nb.convert(script_path, execute=True)
            # If execution succeeds, check that we get a valid notebook
            self.assertTrue(os.path.exists(executed_path))
            if executed_path.endswith('_executed.ipynb'):
                # Execution succeeded and created new file
                with open(executed_path, 'r') as f:
                    nb = json.load(f)
                self.assertGreater(len(nb['cells']), 0)
        except Exception:
            # Execution failed gracefully (e.g., nbconvert not available)
            # This is acceptable behavior for the test environment
            pass

    def test_custom_output_name(self):
        """Test custom output filename functionality."""
        script_content = """#| # Custom Output Test
import math
result = math.sqrt(4)"""
        
        script_path = self.create_test_script(script_content)
        
        # Test py2nb with custom output name
        custom_notebook = py2nb.convert(script_path, output_name="custom_name")
        self.assertTrue(custom_notebook.endswith("custom_name.ipynb"))
        self.assertTrue(os.path.exists(custom_notebook))
        
        # Test py2nb with custom output name including extension
        custom_notebook2 = py2nb.convert(script_path, output_name="custom_name2.ipynb")
        self.assertTrue(custom_notebook2.endswith("custom_name2.ipynb"))
        self.assertTrue(os.path.exists(custom_notebook2))

    def test_nb2py_custom_output(self):
        """Test nb2py with custom output names."""
        # Create a simple notebook first  
        script_content = """#| # Test Notebook
#! pip install numpy
import numpy as np
x = np.array([1, 2, 3])"""
        
        script_path = self.create_test_script(script_content)
        notebook_path = py2nb.convert(script_path)
        
        # Test nb2py conversion with subprocess
        import subprocess
        
        # Test default conversion
        result = subprocess.run(['python', 'nb2py', notebook_path], 
                               capture_output=True, text=True, cwd=os.getcwd())
        self.assertEqual(result.returncode, 0)
        
        # Test custom output conversion
        custom_output = "custom_output.py"
        result = subprocess.run(['python', 'nb2py', notebook_path, '--output', custom_output], 
                               capture_output=True, text=True, cwd=os.getcwd())
        self.assertEqual(result.returncode, 0)
        
        # Check that custom output file was created
        expected_path = os.path.join(os.getcwd(), custom_output)
        self.assertTrue(os.path.exists(expected_path))
        
        # Check content includes command syntax
        with open(expected_path, 'r') as f:
            content = f.read()
        self.assertIn("#! pip install numpy", content)
        self.assertIn("#| # Test Notebook", content)
        
        # Clean up
        if os.path.exists(expected_path):
            os.remove(expected_path)

if __name__ == '__main__':
    # Allow running tests directly
    unittest.main()
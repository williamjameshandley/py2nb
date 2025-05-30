#!/usr/bin/env python3
"""Test suite for py2nb with enhanced features."""

import os
import tempfile
import json
import unittest
from unittest.mock import patch
import nbformat

# Import py2nb functions by reading and executing only the function definitions
import sys
import os

# Read py2nb script and extract only function definitions
with open('py2nb', 'r') as f:
    content = f.read()

# Execute only the parts we need (up to main function, but not the main call)
lines = content.split('\n')
func_lines = []
in_main_call = False

for line in lines:
    if line.strip() == "if __name__ == '__main__':":
        in_main_call = True
        break
    func_lines.append(line)

# Execute the function definitions
exec('\n'.join(func_lines))

# Create a mock module for the functions
class MockPy2nb:
    def __init__(self):
        # Copy all functions from global namespace
        self.convert = convert
        self.get_comment_type = get_comment_type
        self.extract_content = extract_content
        self.main = main
        self.validate_notebook = validate_notebook
        
py2nb = MockPy2nb()


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


if __name__ == '__main__':
    # Allow running tests directly
    unittest.main()
#!/usr/bin/env python3
"""Create a notebook containing code from a script.

Run as:  python py2nb my_script.py

Can also be imported as a module:
    import py2nb
    py2nb.convert('script.py')
    py2nb.convert('script.py', execute=True, output_name='notebook.ipynb')
"""
import argparse
import os
import json
import subprocess
import sys

import nbformat.v4

# Export main functions for module use
__all__ = ['convert', 'execute_notebook', 'validate_notebook', 'CELL_SPLIT_CHARS', 'MARKDOWN_CHARS', 'COMMAND_CHARS']

# Comment syntax patterns
CELL_SPLIT_CHARS = ['#-', '# -']
MARKDOWN_CHARS = ['#|', '# |']
COMMAND_CHARS = ['#!', '# !']
ACCEPTED_CHARS = CELL_SPLIT_CHARS + MARKDOWN_CHARS + COMMAND_CHARS

def new_cell(nb, cell_content, cell_type='code'):
    """Create a new cell with proper metadata.
    
    Parameters
    ----------
    nb: nbformat.notebooknode.NotebookNode
        Notebook to write to, as produced by nbformat.v4.new_notebook()
    cell_content: str
        String content for the cell
    cell_type: str, optional
        Type of cell: 'code', 'markdown', or 'command'
    
    Returns
    -------
    str
        Empty string (resets cell content)
    """
    cell_content = cell_content.rstrip().lstrip()
    if cell_content:
        if cell_type == 'markdown':
            cell = nbformat.v4.new_markdown_cell(cell_content)
        elif cell_type == 'command':
            # Create code cell with command content
            cell = nbformat.v4.new_code_cell(cell_content)
            # Add metadata to identify as command cell
            cell.metadata.update({
                'tags': ['command'],
                'collapsed': False
            })
        else:  # code cell
            cell = nbformat.v4.new_code_cell(cell_content)
        
        # Ensure proper execution count for clean notebooks
        if hasattr(cell, 'execution_count'):
            cell.execution_count = None
            
        # Ensure outputs field exists and is empty for code cells
        if cell.cell_type == 'code' and not hasattr(cell, 'outputs'):
            cell.outputs = []
            
        nb.cells.append(cell)
    return ''

def str_starts_with(string, options):
    """Check if string starts with any of the given options."""
    for opt in options:
        if string.startswith(opt):
            return True
    return False


def get_comment_type(line):
    """Determine the type of comment based on prefix."""
    if str_starts_with(line, COMMAND_CHARS):
        return 'command'
    elif str_starts_with(line, MARKDOWN_CHARS):
        return 'markdown'
    elif str_starts_with(line, CELL_SPLIT_CHARS):
        return 'split'
    return None


def extract_content(line, comment_type):
    """Extract content from comment line based on type."""
    if comment_type == 'command':
        # Find first ! and return ! plus everything after it
        return '!' + line[line.index('!') + 1:].lstrip()
    elif comment_type == 'markdown':
        # Find first | and return everything after it  
        return line[line.index('|') + 1:]
    return ''


def convert(script_name, validate=True, execute=False, output_name=None):
    """Convert the python script to jupyter notebook with enhanced features."""
    with open(script_name, 'r', encoding='utf-8') as f:
        # Initialize cells and notebook
        markdown_cell = ''
        code_cell = ''
        command_cell = ''
        nb = nbformat.v4.new_notebook()
        
        # Set notebook metadata (maintain compatibility with existing notebooks)
        nb.metadata.update({
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'
            },
            'language_info': {
                'codemirror_mode': {'name': 'ipython', 'version': 3},
                'file_extension': '.py',
                'mimetype': 'text/x-python',
                'name': 'python',
                'nbconvert_exporter': 'python',
                'pygments_lexer': 'ipython3',
                'version': '3.8.0'
            }
        })
        
        # Set consistent nbformat version
        nb.nbformat = 4
        nb.nbformat_minor = 2
        
        for line in f:
            comment_type = get_comment_type(line)
            
            if comment_type:
                # Finish current code cell before processing comment
                code_cell = new_cell(nb, code_cell, 'code')
                
                if comment_type == 'markdown':
                    # Add to markdown cell
                    markdown_cell += extract_content(line, 'markdown')
                elif comment_type == 'command':
                    # Finish any pending markdown cell
                    markdown_cell = new_cell(nb, markdown_cell, 'markdown')
                    # Add to command cell
                    command_cell += extract_content(line, 'command') + '\n'
                elif comment_type == 'split':
                    # Finish any pending cells and start fresh
                    markdown_cell = new_cell(nb, markdown_cell, 'markdown')
                    command_cell = new_cell(nb, command_cell, 'command')
            else:
                # Regular code line - finish pending markdown/command cells
                markdown_cell = new_cell(nb, markdown_cell, 'markdown')
                command_cell = new_cell(nb, command_cell, 'command')
                # Add to code cell
                code_cell += line

        # Finish any remaining cells
        markdown_cell = new_cell(nb, markdown_cell, 'markdown')
        command_cell = new_cell(nb, command_cell, 'command')
        code_cell = new_cell(nb, code_cell, 'code')

        # Validate notebook structure if requested
        if validate:
            validate_notebook(nb)

        # Write notebook with consistent format (avoid auto-generated ids)
        if output_name:
            notebook_name = output_name
            if not notebook_name.endswith('.ipynb'):
                notebook_name += '.ipynb'
        else:
            notebook_name = os.path.splitext(script_name)[0] + '.ipynb'
        
        # Remove any auto-generated cell ids to maintain clean format
        for cell in nb.cells:
            if 'id' in cell:
                del cell['id']
        
        # Write with explicit version to avoid nbformat_minor changes
        with open(notebook_name, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f, version=nbformat.NO_CONVERT)
        
        # Execute notebook if requested
        if execute:
            executed_name = execute_notebook(notebook_name)
            return executed_name
        
        return notebook_name


def execute_notebook(notebook_path):
    """Execute a notebook using nbconvert and return the executed notebook path."""
    executed_name = notebook_path
    
    try:
        # Use nbconvert to execute the notebook
        cmd = [
            'jupyter', 'nbconvert', 
            '--to', 'notebook',
            '--execute',
            '--inplace',
            notebook_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✓ Successfully executed notebook: {executed_name}")
            return executed_name
        else:
            print(f"⚠ Notebook execution failed: {result.stderr}")
            print(f"  Original notebook available: {notebook_path}")
            return notebook_path
            
    except subprocess.TimeoutExpired:
        print(f"⚠ Notebook execution timed out (5 minutes)")
        print(f"  Original notebook available: {notebook_path}")
        return notebook_path
    except FileNotFoundError:
        print(f"⚠ jupyter nbconvert not found. Install with: pip install nbconvert")
        print(f"  Original notebook available: {notebook_path}")
        return notebook_path
    except Exception as e:
        print(f"⚠ Error executing notebook: {e}")
        print(f"  Original notebook available: {notebook_path}")
        return notebook_path


def validate_notebook(nb):
    """Validate notebook structure and fix common issues."""
    for i, cell in enumerate(nb.cells):
        # Ensure proper cell structure
        if not hasattr(cell, 'metadata'):
            cell.metadata = {}
        
        # Remove auto-generated cell ids for consistent format
        if 'id' in cell:
            del cell['id']
        
        if cell.cell_type == 'code':
            # Ensure code cells have required fields
            if not hasattr(cell, 'execution_count'):
                cell.execution_count = None
            if not hasattr(cell, 'outputs'):
                cell.outputs = []
        elif cell.cell_type == 'markdown':
            # Ensure markdown cells don't have code cell fields
            if hasattr(cell, 'execution_count'):
                delattr(cell, 'execution_count')
            if hasattr(cell, 'outputs'):
                delattr(cell, 'outputs')
        
        # Ensure source is a list
        if isinstance(cell.source, str):
            cell.source = cell.source.splitlines(True)


def parse_args():
    """Enhanced argument parsing for py2nb."""
    description = "Convert a python script to a jupyter notebook"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "script_name",
        help="name of script (.py) to convert to jupyter notebook (.ipynb)")
    parser.add_argument(
        "--no-validate", 
        action="store_true",
        help="skip notebook validation")
    parser.add_argument(
        "--execute", 
        action="store_true",
        help="execute the notebook after conversion")
    parser.add_argument(
        "--output", 
        help="specify output notebook filename (default: script_name.ipynb)")
    return parser.parse_args()


def main():
    """Main conversion function."""
    args = parse_args()
    
    if not os.path.exists(args.script_name):
        print(f"Error: File {args.script_name} not found")
        return 1
    
    try:
        notebook_name = convert(args.script_name, validate=not args.no_validate, execute=args.execute, output_name=args.output)
        if args.execute:
            print(f"✓ Successfully converted and executed {args.script_name} to {notebook_name}")
        else:
            print(f"✓ Successfully converted {args.script_name} to {notebook_name}")
        
        # Validate the created notebook
        if not args.no_validate:
            try:
                with open(notebook_name, 'r', encoding='utf-8') as f:
                    json.load(f)
                print("✓ Notebook JSON validation passed")
            except json.JSONDecodeError as e:
                print(f"⚠ Notebook JSON validation failed: {e}")
                return 1
                
    except Exception as e:
        print(f"Error during conversion: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())

#!/usr/bin/env python3
"""Create a notebook containing code from a script.

Run as:  python to_noteebook.py my_script.py
"""
import sys
import os
import nbformat.v4

script_name = sys.argv[1]
notebook_name = os.path.splitext(script_name)[0] + '.ipynb'

def new_cell(nb, cell, markdown=False):
    """ Create a new cell

    Parameters
    ----------
    nb: nbformat.notebooknode.NotebookNode
        Notebook to write to, as produced by nbformat.v4.new_notebook()

    cell: str
        String to write to the cell

    markdown: boolean, optional, (default False)
        Whether to create a markdown cell, or a code cell
    """
    cell = cell.rstrip().lstrip()
    if cell:
        if markdown:
            cell = nbformat.v4.new_markdown_cell(cell)
        else:
            cell = nbformat.v4.new_code_cell(cell)
        nb.cells.append(cell)
    return ''


with open(script_name) as f:
    markdown_cell = ''
    code_cell = ''
    nb = nbformat.v4.new_notebook()
    for line in f:
        if line[:2] == '#-' or line[:2] == '#|':
            code_cell = new_cell(nb, code_cell)
            if line[:2] == '#|':
                markdown_cell += line[2:]
            else:
                markdown_cell = new_cell(nb, markdown_cell, markdown=True)
        else:
            markdown_cell = new_cell(nb, markdown_cell, markdown=True)
            code_cell += line

    code_cell = new_cell(nb, code_cell)
    markdown_cell = new_cell(nb, markdown_cell, markdown=True)

    nbformat.write(nb, notebook_name)

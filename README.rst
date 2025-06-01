==================================================
py2nb: convert python scripts to jupyter notebooks
==================================================
:py2nb: convert python scripts to jupyter notebooks
:Author: Will Handley
:Version: 1.1.1
:Homepage: https://github.com/williamjameshandley/py2nb

.. image:: https://badge.fury.io/py/py2nb.svg
   :target: https://badge.fury.io/py/py2nb
   :alt: PyPi location

Description
===========

``py2nb`` is a python package for converting python scripts with minimal
markdown to jupyter notebooks.

Markdown cells are rendered from comments beginning with ``#|``, splits between
code cells are created by comment lines beginning with ``#-``, and command cells
(for shell commands like pip installs) are created from comments beginning with ``#!``

``nb2py`` converts from jupyter notebooks to python

Installation
============

Users can install using pip:

.. code:: bash

   pip install py2nb

from source:

.. code:: bash

   git clone https://github.com/williamjameshandley/py2nb
   cd py2nb
   python setup.py install

or for those on `Arch linux <https://www.archlinux.org/>`__ it is
available on the
`AUR <https://aur.archlinux.org/packages/python-py2nb/>`__

Programmatic Usage
==================

Both ``py2nb`` and ``nb2py`` can be imported and used programmatically:

.. code:: python

   import py2nb
   import nb2py
   
   # Convert script to notebook
   notebook_path = py2nb.convert('script.py')
   
   # Convert with custom output and execution
   executed_notebook = py2nb.convert('script.py', 
                                     output_name='workshop.ipynb', 
                                     execute=True)
   
   # Convert notebook back to script  
   script_path = nb2py.convert('notebook.ipynb', output_name='converted.py')

Example
=======

If one has a script named ``example.py`` containing the code:

.. code:: python

    #| # Testing ipython notebook
    #| This is designed to demonstrate a simple script that converts a script into
    #| a jupyter notebook with a simple additional markdown format.
    #|
    #| Code by default will be put into code cells
    #|
    #| * To make a markdown cell, prefix the comment line with '#|' or '# |'
    #| * To split a code cell, add a line beginning with '#-' or '# -'
    #| * To make a command cell, prefix the comment line with '#!' or '# !'

    #! pip install matplotlib numpy
    #! pip install scipy

    import matplotlib.pyplot as plt
    import numpy as np

    %matplotlib inline

    #| Here is a markdown cell.
    #| Maths is also possible: $A=B$
    #|
    #| There are code cells below, split by `'#-'`:

    # | Here is another markdown cell

    x = np.random.rand(5)

    #-------------------------------

    y = np.random.rand(4)
    z = np.random.rand(3)

    #| Here are some plots

    x = np.linspace(-2,2,1000)
    y = x**3
    fig, ax = plt.subplots()
    ax.plot(x,y)

    # -------------------------------

    # | Here is another plot

    x = np.linspace(-np.pi, np.pi, 201)
    fig, ax = plt.subplots()
    ax.plot(x,np.sin(x))


then running

.. code :: bash

   py2nb example.py

produces the notebook `example.ipynb <https://github.com/williamjameshandley/py2nb/blob/master/example.ipynb>`_

To see an executed version with outputs and plots, run:

.. code :: bash

   py2nb example.py --execute --output example_executed

which produces `example_executed.ipynb <https://github.com/williamjameshandley/py2nb/blob/master/example_executed.ipynb>`_ with all code cells executed and outputs displayed.

Command Line Options
====================

.. code:: bash

   py2nb script.py                      # Basic conversion
   py2nb script.py --no-validate        # Skip notebook validation  
   py2nb script.py --execute            # Convert and execute notebook
   py2nb script.py --output workshop    # Custom output name
   py2nb script.py --output workshop --execute  # Custom name + execution

   nb2py notebook.ipynb                 # Convert notebook to script
   nb2py notebook.ipynb --output script # Custom output script name

Command Blocks
==============

Command blocks allow you to run shell commands (like pip installs) in separate notebook cells:

.. code:: python

    #| # Workshop Example
    #| This demonstrates command blocks for dependency management

    #! pip install numpy matplotlib
    #! pip install seaborn

    import numpy as np
    import matplotlib.pyplot as plt

    #| ## Advanced Analysis
    #| Install additional dependencies when needed

    #! pip install scikit-learn

    from sklearn import datasets

This creates dedicated cells for commands, improving modularity and compatibility
with platforms like Google Colab.

Execution Option
================

The ``--execute`` option runs the converted notebook using jupyter nbconvert,
creating a new notebook with outputs included:

.. code:: bash

   py2nb workshop.py --execute                    # Execute in place
   py2nb workshop.py --output clean               # Create clean.ipynb
   py2nb workshop.py --output executed --execute  # Create executed.ipynb with outputs

The ``--output`` option allows you to specify custom filenames, giving you complete control
over the generated notebook names. Useful for creating workshop materials with pre-computed 
results, or for testing that your workshop notebooks execute successfully.

**Requirements**: Requires ``nbconvert`` to be installed (``pip install nbconvert``).

Testing
=======

To run the test suite:

.. code:: bash

   python test_py2nb.py

The test suite includes 16 test cases covering:

* Basic conversion functionality
* Markdown cell creation (``#|`` syntax)
* Code cell splitting (``#-`` syntax)
* Command block creation (``#!`` syntax)
* Notebook execution (``--execute`` option)
* Custom output filenames (``--output`` option)
* nb2py reverse conversion with custom output
* Programmatic module usage
* Mixed syntax combinations
* Notebook metadata and validation
* UTF-8 encoding support
* Backward compatibility
* Error handling

Vim Integration
===============

For vim users working with py2nb syntax, you can enhance your editing experience:

**Syntax Highlighting**

Add to your ``.vimrc`` for basic py2nb syntax support:

.. code:: vim

   " py2nb syntax highlighting
   autocmd BufRead,BufNewFile *.py syntax match Comment "#|.*$" 
   autocmd BufRead,BufNewFile *.py syntax match Special "#!.*$"
   autocmd BufRead,BufNewFile *.py syntax match Delimiter "#-.*$"

**File Templates**

Create a py2nb template in ``~/.vim/templates/py2nb.py``:

.. code:: python

   #| # Workshop Title
   #| 
   #| Brief description and learning objectives
   
   #! pip install required_packages
   
   import standard_libraries
   
   #| ## Section 1: Core Concepts
   #| Essential material description
   
   # Your code here
   
   #-
   
   # Next code cell
   
   #| ## Section 2: Advanced Topics
   #| Building on previous concepts

Then use ``:read ~/.vim/templates/py2nb.py`` to insert the template.

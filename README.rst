==================================================
py2nb: convert python scripts to jupyter notebooks
==================================================
:py2nb: convert python scripts to jupyter notebooks
:Author: Will Handley
:Version: 1.0.0
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

Command Line Options
====================

.. code:: bash

   py2nb script.py                 # Basic conversion
   py2nb script.py --no-validate   # Skip notebook validation

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

Testing
=======

To run the test suite:

.. code:: bash

   python test_py2nb.py

The test suite includes 13 test cases covering:

* Basic conversion functionality
* Markdown cell creation (``#|`` syntax)
* Code cell splitting (``#-`` syntax)
* Command block creation (``#!`` syntax)
* Mixed syntax combinations
* Notebook metadata and validation
* Backward compatibility
* Error handling

To do
=====
- evaluation option for script produced
- vim syntax highlighting for markdown code blocks

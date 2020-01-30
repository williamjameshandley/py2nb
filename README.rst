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
code cells are created by comment lines beginning with ``#-``

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
    #| * To make a markdown cell, prefix the comment line with with '#|' or '# |'
    #| * To split a code cell, add a line beginning with '#-' or '# -'

    import matplotlib.pyplot as plt
    import numpy

    %matplotlib inline

    #| Here is a markdown cell.
    #| Maths is also possible: $A=B$
    #|
    #| There are code cells below, split by `'#-'`:

    # | Here is another markdown cell

    x = numpy.random.rand(5)

    #-------------------------------

    y = numpy.random.rand(4)
    z = numpy.random.rand(3)

    #| Here are some plots

    x = numpy.linspace(-2,2,1000)
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

To do
=====
- evaluation option for script produced
- vim syntax highlighting for markdown code blocks

==================================================
py2nb: convert python scripts to jupyter notebooks
==================================================
:py2nb: convert python scripts to jupyter notebooks
:Author: Will Handley
:Version: 0.0.0
:Homepage: https://github.com/williamjameshandley/py2nb

.. image:: https://badge.fury.io/py/py2nb.svg
   :target: https://badge.fury.io/py/py2nb
   :alt: PyPi location

Description
===========

``py2nb`` is a python package for converting python scripts with minimal markdown to jupyter notebooks.

Here is example code, saved as ``example.py``:

.. code:: python

   #| # Testing ipython notebook
   #| This is designed to demonstrate a simple script that converts a script into
   #| a jupyter notebook with a simple additional markdown format.
   #|
   #| Code by default will be put into code cells
   #| 
   #| * To make a markdown cell, prefix the comment line with with '#|'
   #| * To split a code cell, add a line beginning with '#-'

   import numpy
   import matplotlib.pyplot as plt
   %matplotlib inline

   #| Here is a markdown cell.
   #| Maths is also possible: $A=B$
   #|
   #| There are code cells below, split by '#-':

   x = numpy.random.rand(5)
   #---------------------------
   y = numpy.random.rand(4)
   z = numpy.random.rand(3)

   #| Here are some plots

   x = numpy.linspace(-2,2,1000)
   y = x**3
   fig, ax = plt.subplots()
   ax.plot(x,y)

Converting via the script

.. code :: bash
   
   py2nb example.py

   
produces the notebook `example.ipynb <https://github.com/williamjameshandley/py2nb/blob/master/example.ipynb>`_


To do
=====
- reverse script
- evaluation option for script produced
- vim syntax highlighting for markdown code blocks

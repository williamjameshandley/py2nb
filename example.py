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

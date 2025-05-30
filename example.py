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

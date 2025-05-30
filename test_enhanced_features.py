#| # Enhanced py2nb Test Workshop
#| 
#| This demonstrates the new enhanced py2nb syntax including:
#| - Installation blocks with `#!` syntax
#| - Proper cell metadata
#| - Modern notebook validation

#! pip install numpy matplotlib
#! pip install scipy

import numpy as np
import matplotlib.pyplot as plt

#| ## Basic Functionality
#| 
#| Let's start with some basic plotting to test core features.

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

#- # Split to new code cell

plt.figure(figsize=(8, 5))
plt.plot(x, y, label='sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Basic Plot Test')
plt.show()

#| ## Advanced Features Test
#| 
#| Now we'll test installing additional dependencies when needed.

#! pip install seaborn

import seaborn as sns

# Test advanced plotting
data = np.random.randn(100, 2)
plt.figure(figsize=(6, 6))
sns.scatterplot(x=data[:, 0], y=data[:, 1])
plt.title('Advanced Plotting Test')
plt.show()

#| ## Conclusion
#| 
#| This workshop tested:
#| - ✓ Installation blocks (`#!`)  
#| - ✓ Markdown cells (`#|`)
#| - ✓ Code cell splits (`#-`)
#| - ✓ Proper metadata handling
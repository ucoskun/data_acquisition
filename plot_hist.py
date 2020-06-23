import matplotlib
import numpy as np
import matplotlib.pyplot as plt

x = np.loadtxt("offset_122.txt")[:,0]
print(np.mean(x))
num_bins = 30

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, density=1)
plt.xlabel("Offset (uT)")
# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()

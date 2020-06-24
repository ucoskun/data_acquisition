import numpy as np
import matplotlib.pyplot as plt

t = [x for x in range(0, 20400, 400)]
x = np.loadtxt("ang_vs_field2.txt")[:,1]

ax = plt.subplot(111)
ax.plot(t, x, '.')
ax.grid(True)
plt.xlabel('time (s)')
plt.ylabel('field (nT)')

plt.show()

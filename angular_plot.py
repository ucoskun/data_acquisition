import numpy as np
import matplotlib.pyplot as plt

t = [x for x in range(0, 10400, 400)]
x = np.loadtxt("ang_vs_field2.txt")[:,1]

off = [(x[i]+x[25+i])/2 for i in range(26)]
for i in range(25):
    print((x[i]+x[25+i])/2)
ax = plt.subplot(111)
ax.plot(t, off, '.')
ax.grid(True)
plt.xlabel('angle (counts)')
plt.ylabel('field (nT)')

plt.show()

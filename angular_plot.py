import numpy as np
import matplotlib.pyplot as plt


theta = np.linspace(0,2*np.pi,41)
x = np.loadtxt("angular_1.txt")[:,0]
ax = plt.subplot(111)
ax.plot(theta, x)

ax.grid(True)

ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()

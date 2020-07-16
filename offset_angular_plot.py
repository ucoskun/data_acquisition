import numpy as np
import matplotlib.pyplot as plt

data_path = "data_out"
t = [x * 360 / 20000 for x in range(0, 10400, 400)]
x = np.loadtxt(data_path + "/ang_vs_field_7_16_2020_probe24_run1.txt")[:,1]

off = [(x[i]+x[25+i])/2 for i in range(26)]

print(np.mean(off))

ax = plt.subplot(111)
ax.plot(t, off, '.')
ax.grid(True)

plt.xticks(t)
plt.xlabel('starting angle (degrees)')
plt.ylabel('offset (nT)')

plt.show()

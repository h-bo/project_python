# -*-coding:utf-8-*-
import ch
import data2matrix as d2m
import numpy as np
import dict_op
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ch.set_ch() # matplotlib Chinese

data = d2m.data2matrix('data.txt', '\t')
data[:, 0] *= 2

out = [1, 3, 8]  # the out points index count from 1
out = [i - 1 for i in out]

dists = {}
N, D = data.shape
inlist = []
for i in range(N):
    if i not in out:
        inlist.append(i)
for i in inlist:
    for j in inlist:
        dists[(i, j)] = np.sqrt(np.sum((data[i] - data[j]) ** 2))
sortlist = dict_op.sort_dict_by_value(dists)
i, j = sortlist[0]
circle_centre = (data[i] + data[j]) / 2
circle_radius = dists[(i, j)] / 2
print 'circle_centre = ', circle_centre
print 'circle_radius = %f' % circle_radius

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
marker = [
    '去离子水',
    '乙二醇',
    '无水乙醇',
    '二乙二醇',
    '乙醇胺',
    'DMF',
    'NMP',
    '甲基异丁基甲酮'
]
c = ['b', 'c', 'g', 'k', 'm', 'r', 'w', 'y']

for i in range(N):
    ax.scatter(data[i, 0], data[i, 1], data[i, 2], c=c[i])
# ax.legend(marker, loc=5)

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

x = circle_radius * np.outer(np.cos(u), np.sin(v))
y = circle_radius * np.outer(np.sin(u), np.sin(v))
z = circle_radius * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x + circle_centre[0], y + circle_centre[1], z + circle_centre[2], rstride=4, cstride=4, color='w', alpha=0.2)

plt.show()
print 'OK'
print 'OK'

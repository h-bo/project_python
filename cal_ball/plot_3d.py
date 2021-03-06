import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Axes3D.scatter(xs, ys, zs=0, zdir='z', s=20, c='b', depthshade=True, *args, **kwargs)

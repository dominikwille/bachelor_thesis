import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

point = np.array([0, 0, -1])
normal = np.array([0, 0, 1])

# a plane is a*x+b*y+c*z+d=0
# [a,b,c] is the normal. Thus, we have to calculate
# d and we're set
d = -point.dot(normal)

# create x,y
x1, y1 = np.meshgrid(np.arange(-2, 2, 0.2), np.arange(-2, 2, 0.2))
x2, y2 = np.meshgrid(np.arange(-2, 2, 0.2), np.arange(-2, 2, 0.2))

# calculate corresponding z
z1 = -1
z2 = 1

def ball(x0,y0,z0, r=0.1):
    u = np.r_[0:2*np.pi:100j]
    # v is an array from 0 to 2*pi, with 100 elements
    v = np.r_[0:np.pi:100j]
    # x, y, and z are the coordinates of the points for plotting
    # each is arranged in a 100x100 array
    x = r*np.outer(np.cos(u), np.sin(v)) + x0
    y = r*np.outer(np.sin(u), np.sin(v)) + y0
    z = r*np.outer(np.ones(np.size(u)), np.cos(v)) + z0

    return x, y, z

pos1 = ball(-1.5, 0, 0.9)
pos2 = ball(-1.0, 0, 0.9)
pos3 = ball(-0.7, -0.8, 0.1)
pos4 = ball(-0.4, -1.3, -0.9)
pos5 = ball(0.1, -1.3, -0.9)
pos6 = ball(0.3, 0.0, -0.2)
pos7 = ball(0.7, 0.8, 0.2)
pos8 = ball(1.0, 0.4, -0.3)
pos9 = ball(1.2, 0.5, -0.9)

fig=plt.figure()
ax = Axes3D(fig)
ax.plot_surface(*pos1, color="#FF8888", linewidth=0, antialiased=True, zorder=4)
ax.plot_surface(*pos2, color="#FF7777", linewidth=0, antialiased=True, zorder=4)
ax.plot_surface(*pos3, color="#FF6666", linewidth=0, antialiased=True, zorder=4)
ax.plot_surface(*pos4, color="#FF5555", linewidth=0, antialiased=True, zorder=4)
ax.plot_surface(*pos5, color="#FF4444", linewidth=0, antialiased=True, zorder=4)
ax.plot_surface(*pos6, color="#FF3333", linewidth=0, antialiased=True, zorder=4)
ax.plot_surface(*pos7, color="#FF2222", linewidth=0, antialiased=True, zorder=4)
ax.plot_surface(*pos8, color="#FF1111", linewidth=0, antialiased=True, zorder=4)
ax.plot_surface(*pos9, color="#FF0000", linewidth=0, antialiased=True, zorder=4)
ax.plot_wireframe(x2,y2,z2, color="blue", antialiased=True, zorder=-100)
ax.plot_wireframe(x1,y1,z1, color="blue", antialiased=True, zorder=-100)
ax.add_artist(Arrow3D([-1.5, -1.0], [0, 0], [0.9, 0.9], color="#88FF88", mutation_scale=20, lw=3, arrowstyle="-|>"))
ax.add_artist(Arrow3D([-1.0, -0.7], [0, -0.8], [0.9, 0.1], color="#66FF66", mutation_scale=20, lw=3, arrowstyle="-|>"))
ax.add_artist(Arrow3D([-0.7, -0.4], [-0.8, -1.3], [0.1, -0.9], color="#66FF66", mutation_scale=20, lw=3, arrowstyle="-|>"))
ax.add_artist(Arrow3D([-0.4, 0.1], [-1.3, -1.3], [-0.9, -0.9], color="#66FF66", mutation_scale=20, lw=3, arrowstyle="-|>"))
ax.add_artist(Arrow3D([0.1, 0.3], [-1.3, 0.0], [-0.9, -0.2], color="#66FF66", mutation_scale=20, lw=3, arrowstyle="-|>"))
ax.add_artist(Arrow3D([0.3, 0.7], [0.0, 0.8], [-0.2, 0.2], color="#66FF66", mutation_scale=20, lw=3, arrowstyle="-|>"))
ax.add_artist(Arrow3D([0.7, 1.0], [0.8, 0.4], [0.2, -0.3], color="#44FF44", mutation_scale=20, lw=3, arrowstyle="-|>"))
ax.add_artist(Arrow3D([1.0, 1.2], [0.4, 0.5], [-0.3, -0.9], color="#22FF22", mutation_scale=20, lw=3, arrowstyle="-|>"))
ax.add_artist(Arrow3D([1.2, 2.0], [0.5, 0.5], [-0.9, -0.9], color="#00FF00", mutation_scale=20, lw=3, arrowstyle="-|>"))
# ax.set_xlabel('$t$')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
ax.set_zlim([-1.1, 1.1])
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
plt.axis('off')
plt.show()
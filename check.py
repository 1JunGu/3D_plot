import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 创建一个新的图形和三维坐标轴
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)
ax.set_zlim(0, 0.5)

# 创建一些三维数据
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
z = X + Y

# 将数据转换为网格
Z = z

# 绘制三维散点图
# ax.scatter(X, Y, Z)

# 设置坐标轴标签
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")
ax.set_zlabel("Z Label")

# 显示图形
plt.savefig("check_3d.png", dpi=300, bbox_inches="tight")

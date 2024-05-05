import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

# Load the 2D image generated by NCL
image_path = "./ncl.png"
image = Image.open(image_path)

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

# Create a meshgrid for the 3D surface
x, y = np.meshgrid(np.linspace(0, image.width, 100), np.linspace(0, image.height, 100))

# Create a 3D surface by applying a transformation to the 2D image
#z = np.sin(x * 0.05) * np.cos(y * 0.05) * 10
z = np.zeros_like(x)

# Plot the 3D surface with the 2D image as texture
ax.plot_surface(x, y, z, facecolors=plt.cm.viridis(z), rstride=1, cstride=1, linewidth=0, antialiased=False)

# Set the 3D plot limits and labels
ax.set_xlim(0, image.width)
ax.set_ylim(0, image.height)
ax.set_zlim(np.min(z), np.max(z))
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# Adjust the camera view
ax.view_init(elev=20, azim=45)

# Display the plot
plt.tight_layout()
plt.savefig("from_ncl.png", dpi=300)
import itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
import numpy as np
import cartopy.feature
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times"]})
plt.rcParams["axes.unicode_minus"] = False  # 负号

fig = plt.figure(figsize=(10, 8), dpi=200)
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(90, 160)
ax.set_ylim(-5, 40)
ax.set_zlim(0, 0.5)
##############################################################
concat = lambda iterable: list(itertools.chain.from_iterable(iterable))
target_projection = ccrs.PlateCarree()
# 目标投影，这里用最常见的一种
feature = cartopy.feature.NaturalEarthFeature("physical", "land", "110m")
geoms = feature.geometries()
geoms = [target_projection.project_geometry(geom, feature.crs) for geom in geoms]
paths = concat(geos_to_path(geom) for geom in geoms)  # geom转path
polys = concat(path.to_polygons() for path in paths)  # path转poly
lc = PolyCollection(polys, edgecolor="black", facecolor="yellow", closed=False)
ax.add_collection3d(lc)
ax.set_xlabel("longtitude")
ax.set_ylabel("latitude")
ax.set_zlabel("Height")
plt.savefig("test2.png", dpi = 300, bbox_inches = "tight", pad_inches = 0.5)

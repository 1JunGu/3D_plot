import cartopy.crs as ccrs
import cartopy.feature
from cartopy.mpl.patch import geos_to_path

import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.collections import PolyCollection
import numpy as np


def f(x,y):
    x, y = np.meshgrid(x, y)
    return (1 - x / 2 + x**5 + y**3 + x*y**2) * np.exp(-x**2 -y**2)

nx, ny = 256, 512
X = np.linspace(90, 160, nx)
Y = np.linspace(-5, 40, ny)
Z = f(np.linspace(-3, 3, nx), np.linspace(-3, 3, ny))


fig = plt.figure()
ax3d = fig.add_axes([0, 0, 1, 1], projection='3d')
#get the default view and change the elevation and azimuth
elev, azim, roll = ax3d.elev, ax3d.azim, ax3d.roll
print(elev, azim, roll)
ax3d.view_init(elev=35, azim=-55, roll=0)

# Make an axes that we can use for mapping the data in 2d.
proj_ax = plt.figure().add_axes([0, 0, 1, 1], projection=ccrs.Mercator())#, xlim=[90, 160], ylim=[-5, 40])
proj_ax.set_extent([95, 145, -5, 40], crs=ccrs.PlateCarree())
#cs = proj_ax.contourf(X, Y, Z, transform=ccrs.PlateCarree(), alpha=0.4)


#for zlev, collection in zip(cs.levels, cs.collections):
#    paths = collection.get_paths()
#    # Figure out the matplotlib transform to take us from the X, Y coordinates
#    # to the projection coordinates.
#    trans_to_proj = collection.get_transform() - proj_ax.transData
#
#    paths = [trans_to_proj.transform_path(path) for path in paths]
#    verts3d = [np.concatenate([path.vertices,
#                               np.tile(zlev, [path.vertices.shape[0], 1])],
#                              axis=1)
#               for path in paths]
#    codes = [path.codes for path in paths]
#    pc = Poly3DCollection([])
#    pc.set_verts_and_codes(verts3d, codes)
#
#    # Copy all of the parameters from the contour (like colors) manually.
#    # Ideally we would use update_from, but that also copies things like
#    # the transform, and messes up the 3d plot.
#    pc.set_facecolor(collection.get_facecolor())
#    pc.set_edgecolor(collection.get_edgecolor())
#    pc.set_alpha(collection.get_alpha())
#
#    ax3d.add_collection3d(pc)

proj_ax.autoscale_view()

ax3d.set_xlim(*proj_ax.get_xlim())
ax3d.set_ylim(*proj_ax.get_ylim())
ax3d.set_zlim(Z.min(), Z.max())


# Now add coastlines.
concat = lambda iterable: list(itertools.chain.from_iterable(iterable))

target_projection = proj_ax.projection

feature = cartopy.feature.NaturalEarthFeature('physical', 'land', '110m')
geoms = feature.geometries()

# Use the convenience (private) method to get the extent as a shapely geometry.
boundary = proj_ax._get_extent_geom()

# Transform the geometries from PlateCarree into the desired projection.
geoms = [target_projection.project_geometry(geom, feature.crs)
         for geom in geoms]
# Clip the geometries based on the extent of the map (because mpl3d can't do it for us)
geoms2 = []
for i in range(len(geoms)):
    if geoms[i].is_valid:
        geoms2.append(geoms[i])
geoms = geoms2
geoms = [boundary.intersection(geom) for geom in geoms]

# Convert the geometries to paths so we can use them in matplotlib.
paths = concat(geos_to_path(geom) for geom in geoms)
polys = concat(path.to_polygons() for path in paths)
lc = PolyCollection(polys, edgecolor='red',
                    facecolor='yellow', closed=True)
ax3d.add_collection3d(lc, zs=ax3d.get_zlim()[0])

plt.close(proj_ax.figure)
plt.savefig("tmp.png", dpi=300, bbox_inches="tight")
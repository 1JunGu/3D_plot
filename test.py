import sys
import itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.textpath import TextPath
from matplotlib.transforms import Affine2D
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from mpl_toolkits.mplot3d import art3d
import numpy as np
import cartopy.feature
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter

def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, **kwargs):
    x, y, z = xyz
    if zdir == "y":
        xy1, z1 = (x, z), y
    elif zdir == "x":
        xy1, z1 = (y, z), x
    else:
        xy1, z1 = (x, y), z

    text_path = TextPath((0, 0), s, size=size, usetex=usetex)
    trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])

    p1 = PathPatch(trans.transform_path(text_path), **kwargs)
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)


plt.rcParams.update({"font.family": "serif", "font.serif": ["Times"]})
plt.rcParams["axes.unicode_minus"] = False  # 负号

fig = plt.figure(figsize=(10, 8))

ax3d = fig.add_axes([0, 0, 1, 1], projection="3d")
##get the default view and change the elevation and azimuth
#elev, azim, roll = ax3d.elev, ax3d.azim, ax3d.roll
#print(elev, azim, roll)

ax3d.view_init(elev=30, azim=-55, roll=0) #change the view of 3d plot

# Make an axes that we can use for mapping the data in 2d.
proj_ax = plt.figure().add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree())#, xlim=[90, 160], ylim=[-5, 40])
proj_ax.set_extent([95, 145, -5, 40], crs=ccrs.PlateCarree())
proj_ax.set_xticks( np.arange(100, 150, 10), crs=ccrs.PlateCarree())
proj_ax.set_yticks( np.arange(0,40,5), crs=ccrs.PlateCarree())

ax3d.set_xlim(*proj_ax.get_xlim())
ax3d.set_ylim(*proj_ax.get_ylim())
ax3d.set_zlim(0, 0.5)

concat = lambda iterable: list(itertools.chain.from_iterable(iterable))

target_projection = proj_ax.projection

feature = cartopy.feature.NaturalEarthFeature("physical", "land", "50m")
geoms = feature.geometries()

# Use the convenience (private) method to get the extent as a shapely geometry.
boundary = proj_ax._get_extent_geom()
# Transform the geometries from PlateCarree into the desired projection.
geoms = [target_projection.project_geometry(geom, feature.crs) for geom in geoms]
geoms2 = []
for i in range(len(geoms)):
    if geoms[i].is_valid:
        geoms2.append(geoms[i])
geoms = geoms2
geoms = [boundary.intersection(geom) for geom in geoms]
# Clip the geometries based on the extent of the map (because mpl3d can't do it for us)
paths = concat(geos_to_path(geom) for geom in geoms)
polys = concat(path.to_polygons() for path in paths)
lc = PolyCollection(polys, edgecolor="black", facecolor="#d1af87", closed=False, linewidths=0.5)

#ax3d.spines['geo'].set_visible(False) 
ax3d.add_collection3d(lc, zs=0)

#ax3d.set_xlabel("longtitude")
#ax3d.set_ylabel("latitude")
#ax3d.set_zlabel("Height")

# beautify the imgae
ax3d.grid(False)  # remove the gridlines
ax3d.xaxis.pane.fill=False #remove the x axis pane
ax3d.yaxis.pane.fill=False #remove the x axis pane
ax3d.zaxis.pane.fill="tan" #remove the x axis pane
#remove the edge color of the pane
ax3d.xaxis.pane.set_edgecolor('none')
ax3d.yaxis.pane.set_edgecolor('none')
ax3d.zaxis.pane.set_edgecolor('none')

#set the ticks inward&outward length
ax3d.xaxis._axinfo['tick']['outward_factor']=0
ax3d.xaxis._axinfo['tick']['inward_factor']=0.25
ax3d.yaxis._axinfo['tick']['outward_factor']=0
ax3d.yaxis._axinfo['tick']['inward_factor']=0.25
ax3d.zaxis._axinfo['tick']['outward_factor']=0
ax3d.zaxis._axinfo['tick']['inward_factor']=0.25

ax3d.xaxis.set_major_formatter(LongitudeFormatter())
ax3d.yaxis.set_major_formatter(LatitudeFormatter())

#get the bottom zorder of the 3d plot
bottom = ax3d.get_zlim()[0]
#ax3d.text3D(105, -8, bottom, "Longitude, 3D", rotation = "vertical",zdir="z", size=10, c="k")
text3d(ax3d, (115,-12, bottom),'Longitude', zdir="z",size=2,usetex=False,ec="none", fc="k")
text3d(ax3d, (155,10,bottom),'Latitude', zdir="z",size=2,angle=np.pi*0.5,usetex=False, ec="none", fc="k")
text3d(ax3d, (137,42,bottom),'Surface', zdir="z",size=2,usetex=False, ec="none", fc="k")

for m in np.arange(100,150,10):
    text3d(ax3d, (m-2,-5-3,bottom), "{}".format(m)+'°E', zdir="z",size=2,usetex=False,ec="none", fc="k")
    #add major tick lines for the longitude
    ax3d.plot([m,m],[-6,-5],[bottom,bottom],color='k',lw=1,zorder=5)
for n in np.arange(0,40,5):
    text3d(ax3d, (145+2,n,bottom), "{}".format(n)+'°N', zdir="z",size=2,usetex=False,ec="none", fc="k")
    #add major tick lines for the latitude
    ax3d.plot([145,146],[n,n],[bottom,bottom],color='k',lw=1,zorder=5)

#remove the default axis
ax3d.axis("off")
ax3d.plot([95,146],[-5,-5],[bottom,bottom],color='k',lw=1,zorder=5)
ax3d.plot([145,145],[-6,40],[bottom,bottom],color='k',lw=1,zorder=5)

plt.close(proj_ax.figure)
plt.savefig("test8.png", dpi = 600, bbox_inches = "tight", pad_inches = 0.3)
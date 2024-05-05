import itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
import numpy as np
import cartopy.feature as cf
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False#负号
fig = plt.figure(figsize=(10,8),dpi=200)
ax = Axes3D(fig, xlim=[70, 130], ylim=[-0, 70])
ax.set_zlim(0,0.5)
####################预先设置地图的参数######################################
proj_ax=plt.figure().add_subplot(111,projection=ccrs.PlateCarree())
proj_ax.set_xlim(ax.get_xlim())#使地图投影获得当前3d投影一样的绘图范围
proj_ax.set_ylim(ax.get_ylim())
concat = lambda iterable: list(itertools.chain.from_iterable(iterable))
target_projection=proj_ax.projection
feature=cf.NaturalEarthFeature('physical', 'land', '50m')
geoms=feature.geometries()
boundary=proj_ax._get_extent_geom()
geoms = [target_projection.project_geometry(geom, feature.crs)
         for geom in geoms]
geoms2=[]
for i in range(len(geoms)):
    if geoms[i].is_valid:
        geoms2.append(geoms[i])
geoms=geoms2
geoms=[boundary.intersection(geom)for geom in geoms]
paths = concat(geos_to_path(geom) for geom in geoms)
polys = concat(path.to_polygons() for path in paths)
lc = PolyCollection(polys, edgecolor='black',
                    facecolor='yellow', closed=False)
ax.add_collection3d(lc)
proj_ax.spines['geo'].set_visible(False)#解除掉用于确定地图的子图
plt.savefig("check_Axes_3d.png", dpi=300, bbox_inches="tight")
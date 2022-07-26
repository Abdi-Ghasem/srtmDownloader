<div align="center">

# **Python library (multi-threaded) for retrieving SRTM elevation map of [CGIAR-CSI](https://srtm.csi.cgiar.org/).**

</div>

**This is a Python library (multi-threaded), named 'srtm', for retrieving SRTM elevation map of [CGIAR-CSI](https://srtm.csi.cgiar.org/). SRTM elevation map is retrieved by using of:** 

<div>

```python
# RETRIEVE SRTM DATA OVER AN AOI WITH RESPECT TO GEOID (ORTHOMETRIC HEIGHT)
import srtm

# Define the AOI
aoi = {'upper_left' : [48.07, -69.06], 
       'lower_right': [44.60, -63.77]}

# Retrieve, merge, and crop SRTM elevation map over the AOI
srtm.clip(aoi, save_path='/Users/ghasem.abdi/Desktop/nb_srtm.tif')
```

```python
# RETRIEVE SRTM DATA OF A POINT WITH RESPECT TO GEOID (ORTHOMETRIC HEIGHT)
import rasterio
from srtm import srtm

# Define the point
lat, lon = 45.95, -66.65

# Retrieve SRTM elevation map of the point
srtm.retrieve((srtm.which_tile(lat, lon), '/Users/ghasem.abdi/Desktop/'))

# Open SRTM elevation map of the point
ds = rasterio.open('/Users/ghasem.abdi/Desktop/srtm_23_03.tif')

# Extract orthometric height of the point 
orthometric_height = next(ds.sample([(lon, lat)]))[0]
```

```python
# (OPTIONAL): CONVERT THE ORTHOMETRIC HEIGHT TO ELLIPSOIDAL HEIGHT
import pyproj

# WGS84 with Gravity-related height (EGM96)
geoid = pyproj.CRS('EPSG:4326+5773')

# WGS84 with ellipsoid height as vertical axis
ellipsoid = pyproj.CRS.from_epsg(4979)

# Define a transformation from orthometric to ellipsoidal system
trf = pyproj.Transformer.from_crs(geoid, ellipsoid)

# Estimate the ellipsoidal height
ellipsoidal_height = trf.transform(lat, lon, orthometric_height)[-1]
```

</div>
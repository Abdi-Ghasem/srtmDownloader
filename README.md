<div align="center">

# **Python library (multi-threaded) for retrieving SRTM elevation map of [CGIAR-CSI](https://srtm.csi.cgiar.org/).**

</div>

**This is a Python library (multi-threaded), named 'srtm', for retrieving SRTM elevation map of [CGIAR-CSI](https://srtm.csi.cgiar.org/). SRTM elevation map is retrieved by using of:** 

<div>

```python
# RETRIEVE SRTM DATA OVER AN AOI
import srtm

# Define the AOI
aoi = {'upper_left' : [48.07, -69.06], 
       'lower_right': [44.60, -63.77]}

# Retrieve, merge, and crop SRTM elevation map over the AOI
srtm.clip(aoi, save_path='/Users/ghasem.abdi/Desktop/nb_srtm.tif')
```

```python
# RETRIEVE SRTM DATA OF A POINT
from srtm import srtm

# Define the point
lat, lon = 46.335, -66.415

# Retrieve SRTM elevation map of the above coordinate
srtm.retrieve((srtm.which_tile(lat, lon), '/Users/ghasem.abdi/Desktop/'))
```
</div>
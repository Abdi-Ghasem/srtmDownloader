<div align="center">

# **Python library (multi-threaded) for retrieving SRTM elevation map of [CGIAR-CSI](https://srtm.csi.cgiar.org/).**

</div>

**This is a Python library (multi-threaded), named 'srtm', for retrieving SRTM elevation map of [CGIAR-CSI](https://srtm.csi.cgiar.org/). SRTM elevation map is retrieved by using of:** 

<div>

```python
import srtm

# Define an AOI
aoi = {'upper_left' : [48.07, -69.06], 
       'lower_right': [44.60, -63.77]}

# Retrieve, merge, and crop SRTM elevation map over the AOI
srtm.clip(aoi, save_path='/Users/ghasem.abdi/Desktop/nb_srtm.tif')
```

</div>
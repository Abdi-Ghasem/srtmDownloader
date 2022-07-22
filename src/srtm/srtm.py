# Original Author       : Ghasem Abdi, ghasem.abdi@yahoo.com
# File Last Update Date : July 22, 2022

# Import dependencies
import os
import glob
import shutil
import rasterio
import numpy as np
import urllib.request
import concurrent.futures
from rasterio.merge import merge

# Define the base url for retrieving SRTM data
url = 'https://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/'

# Define custom functions
def which_tile(lat, long):
    '''Find SRTM tile number.
    Parameters
    ----------
    lat : float
        latitude.
    long : float
        longitude.
    Returns
    -------
    xy : tuple
        SRTM tile number.
    '''
    return (180 + np.floor(long).astype(int)) // 5 + 1, (64 - np.floor(lat).astype(int)) // 5

def which_tiles(ul, lr):
    '''Find SRTM tile numbers in an AOI.
    Parameters
    ----------
    ul : list
        [lat, long] of upper left.
    lr : list
        [lat, long] of lower right.
    Returns
    -------
    xy : list
        SRTM tile numbers.
    '''
    # Find SRTM tile number for an AOI's upper left and lower right
    (xmin, ymin), (xmax, ymax) = which_tile(ul[0], ul[1]), which_tile(lr[0], lr[1])
    
    # Make a list of SRTM tile numbers in the AOI
    x, y = np.meshgrid(range(xmin, xmax + 1), range(ymin, ymax + 1))
    xy = np.stack((x.flatten(), y.flatten()), axis=1)
    return xy.tolist()

def retrieve(xyp):
    '''Retrieve SRTM data over a tile.
    Parameters
    ----------
    xyp : list
        SRTM tile number and save_path.
    Returns
    -------
    xy : string
        SRTM tile filename.
    '''
    ((x, y), path) = xyp
    
    try:
        # Retrieve SRTM tile and save it
        urllib.request.urlretrieve(url+f'srtm_{x:02d}_{y:02d}.zip', \
            path+f'srtm_{x:02d}_{y:02d}.zip')
        
        # Unpack the downloaded zipfile into a folder
        shutil.unpack_archive(path+f'srtm_{x:02d}_{y:02d}.zip', \
            path+f'srtm_{x:02d}_{y:02d}')
        
        # Remove the downloaded zipfile
        os.remove(path+f'srtm_{x:02d}_{y:02d}.zip')
        
        # Move the tile tif to the base root
        shutil.move(path+f'srtm_{x:02d}_{y:02d}/'+f'srtm_{x:02d}_{y:02d}.tif', \
            path+f'srtm_{x:02d}_{y:02d}.tif')
        
        # Remove the unpacked folder
        shutil.rmtree(path+f'srtm_{x:02d}_{y:02d}')
        
    except:
        pass
    
def clip(aoi, save_path='srtm.tif'):
    '''Retrieve SRTM data over an AOI.
    Parameters
    ----------
    aoi : dict
        upper left and lower right of an AOI.
    save_path: string
        the path where the SRTM data should be stored.
    Returns
    -------
    None
    '''
    # Create a tmp folder for srtm processing
    save_path = os.path.abspath(save_path)
    srtm_tmp = os.path.dirname(save_path)+'/srtm_tmp/'
    os.makedirs(srtm_tmp, exist_ok=True)
    
    ul, lr = aoi['upper_left'], aoi['lower_right']
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Retrieve SRTM tiles of an AOI (multi-threaded)
        executor.map(retrieve, ((xy, srtm_tmp) for xy in which_tiles(ul, lr)))
        
    # Merge the SRTM tiles into a single file followed by cropping over the AOI
    datasets = []
    for filename in glob.glob(srtm_tmp+'*.tif'): datasets.append(rasterio.open(filename)) 
    merge(datasets, bounds=(ul[1], lr[0], lr[1], ul[0]), nodata=-32768, dst_path=save_path)
    
    # Remove the tmp folder
    shutil.rmtree(srtm_tmp)
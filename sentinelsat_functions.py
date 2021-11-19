import os
import shutil
from zipfile import ZipFile
from datetime import datetime
from collections import OrderedDict

from sentinelsat import SentinelAPI
import matplotlib.pyplot as plt
import rasterio
import rasterio.plot
import geopandas
from matplotlib_scalebar.scalebar import ScaleBar
from pyproj import Transformer
import numpy as np

from rasterio.windows import Window
from rasterio.transform import TransformMethodsMixin

from sentinelsat_glacier_definitions import glacier_definitions


def delete_everything_in_directory(download_directory):
    """
    Deletes all files and directories in download_directory
    This action cannot be undone, so use with care!

    Created by oew@geus.dk
    3 Feb 2021
    """
    for filename in os.listdir(download_directory):
        file_path = os.path.join(download_directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete {}. Reason: {}'.format(file_path, e))


def unzip_images(download_directory, image_directory, image_type):
    """
    Unzips images in download_directory, and extracts images of image_type to image_directory
    download_directory:
    image_directory:
    image_type: string containing the type of image demanded. Can be band-8 NIR ('B08.jp2') or true color image
    ('TCI.jp2')

    Created by oew@geus.dk
    27 Jan 2021
    """

    zip_files = [file for file in os.listdir(download_directory) if file[-4:] == '.zip']
    for zip_file in zip_files:
        filePath = os.path.join(download_directory, zip_file)
        with ZipFile(filePath, 'r') as zipObject:
            listOfFileNames = zipObject.namelist()
            for fileName in listOfFileNames:
                if fileName.endswith(image_type):
                    zipObject.extract(fileName, download_directory)

    # Move images from subdirectories to image_directory
    for root, dirs, files in os.walk(download_directory):
        for file in [f for f in files if f.endswith(image_type)]:
            shutil.move(os.path.join(root, file), os.path.join(image_directory, file))

    # Delete zip-files and unzipped folders
    for file in os.listdir(download_directory):
        if file.endswith('.zip'):
            os.remove(os.path.join(download_directory, file))
        elif file.endswith('.DS_Store'):
            os.remove(os.path.join(download_directory, file))
        else:
            shutil.rmtree(os.path.join(download_directory, file))


def make_image(glacier, n, image_list, output_directory, date):
    """
    Makes the image of glacier, using the images in image_list, bounded in the appropriate UTM coordinates by minx, maxx, miny and maxy. Writes date in the bottom, and adds a 10km scalebar.

    Glacier: string containing glacier name
    n: integer (1-10) for RGB composition. band = band^(1/n)
    image_list: list of relative paths to .jp2 images
    date: str formatted  "YYYYMMDDTHHMMSS". ex "20200115T230203"

    Created by oew@geus.dk
    27 Jan 2021

    Last modified by oew@geus.dk
    7 Apr 2021
    """

    
    fig, ax = plt.subplots(figsize=(12, 10))

    #%% Get projection and extent of image
    crs_image = rasterio.open(image_list[0]) # Loaded just for crs
    to_crs = crs_image.crs.data["init"] # Get the projection and use for bounds

    transformer = Transformer.from_crs("epsg:4326", to_crs) # Function to transform lat-lon limits to appropriate projection
    bounding_box = glacier_definitions(glacier, 'bounding_box')
    minx, miny = transformer.transform(bounding_box[1], bounding_box[0]) # Transform limits to image projection
    maxx, maxy = transformer.transform(bounding_box[3], bounding_box[2]) # Transform limits to image projection

    #%% Plot each tile individually.
    tiles = list(set([i[-30:-24] for i in image_list]))
    for i, tile in enumerate(tiles):
        # Get images for this specific tile
        tile_image_list = [i for i in image_list if i[-30:-24].endswith(tile)]
        tile_image_list.sort()

        # Get the appropriate color bands
        blue = rasterio.open(tile_image_list[0], 'r')
        green = rasterio.open(tile_image_list[1], 'r')
        red = rasterio.open(tile_image_list[2], 'r')

        # Make a window to reduce memory use. This way only the relevant part of each tile is read.
        minrow, mincol = TransformMethodsMixin.index(blue, minx, maxy)
        maxrow, maxcol = TransformMethodsMixin.index(blue, maxx, miny)
        window = Window.from_slices((max(0, minrow), max(0, maxrow)), (max(0, mincol), max(0, maxcol)))

        # Take the n'th root of each band
        tci = np.vstack((red.read(window=window), green.read(window=window), blue.read(window=window)))**(1/n)
        # Make sure normalization is the same for all tiles in scene
        if i == 0:
            norm_min = tci.min(axis=(0,1,2), keepdims=True) # axis=(0,1,2) uses min and max of whole image
            norm_max = tci.max(axis=(0,1,2), keepdims=True) # axis=(1,2) normalizes each channel independently
        # Shift and stretch bands to be in [0,1]
        tci = tci - norm_min
        tci = tci/norm_max

        # Plot with rasterio, using the transform of the raster
        rasterio.plot.show(tci, transform=blue.window_transform(window), ax=ax)

    #%% Reproject and ice extents
    cflPath1980 = './prom_total_man_corr_v2b.shp'
    cfl1980 = geopandas.read_file(cflPath1980)
    cfl1980 = cfl1980.to_crs(to_crs)
    cfl1980.boundary.plot(ax=ax, color='red', alpha=1, linewidth=1, label='1980')

    # cflPath2000 = './cfl/gimp_total_diss_id_v2.shp'
    # cfl2000 = geopandas.read_file(cflPath2000)
    # cfl2000 = cfl2000.to_crs(to_crs)
    # cfl2000.boundary.plot(ax=ax, color='blue', alpha=1, linewidth=1, label='2000')

    # Set limits and format ticklabels
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    ax.axis('off')

    # Add legend
    ax.legend(loc='upper left', title='Ice extent', fancybox=False, framealpha=0.8, edgecolor='black')

    ## Add scalebar 
    scale_displace = (maxy-miny) * 0.035
    scaleBar = ScaleBar(dx=1, units='m', frameon=True, box_alpha=0.8, fixed_value=10, fixed_units='km', box_color='white', border_pad=1, location='upper right')
    plt.gca().add_artist(scaleBar)

    ## Add date
    datetimeObject = datetime.strptime(date[0:8], '%Y%m%d')
    dateString = datetimeObject.strftime("%d %B %Y")
    date_plot = plt.text(minx + scale_displace, miny+scale_displace, '{} glacier, {}'.format(glacier, dateString), fontsize=16)
    date_plot.set_bbox(dict(facecolor='white', alpha=0.8))

    # Save figure (4 figs, 2 sizes and 2 languages. For now both languages use english) and close to clear memory
    outlet_number = glacier_definitions(glacier, 'outlet_number')
    filename = '{}/Outlet_{}_LA_EN_{}'.format(output_directory, outlet_number, date[:6])
    filename_SM = '{}/Outlet_{}_SM_EN_{}'.format(output_directory, outlet_number, date[:6])
    fig.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    fig.savefig(filename_SM, dpi=100, bbox_inches='tight', pad_inches=0)
    filename = '{}/Outlet_{}_LA_DK_{}'.format(output_directory, outlet_number, date[:6])
    filename_SM = '{}/Outlet_{}_SM_DK_{}'.format(output_directory, outlet_number, date[:6])
    fig.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    fig.savefig(filename_SM, dpi=100, bbox_inches='tight', pad_inches=0)
    
    plt.close()

    del ax, fig, tci # Clear some memory. Not sure if necessary, but it solved run issues on my computer


def sentinel_process(glacier, from_date, to_date, download_directory, unprocessed_image_directory, processed_image_directory, image_type, n, max_cloud_percentage, download=True):
    """
    Function to download, unzip and process the downloaded Sentinel images into calving front area cutouts with overlay for the glacier

    glacier: string containing glacier name as defined in sentinelsat_glacier_definitions.py
    from_date: string containing the from-date to download from. Formatted 'YYYYMMDD'
    to_date: string containing the to-date to download from. Formatted 'YYYYMMDD'
    download_directory: string containing the directory for downloaded .zip-files to be places
    unprocessed_image_directory: string containing the directory where the extracted tile-size Sentinel images will be placed
    processed_image_directory: string containing the directory where the processed calving front region images will be placed
    image_type: string containing the used band in the Sentinel download. Can be bands 'B01' through 'B12' or 'TCI' (true-color image)
    download: bool to control whether or not the images should be downloaded. If downloaded, all images in the directory unprocessed_image_directory will be deleted. Allows for code development of image processing with already downloaded images, without having to download again. Defaults to True.

    BE AWARE: everything in the unprocessed_image_directory and download_directory will be routinely deleted, and cannot be recovered to my knowledge.

    Created by oew@geus.dk
    3 Feb 2021

    Last modified by oew@geus.dk
    24 Mar 2021

    """

    if download: # Makes it possible to process without downloading
        download_sentinel(glacier, from_date, to_date, download_directory, unprocessed_image_directory, max_cloud_percentage)

        ## Unzip downloaded files, get image, delete the rest of the sentinel zip-contents
        unzip_images(download_directory, unprocessed_image_directory, image_type)

    ## Make image from each set of tiles from same time
    # Get all image files
    imageList = [i for i in os.listdir(unprocessed_image_directory) if i.endswith('jp2')] 

    # Get all unique dates by transforming list to set
    uniqueDates = set([i[7:22] for i in imageList]) 
    print('Processing images for {}'.format(glacier))

    # Run the function for each set of images from same glacier with the same timestamp
    for uniqueDate in uniqueDates: 
        # Get list of all images
        image_list_all = [os.path.join(unprocessed_image_directory, image) for image in imageList if image[7:22] == uniqueDate] 
        # Get relative orbits for this glacier
        relorbs = glacier_definitions(glacier, 'tile_relorb_dict')
        relorbsList = list(relorbs)
        image_list = []
        # Make list of images for this glacier
        for relorbi in relorbsList:
            image_list += [i for i in image_list_all if i.startswith('{}/T{}'.format(unprocessed_image_directory, relorbi))]
        if image_list:
            make_image(glacier, n, image_list, processed_image_directory, uniqueDate)
    print('Finished processing images for {}'.format(glacier))


def download_sentinel(glacier, from_date, to_date, download_directory, unprocessed_image_directory, max_cloud_percentage):
    """
    Downloads Sentinel 2 images from glacier during from_date to to_date to download_directory
    glacier: string containing the glacier name
    from_date: string formatted 'YYYYMMDD' or 'NOW' or 'NOW-kDAYS' where k is integer
    to_date: same as above
    unprocessed_image_directory: string containing the directory of unprocessed images (for clearing it)
    download_directory: string containing the target directory to place downloads.
    max_cloud_percentage: integer

    Created by oew@geus.dk
    27 Jan 2021

    Last modified by oew@geus.dk
    10 Feb 2021
    """

    # User credentials to the Copernicus SciHub
    with open('../username_password.txt', 'r') as file:
        data = file.readlines()
        data = [d.replace('\n', '') for d in data]
    USERNAME = data[0]
    PASSWORD = data[1]
    api = SentinelAPI(USERNAME, PASSWORD, 'https://apihub.copernicus.eu/apihub/')
    print('Downloading images for {}'.format(glacier))
    delete_everything_in_directory(download_directory)
    #delete_everything_in_directory(unprocessed_image_directory)

    # Dictionary containing Sentinel-2 Level1C Tile ID and relative orbit number(s)
    tile_relorb_dict = glacier_definitions(glacier, 'tile_relorb_dict')

    # Specify attributes
    query_kwargs = {
                    'platformname': 'Sentinel-2',
                    'producttype': 'S2MSI1C',
                    'date': (from_date, to_date), 
                    'cloudcoverpercentage': (0, max_cloud_percentage)
    }

    # Collect products
    # num_products = 0
    # products = OrderedDict()
    # for tile, rel_orbit in tile_relorb_dict.items():
    #   connection = True
    #   for orb in rel_orbit:
    #     kw = query_kwargs.copy()
    #     kw['tileid'] = tile
    #     kw['relativeorbitnumber'] = orb
    #     try: 
    #       pp = api.query(**kw)
    #     except api_error: # SciHub servers are known to have outages due to high demand, try again later. TODO: find the appropriate exception for HTTP 500 errors
    #       print("Cannot connect to server.")
    #       connection = False
    #       break
    #     products.update(pp)
    #     num_products += api.count(**kw)
    #   if not connection:
    #     break

    num_products = 0
    products = OrderedDict()
    for tile, rel_orbit in tile_relorb_dict.items():
        for orb in rel_orbit:
            kw = query_kwargs.copy()
            kw['tileid'] = tile
            kw['relativeorbitnumber'] = orb
            pp = api.query(**kw)
            products.update(pp)
            num_products += api.count(**kw)


    if num_products == 0:
        print("No products matches for {}".format(glacier))
    else:
        print("Number of products: {}" .format(num_products))
        # Download collected products
        api.download_all(products, download_directory)
        print("Finished downloading {} products for {}".format(num_products, glacier))

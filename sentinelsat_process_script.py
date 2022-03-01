from sentinelsat_functions import sentinel_process
from sentinelsat_ftp import sentinelsat_ftp_upload
"""
Script to call the download and processing of images to make calving front images for Polarportal.

Calls function sentinel_process in sentinelsat_functions.py. This file also contains all other functions required for processing EXCEPT for the function glacier_definitions in sentinalsat_glacier_definitions.py.

Variables to specify:
from_date: string formatted 'YYYYMMDD' or 'NOW' or 'NOW-kDAYS' where k is integer
to_date: same as above
download_directory: string containing the target directory to place downloads.
unprocessed_image_directory: string containing the directory of unprocessed images (for clearing it)
processed_image_directory: string containing the directory where the processed calving front region images will be placed
image_type: string containing the used band in the Sentinel download. Can be bands 'B01' through 'B12' or 'TCI' (true-color image)
max_cloud_percentage: integer. Only downloads images with set percentage of cloud cover as classified by ESA algorithm
download: bool to control whether or not the images should be downloaded. If downloaded, all images in the directory unprocessed_image_directory will be deleted. Allows for code development of image processing with already downloaded images, without having to download again. Defaults to True.
glacier_list: list of glaciers to download and process images for

Created by oew@geus.dk
3 Feb 2021

Last modified by oew@geus.dk
3 Mar 2021
"""

# Variables passed to function
from_date = 'NOW-2YEAR'
to_date = 	'NOW'
download_directory = './downloaded_files.nosync'
unprocessed_image_directory = './unprocessed_images.nosync'
processed_image_directory = './output_images_to_upload.nosync'
processed_image_uploaded_directory = './output_images_uploaded.nosync'
#image_type = 'TCI.jp2' # Truecolor images. Can also be any other band in the zip-file
image_type = ('B02.jp2', 'B03.jp2', 'B04.jp2') # New function makes RGB composites
n = 2 # root of each band in RGB-composite
max_cloud_percentage = 20
download = False;
upload = False;

glacier_list = [
'Ryder', 
'Petermann', 
'Humboldt', 
'Steenstrup', 
'Hayes', 
'Nunatakassaap Sermia', 
'Upernavik',
'Kangilleq',
'Store',
'Jakobshavn',
'Kangiata Nunaata Sermia',
'C. H. Ostenfeld',
'79 N',
'Zachariae',
'Storstrømmen',
'Daugaard-Jensen',
'Kangerlussuaq',
'Midgaard',
'Helheim',
'Ikertivaq'
]


glacier_list = ['Jakobshavn']
for glacier in glacier_list:
	sentinel_process(glacier, from_date, to_date, download_directory, unprocessed_image_directory, processed_image_directory, image_type, n, max_cloud_percentage, download)
print('Finished processing all glaciers from {} to {}'.format(from_date, to_date))

if upload:
	sentinelsat_ftp_upload(processed_image_directory, processed_image_uploaded_directory)




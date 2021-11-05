def glacier_definitions(glacier, output):
    """
    Returns either information for download of satellites images or bounding box for image
    glacier: string with name of one of the below implemented glaciers
    output: string with either "tile_relorb_dict" or "bounding_box" or "outlet_number"

    returns: depending on output
    tile_relorb_dictionary: dictionary containing Sentinel-2 Level1C Tile ID and relative orbit number(s)
     OR
    bounding_box: list in the format [minlon, maxlon, minlat, maxlat]
    outlet_number: outlet number for the glacier in question. For filename for DMI

    Tip for editing the bounding_box: uncomment lines in make_image with ax.set_yticks([]). This puts back ticks on the
    images, to give a reference for how the bounding_box can be edited to get the desired image.

    Created by oew@geus.dk
    1 Feb 2021

    Modified by oew@geus.dk
    3 Mar 2021
    """
    bounding_box = None
    tile_relorb_dict = None
    outlet_number = None

    if glacier == "Ryder":
        tile_relorb_dict = {
                            '22XDR': [114, 42, 28, 99, 27, 13],
                            '22XER': [114, 42, 28, 99, 27, 13],
                            '22XDS': [114, 42, 28, 99, 27, 13],
                            '22XES': [114, 42, 28, 99, 27, 13],
        }
        # bounding_box = [4.92e5, 5.28e5, 90.5e5, 91e5] UTM box
        outlet_number = 14
        bounding_box = [-51.5, 81.5, -49.5, 82]

    elif glacier == "Petermann":
        tile_relorb_dict = {
                            '20XNR': [114, 42, 28, 99, 85, 13],
                            '20XNQ': [114, 42, 28, 99, 85, 13],
                            '20XMR': [114, 42, 28, 99, 85, 13],
                            '20XMQ': [114, 42, 28, 99, 85, 13],
        }
        #bounding_box = [5.1e5, 5.6e5, 89.5e5, 90.2e5]
        outlet_number = 5
        bounding_box = [-63.2, 80.65, -59, 81.25,]

    elif glacier == "Humboldt":
        tile_relorb_dict = {
                            '20XMP': [113, 27, 13, 84, 70, 127],
        }
        # bounding_box = [4.45e5, 4.98e5, 88.4e5, 88.75e5]
        outlet_number = 9
        bounding_box = [-66, 79.6, -63, 79.95]

    elif glacier == "Steenstrup":
        tile_relorb_dict = {
                            '21XVD': [26, 126, 83],
        }
        # bounding_box = [4.4e5, 5e5, 83.3e5, 83.7e5]
        outlet_number = 12
        bounding_box = [-58.5, 75.07, -57, 75.4]

    elif glacier == "Hayes":
        tile_relorb_dict = {
                            '21XVD': [26, 126, 83],
                            '21XWD': [26, 126, 83],
        }
        # bounding_box = [4.8e5, 5.3e5, 82.9e5, 83.3e5]
        outlet_number = 13
        bounding_box = [-57.6, 74.8, -56.3, 75]

    elif glacier == "Nunatakassaap Sermia":
        tile_relorb_dict = {
                            '21XWC': [40, 140, 83],
        }
        # bounding_box = [5.05e5, 5.4e5, 82.75e5, 82.9e5]
        outlet_number = 20
        bounding_box = [-56.8, 74.55, -55.7, 74.7]

    elif glacier == "Upernavik":
        tile_relorb_dict = {
                            '21XWB': [40, 97, 140],
                            '21XWA': [40, 97, 140],
        }
        # bounding_box = [5.65e5, 6e5, 80.85e5, 81.15e5]
        outlet_number = 3
        bounding_box = [-55, 72.85, -53.8, 73.1]

    elif glacier == "Kangilleq":
        tile_relorb_dict = {
                            '22WED': [111, 68],
        }
        # bounding_box = [5.0e5, 5.23e5, 78.42e5, 78.65e5]
        outlet_number = 19
        bounding_box = [-51,  70.7, -50.4, 70.9]

    elif glacier == "Store":
        tile_relorb_dict = {
                            '22WED': [111, 68],
        }
        # bounding_box = [5.05e5, 5.33e5, 78e5, 78.2e5]
        outlet_number = 17
        bounding_box = [-50.9, 70.3, -50, 70.5]

    elif glacier == "Jakobshavn":
        tile_relorb_dict = {
                            '22WEB': [25, 68],
        }
        # bounding_box = [5.25e5, 5.64e5, 76.63e5, 76.87e5]
        outlet_number = 1
        bounding_box = [-50.2515, 69.0766, -49.3379, 69.2747]

    elif glacier == "Kangiata Nunaata Sermia":
        tile_relorb_dict = {
                            '22WES': [82, 125],
        }
        # bounding_box = [5.58e5, 5.84e5, 71.2e5, 71.42e5]
        outlet_number = 18
        bounding_box = [-49.74, 64.2, -49.3, 64.4]

    elif glacier == "C. H. Ostenfeld":
        tile_relorb_dict = {
                            '22XER': [114, 42, 28, 99, 27, 13],
        }
        # bounding_box = [5.62e5, 6.1e5, 90.4e5, 90.95e5]
        outlet_number = 15
        bounding_box = [-46.5, 81.4, -43.75, 81.90]

    elif glacier == "79 N":
        tile_relorb_dict = {
                            '27XWJ': [111, 25, 11, 68],
                            '27XVJ': [111, 25, 11, 68],
        }
        # bounding_box = [5e5, 5.6e5, 88e5, 88.8e5]
        outlet_number = 10
        bounding_box = [-22.5, 79.35, -18.5, 79.65] # From Karina
        bounding_box = [-21, 79.35, -18.5, 80.00] # Extended to include spalte

    elif glacier == "Zachariae":
        tile_relorb_dict = {
                            '27XWH': [39, 25, 68],
                            '27XVH': [39, 25, 68],
        }
        # bounding_box = [4.9e5, 5.6e5, 87.2e5, 87.9e5]
        outlet_number = 8
        bounding_box = [-21.385, 78.65, -18.862, 79.05]

    elif glacier == "Storstrømmen":
        tile_relorb_dict = {
                            '27XVF': [39, 139, 82, 125],
        }
        # bounding_box = [4.49e5, 4.75e5, 85e5, 85.4e5]
        outlet_number = 7
        bounding_box = [-23.6, 76.48, -21.8, 76.84]

    elif glacier == "Daugaard-Jensen":
        tile_relorb_dict = {
                            '26WME': [53, 10],
        }
        # bounding_box = [4.25e5, 4.6e5, 79.6e5, 79.9e5]
        outlet_number = 16
        bounding_box = [-29.3, 71.7, -28.0, 72]

    elif glacier == "Kangerlussuaq":
        tile_relorb_dict = {
                            '25WES': [10, 53],
                            '25WDS': [10, 53],
        }
        # bounding_box = [4.95e5, 5.25e5, 76.0e5, 76.15e5]
        outlet_number = 2
        bounding_box = [-33.3, 68.5, -32.3, 68.7]

    elif glacier == "Midgaard":
        tile_relorb_dict = {
                            '24WXU': [53, 96],
                            '24WWU': [53, 96],
        }
        # bounding_box = [5.9e5, 6.1e5, 73.6e5, 73.8e5]
        outlet_number = 6
        bounding_box = [-37.247,  66.265, -36.35, 66.56]

    elif glacier == "Helheim":
        tile_relorb_dict = {
                            '24WWU': [53, 96],
        }
        # bounding_box = [5.15e5, 5.55e5, 73.48e5, 73.75e5]
        outlet_number = 4
        bounding_box = [-37.247, 66.265, -36.35, 66.56]

    elif glacier == "Ikertivaq":
        tile_relorb_dict = {
                            '24WVT': [96, 139],
        }
        # bounding_box = [4.48e5, 4.9e5, 72.5e5, 72.92e5]
        outlet_number = 11
        bounding_box = [-40, 65.4, -39.2, 65.75]
    elif glacier == "Hagen":
        tile_relorb_dict = {
                            '26XMR': [69, 55, 41, 112],
        }

    else:
        print('{} not defined in glacier_definitions in file sentinel_glacier_definitions.py'.format(glacier))
        output = None

    if output is None:
        raise Exception('No glacier info returned.')
    elif output == 'tile_relorb_dict':
        return tile_relorb_dict
    elif output == 'bounding_box':
        return bounding_box
    elif output == 'outlet_number':
        return outlet_number

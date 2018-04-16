import pandas as pd
import os


def find_pending_fgdc_datasets(fgdc_folder, metadata_folder):
    """
    Check which datasets are missing new FGDC compliant metadata files.
    :return: 
    """

    fgdc_output = []
    pending = []
    for dirpath, subdir, files in os.walk(fgdc_folder):
        for f in files:
            start_index = f.find('_Original')
            f = f[:start_index]
            fgdc_output.append(f)

    for dirpath, subdirs, files in os.walk(metadata_folder):

        for f in files:
            end_index = f.find('.shp')
            if f[:end_index] in fgdc_output:
                continue
            else:
                pending.append(f)

    print("Pending FGDC creation: ", len(pending))
    print(pending)

fgdc = '/home/bhavika/Desktop/GIS/Metadata OGP/Alexandria_2007_DataCD/fgdc_output'
metadata = '/home/bhavika/Desktop/GIS/Metadata OGP/Alexandria_2007_DataCD/metadata'
find_pending_fgdc_datasets(fgdc, metadata)

"""
This script aims to automate the process of adding Abstract <abstract>, Purpose <purpose>, <origin>, <publish>, 
<publisher>, <srccitea>, <caldate>, <themekt>, <themekey> and <onlink> values to the metadata files in order 
to make them compliant with ogpIngest and Solr.
"""

from lxml import etree
import os

input_basepath = '/home/bhavika/Desktop/GIS/Metadata OGP/Alexandria_2007_DataCD/fgdc_output'
output_path = 'home/bhavika/Desktop/GIS/Metadata OGP/Alexandria_2007_DataCD/ogpIngest_fgdc'


def edit_file(path):
    for dirpath, subdirs, files in os.walk(path):
        for f in files:
            p = os.path.join(input_basepath, f)
            doc = etree.parse(p)

            doc.find('abstract')


edit_file(input_basepath)




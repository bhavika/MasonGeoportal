from geoserver_utils.Catalog import CatalogUtils
import os
from os.path import basename
from geoserver.catalog import Catalog

alexandria_2007_path = "/media/bhavika/Bhavika/BHAVIKA/Geodata/all/Alexandria_2007_DataCD"
arlington_2004_path = "/media/bhavika/Bhavika/BHAVIKA/Geodata/all/Arlington_2004"
arlington_2011_path = "/media/bhavika/Bhavika/BHAVIKA/Geodata/all/Arlington_2011"
campus = "/media/bhavika/Bhavika/BHAVIKA/Geodata/all/campus"
fairfax_county_path = "/media/bhavika/Bhavika/BHAVIKA/Geodata/all/Fairfax_County"

# c = CatalogUtils(url="http://localhost:8080/geoserver/rest", user="", pw="")
c = CatalogUtils(url="http:///geoserver/rest", user="", pw="")


def find_shapefiles(path):
    shpfiles = {}
    for dirpath, subdirs, files in os.walk(path):
        for x in files:
            if x.endswith(".shp"):
                name = os.path.splitext(x)[0]
                shpfiles[name] = os.path.join(dirpath, x)
    for shp in shpfiles.keys():
        file_path = shpfiles[shp]
        print file_path
        c.add_shapefile(data=file_path, ws="GMUGeodata")
    print shpfiles


def edit_layers(workspace):
    cat = Catalog("http:///geoserver/rest", username="", password="")
    r = cat.get_resources(store="geodata", workspace=workspace)
    print(r)

find_shapefiles(alexandria_2007_path)

print c.store_exists("geodata")

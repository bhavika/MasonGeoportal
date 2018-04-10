from geoserver_utils.Catalog import CatalogUtils
import os
from geoserver.catalog import Catalog
from dotenv import load_dotenv

load_dotenv('../.env')

alexandria_2007_path = os.environ['ALEXANDRIA_2007_PATH']
arlington_2004_path = os.environ['ARLINGTON_2004_PATH']
arlington_2011_path = os.environ['ARLINGTON_2011_PATH']
campus = os.environ['CAMPUS']
fairfax_county_path = os.environ['FAIRFAX_CO_PATH']

user = str(os.environ['GEOSERVER_USERNAME'])
password = str(os.environ['GEOSERVER_PASSWORD'])

# c = CatalogUtils(url="http://localhost:8080/geoserver/rest", user="", pw="")
c = CatalogUtils(url=str(os.environ['GEOSERVER_URL']), user=user,
                 pw=password)

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
        c.add_shapefile(data=file_path, ws=os.environ['GEOSERVER_WORKSPACE_NAME'])
    print shpfiles


def edit_layers(workspace):
    cat = Catalog(url=str(os.environ['GEOSERVER_URL']), user=user, pw=password)
    r = cat.get_resources(store="geodata", workspace=workspace)
    print(r)

# find_shapefiles(alexandria_2007_path)

print c.store_exists("GMUROAD_LC")

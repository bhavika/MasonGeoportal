from geoserver.catalog import Catalog
import geoserver.util
import os


class CatalogUtils:
    cat = None

    def __init__(self, url=None, user=None, pw=None):
        """
        :param url: example: http://localhost:8080/geoserver/rest/
        :param user:
        :param pw:
        """
        self.cat = Catalog(url, username=user, password=pw)

    def ws(self, ws_name):
        return self.cat.get_workspace(ws_name)

    def get_shapefile(self, path):
        """
        Creates a dictionary of all the files in a shapefile (.shp, .dbf, .xml, etc.)
        :param path: path to unarchived shapefile, without extension
        :return:
        """
        return geoserver.util.shapefile_and_friends(path)

    def store_exists(self, name):
        for i in self.cat.get_stores():
            if i.name == name:
                return True
        return False

    def add_shapefile(self, data, name=None, ws=None):
        """
        Adds a shapefile to a GeoServer instance as a Feature Store
        :param data: the path to the shapefile  (.shp) or the zipped shapefile (.zip)
        :param name: the name of the feature store. if None, the file name will be used
        :param ws: the name of the workspace. if None, the default workspace will be used
        :return: the created feature store
        """

        if name is None:
            name = os.path.split(data)[-1]
            if name.endswith('.zip') or name.endswith('.shp'):
                name = name[:name.rindex('.')].upper()
                # name = name[:name.rindex('.')]
                print name

        if self.store_exists(name):
            print "Store exists", name
            raise Exception("A store with this name already exists... please change the name.")

        if data.endswith('.shp'):
            data = self.get_shapefile(data[:data.rindex('.')])
        elif data.endswith('.zip'):
            pass
        else:
            raise Exception("'data' must be the path to a shapefile (.shp) or zipped shapefile.")

        if ws is not None:
            ws = self.ws(ws)
            if ws is None:
                raise Exception("The requested workspace does not exist.")
        else:
            ws = self.cat.get_default_workspace()
            if ws is None:
                raise Exception("No default workspace found!")
        print('adding: ' + name)
        self.cat.create_featurestore(name="GMU"+name, data=data, workspace=ws)
        return self.cat.get_store("GMU"+name)

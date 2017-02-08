from geoserver_utils.Catalog import CatalogUtils
from MetadataUtils.extract_bounds import ExtractBounds
import json

inst_code = "gmu"
geoserver_url = 'http://localhost:8080/geoserver'


class GeoServerAdder:
    def __init__(self, url=geoserver_url, user=None, password=None, institution_code=inst_code, ws_name=None):
        self.ws_name = ws_name
        self.geoserver_url = url
        self.cat = CatalogUtils(url + '/rest/', user, password)
        self.institution_code = institution_code

    def add_dataset_to_geoserver(self, dataset_path, download_url=None, ws_name=None):
        f = self.cat.add_shapefile(dataset_path, ws=ws_name)
        return self.get_metadata_from_geoserver(f, download_url=download_url)

    def get_metadata_from_geoserver(self, featurestore, download_url=None):
        ft = featurestore.get_resources()[0]
        metadata = {'Availability': 'online', 'GeoReferenced': True,
                    'Name': ft.name, 'Institution': self.institution_code.lower(),
                    'WorkspaceName': featurestore.workspace.name,
                    'DataType': GeoServerAdder.get_datatype_from_default_style(ft),
                    'LayerId': self.institution_code.lower() + '.' + ft.name.lower()}

        bounds = ft.latlon_bbox

        metadata['MinX'] = float(bounds[0])
        metadata['MaxX'] = float(bounds[1])
        metadata['MinY'] = float(bounds[2])
        metadata['MaxY'] = float(bounds[3])

        # adds centerx, centery, area, halfheight, halfwidth
        metadata = ExtractBounds.add_spatial(metadata)

        base_ows = self.geoserver_url + '/' + featurestore.workspace.name
        # add location object
        wms = base_ows + '/wms'
        wfs = base_ows + '/wfs'
        if download_url is None:
            metadata['Location'] = GeoServerAdder.get_location(wms=wms, wfs=wfs)
        else:
            metadata['Location'] = GeoServerAdder.get_location(wms=wms, wfs=wfs, file_download=download_url)
        return metadata

    @staticmethod
    def get_datatype_from_default_style(ft):
        name = ft.name
        # polygon, line, point
        return ft.catalog.get_layer(name).default_style.name.title()

    @staticmethod
    def get_location(wms=None, wfs=None, file_download=None):
        '''
                "Location": "{\"wms\":[\"https://geowebservices.princeton.edu/geoserver/pulmap-restricted/wms\"],
                \"fileDownload\":[\"https://geowebservices.princeton.edu/item/5m60qt49k/data.zip\"],
                \"wfs\":\"https://geowebservices.princeton.edu/pulmap-restricted/geoserver/wfs\"}",

        :param wms:
        :param wfs:
        :param file_download:
        :return:
        '''
        loc = {}
        if wms is not None:
            loc['wms'] = [wms]

        if wfs is not None:
            loc['wfs'] = wfs

        if file_download is not None:
            loc['fileDownload'] = file_download

        return json.dumps(loc)

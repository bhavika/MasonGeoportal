__author__ = 'cbarne02'

import json
from extract_from_metadata import ExtractFromMetadata

class RepairFromMetadata:

    @staticmethod
    def suspicious(layer):
        suspicious = []
        # check Location
        if not RepairFromMetadata.check_location(layer):
            suspicious.append('Location')

        # check bounds
        if not RepairFromMetadata.check_bounds(layer):
            suspicious.append('Bounds')

        # check DataType
        if not RepairFromMetadata.check_datatype(layer):
            suspicious.append('DataType')

        if 'LayerDisplayName' not in layer:
            suspicious.append('LayerDisplayName')

        # check ContentDate
        if 'ContentDate' not in layer:
            suspicious.append('ContentDate')

        # check Originator
        if 'Originator' not in layer:
            suspicious.append('Originator')

        # check Publisher
        if 'Publisher' not in layer:
            suspicious.append('Publisher')

        # check keywords
        if 'ThemeKeywords' not in layer:
            suspicious.append('ThemeKeywords')

        if 'PlaceKeywords' not in layer:
            suspicious.append('PlaceKeywords')

        return suspicious

    @staticmethod
    def check_location(layer):
        if 'Location' not in layer:
            return False
        if len(layer['Location']) < 4:
            return False
        return True

    @staticmethod
    def check_datatype(layer):
        if 'DataType' in layer:
            val = layer.get('DataType')
            if val.lower() in ['line', 'point', 'polygon', 'raster', 'scanned map']:
                return True

        return False

    @staticmethod
    def check_bounds(layer):
        if 'MinX' in layer and 'MinY' in layer and 'MaxX' in layer and 'MaxY'in layer:
            if layer['MinX'] + layer['MinY'] + layer['MaxX'] + layer['MaxY'] == 0:
                return False
        else:
            return False
        return True

    @staticmethod
    def repair_from_xml(layer, suspicious=None):
        xml_string = layer.get('FgdcText')

        extract = ExtractFromMetadata(xml_string)

        if 'Bounds' in suspicious:
            bounds = extract.get_bounds()
            RepairFromMetadata.update_layer(layer, bounds)
        if 'Location' in suspicious:
            links = extract.get_links()
            if links is not None:
                layer['Location'] = json.dumps(links)
        if 'DataType' in suspicious:
            RepairFromMetadata.update_layer(layer, extract.get_datatype())
        if 'LayerDisplayName' in suspicious:
            title = extract.get_title()
            RepairFromMetadata.update_layer(layer, title)

        return layer

    @staticmethod
    def update_layer(layer, new_info):
        if layer is None:
            raise Exception("layer is None!")
        if new_info is not None and len(new_info) > 0:
            return layer.update(new_info)
        return layer




__author__ = 'cbarne02'


class ExtractBounds:

    @staticmethod
    def get_bounds(xml_doc, mtype, ns):

        if mtype == 'ISO19139':
            return ExtractBounds.extract_iso_bounds(xml_doc, ns)
        elif mtype == 'FGDC':
            return ExtractBounds.extract_fgdc_bounds(xml_doc)
        else:
            print('match failed')
            print(xml_doc)
            raise Exception('No logic for this metadata type.')

    @staticmethod
    def extract_fgdc_bounds(xml_doc):
        bounds = {}
        node = xml_doc.find('.//metadata/idinfo/spdom/bounding')
        bounds['MaxX'] = float(node.find('eastbc').text)
        bounds['MinX'] = float(node.find('westbc').text)
        bounds['MaxY'] = float(node.find('northbc').text)
        bounds['MinY'] = float(node.find('southbc').text)
        return bounds

    @staticmethod
    def extract_iso_bounds(xml_doc, ns):
        bounds = {}
        node = xml_doc.find('.//gmd:EX_GeographicBoundingBox', ns)
        bounds['MaxX'] = float(node.find('gmd:eastBoundLongitude/*', ns).text)
        bounds['MinX'] = float(node.find('gmd:westBoundLongitude/*', ns).text)
        bounds['MaxY'] = float(node.find('gmd:northBoundLatitude/*', ns).text)
        bounds['MinY'] = float(node.find('gmd:southBoundLatitude/*', ns).text)
        return bounds

    @staticmethod
    def add_spatial(layer):
        if 'MinX' in layer and 'MaxX' in layer and 'MinY' in layer and 'MaxY' in layer:
            # add fields like HalfHeight, HalfWidth, Area, etc.
            height = abs(layer['MaxY'] - layer['MinY'])
            width = abs(layer['MaxX'] - layer['MinX'])
            layer['HalfHeight'] = height / 2
            layer['HalfWidth'] = width / 2
            layer['Area'] = height * width
            layer['CenterY'] = layer['MinY'] + layer['HalfHeight']
            layer['CenterX'] = layer['MinX'] + layer['HalfWidth']
        return layer
__author__ = 'cbarne02'


class ExtractDataType:

    @staticmethod
    def get(xml_doc, mtype, ns):

        if mtype == 'ISO19139':
            return ExtractDataType.extract_iso_datatype(xml_doc, ns)

        elif mtype == 'FGDC':
            return ExtractDataType.extract_fgdc_datatype(xml_doc)
        else:
            print('match failed')
            print(xml_doc)
            raise Exception('No logic for this metadata type.')


    '''

        DataType_Srccitea("srccitea", "/metadata/spdoinfo/srccitea"), // TODO:
        // Verify
        // xpath
        DataType_Direct("direct", "/metadata/spdoinfo/direct"), DataType_Sdtstype(
                "sdtstype", "/metadata/spdoinfo/ptvctinf/sdtsterm/sdtstype")
    '''
    @staticmethod
    def extract_fgdc_datatype(xml_doc):
        srccitea = ExtractDataType.extract_srccitea(xml_doc)
        if srccitea is None:
            direct = ExtractDataType.extract_direct(xml_doc)
            if direct is None:
                direct = 'Unknown'
            return {'DataType': direct}
        else:
            print('Scanned map?????????: ' + srccitea)

    @staticmethod
    def extract_direct(xml_doc):
        xpath = './/direct'
        node = xml_doc.find(xpath)
        if node is None or node.text is None:
            return None
        elif node.text.lower().find('vector') != -1:
            return ExtractDataType.extract_sdtstype(xml_doc)
        elif node.text.lower().find('polygon') != -1:
            return 'Polygon'
        else:
            print('RASTER>>>>>>>' + node.text)

    @staticmethod
    def extract_sdtstype(xml_doc):
        xpath = './/sdtstype'
        node = xml_doc.find(xpath)
        if node is None:
            return None
        elif node.text.lower().find('polygon') != -1:
            return 'Polygon'
        elif node.text.lower().find('string') != -1:
            return 'Line'
        elif node.text.lower().find('point') != -1:
            return 'Point'
        else:
            return 'Unknown'

    @staticmethod
    def extract_srccitea(xml_doc):
        xpath = './/srccitea'
        node = xml_doc.find(xpath)
        if node is None:
            return None
        else:
            return node.text
        # elif node.text.lower().find('polygon') != -1:
        #     return 'Polygon'
        # elif node.text.lower().find('string') != -1:
        #     return 'Line'
        # elif node.text.lower().find('point') != -1:
        #     return 'Point'
        # else:
        #     return 'Unknown'


    @staticmethod
    def extract_iso_datatype(xml_doc, ns):
        # CI_PresentationFormCode, attribute: codeListValue
        xpath ='.//gmd:CI_PresentationFormCode'
        dtype = ExtractDataType.get_code_list_value(xml_doc, xpath, ns)

        if dtype == 'mapDigital':
            vtype = ExtractDataType.extract_map_digital(xml_doc, ns)
            if vtype is None:
                vtype = 'Unknown'
            return {'DataType': vtype}
        elif dtype == 'mapImage':
            return {'DataType': 'ScannedMap'}
        else:
            print('!!!!!!!!!!!!!!!!! non spatial metadata record.')
        return None

    @staticmethod
    def extract_map_digital(xml_doc, ns):
        xpath = './/gmd:MD_SpatialRepresentationTypeCode'
        dtype = ExtractDataType.get_code_list_value(xml_doc, xpath, ns)

        if dtype == 'vector':
            vtype = ExtractDataType.extract_geometric_object_code(xml_doc, ns)
            if vtype == 'Unknown':
                return ExtractDataType.extract_geom_type_code(xml_doc, ns)
            else:
                return vtype
        elif dtype == 'grid':
            return 'Raster'
        elif dtype == 'tin':
            return 'Raster'
        else:
            print('Not a recognized SpatialRepresentationTypeCode !!!!!!!!!!!!!!')
            return None


    @staticmethod
    def extract_geometric_object_code(xml_doc, ns):
        xpath = './/gmd:MD_GeometricObjectTypeCode'
        dtype = ExtractDataType.get_code_list_value(xml_doc, xpath, ns)
        if dtype == 'point':
            return 'Point'
        elif dtype == 'surface':
            return 'Polygon'
        elif dtype == 'curve':
            return 'Line'
        else:
            return 'Unknown'

    @staticmethod
    def extract_geom_type_code(xml_doc, ns):
        xpath = './/gmd:MI_GeometryTypeCode'
        dtype = ExtractDataType.get_code_list_value(xml_doc, xpath, ns)
        return dtype


    @staticmethod
    def get_code_list_value(xml_doc, xpath, ns):
        node = xml_doc.find(xpath, ns)
        if node is None:
            return None

        if 'codeListValue' in node.attrib:
            return node.attrib['codeListValue']
        else:
            return None

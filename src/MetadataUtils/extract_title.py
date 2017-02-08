__author__ = 'cbarne02'


class ExtractTitle:

    @staticmethod
    def get(xml_doc, mtype, ns):

        if mtype == 'ISO19139':
            return ExtractTitle.extract_iso_title(xml_doc, ns)
        elif mtype == 'FGDC':
            return ExtractTitle.extract_fgdc_title(xml_doc)
        else:
            print('match failed')
            print(xml_doc)
            raise Exception('No logic for this metadata type.')

    @staticmethod
    def extract_fgdc_title(xml_doc):
        node = xml_doc.find('.//idinfo/citation/citeinfo/title')
        name = ''
        if node is not None:
            name = node.text
        return {'LayerDisplayName': name}

    @staticmethod
    def extract_iso_title(xml_doc, ns):
        node = xml_doc.find('.//gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/*', ns)
        name = ''
        if node is not None:
            name = node.text
        return {'LayerDisplayName': name}
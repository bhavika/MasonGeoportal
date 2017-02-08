import xml.etree.ElementTree as ET


class XmlUtils:

    @staticmethod
    def parse_metadata_type(xml_doc):
        root = xml_doc.getroot().tag
        if root.rfind('metadata') != -1:
            return 'FGDC'
        if root.rfind('MD_Metadata') != -1:
            return 'ISO19139'
        elif root.rfind('MI_Metadata') != -1:
            return 'ISO19139'
        else:
            raise Exception('Unknown metadata type')

    @staticmethod
    def to_doc(xml_string):
        try:
            parser = ET.XMLParser(encoding="utf-8")
            el = ET.XML(xml_string, parser=parser)
            tree = ET.ElementTree(element=el)
            return tree
        except UnicodeEncodeError as e:
            print(e.message)
            print(xml_string)
            raise e
        except ET.ParseError as e:
            print(e.message)
            print(xml_string)
            raise e
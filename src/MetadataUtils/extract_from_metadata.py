from xml_utils import XmlUtils
from extract_bounds import ExtractBounds
from extract_links import ExtractLinks
from extract_datatype import ExtractDataType
from extract_title import ExtractTitle


class ExtractFromMetadata:
    ns = {'gmd': 'http://www.isotc211.org/2005/gmd'}

    def __init__(self, xml_string):
        self.xml_doc = XmlUtils.to_doc(xml_string)
        self.mtype = XmlUtils.parse_metadata_type(self.xml_doc)

    def get_bounds(self):
        return ExtractBounds.get_bounds(self.xml_doc, self.mtype, self.ns)

    def get_links(self):
        return ExtractLinks.get_links(self.xml_doc, self.mtype, self.ns)

    def get_datatype(self):
        return ExtractDataType.get(self.xml_doc, self.mtype, self.ns)

    def get_title(self):
        return ExtractTitle.get(self.xml_doc, self.mtype, self.ns)

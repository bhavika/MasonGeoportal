__author__ = 'cbarne02'

'''
<CI_OnlineResource>
    <linkage>
        <URL>http://opendata.minneapolismn.gov/datasets/107ae837504447bab708d481fdd52175_0</URL>
    </linkage>
    <protocol>
        <gco:CharacterString>download</gco:CharacterString>
    </protocol>
</CI_OnlineResource>
'''
class ExtractLinks:

    @staticmethod
    def get_links(xml_doc, mtype, ns):
        if mtype == 'ISO19139':
            try:
                return ExtractLinks.extract_iso_links(xml_doc, ns)
            except Exception as e:
                print(e.message)
                print('find failed')

        elif mtype == 'FGDC':
            try:
                return ExtractLinks.extract_fgdc_links(xml_doc)
            except Exception as e:
                print(e.message)
                print('find failed')
        else:
            print('match failed')
            print(xml_doc)
            raise Exception('No logic for this metadata type.')
        print('returning None')
        return None

    @staticmethod
    def extract_iso_links(xml_doc, ns):
        location = {}
        nodes = xml_doc.findall('.//gmd:CI_OnlineResource', ns)
        for node in nodes:
            ltype = node.find('gmd:protocol/*', ns).text
            url = node.find('gmd:linkage/*', ns).text
            if ltype == 'download':
                if url.lower().rfind('.zip') != -1:
                    location['fileDownload'] = [url]
                else:
                    location['externalDownload'] = url
        return location

    @staticmethod
    def extract_fgdc_links(xml_doc):
        location = {}
        nodes = xml_doc.findall('.//onlink')
        for node in nodes:
            url = node.text
            location = ExtractLinks.add_link(location, url)
        return location

    @staticmethod
    def add_link(loc, link):
        if link is None:
            return loc

        if link.lower().find('wms') != -1:
            loc['wms'] = [link]
        elif link.lower().rfind('.zip') != -1:
            loc['fileDownload'] = [link]
        elif link.lower().find('stds/metadata.htm') != -1:
            pass
        elif link.lower().find('standards/mgmg/metadata.htm') != -1:
            pass

        return loc
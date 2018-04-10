"""
This script aims to automate the process of adding Abstract <abstract>, Purpose <purpose>, <origin>, <publish>, 
<publisher>, <srccitea>, <caldate>, <themekt>, <themekey> and <onlink> values to the metadata files in order 
to make them compliant with ogpIngest and Solr.
"""

from lxml import etree
import os
import pickle

input_basepath = '/home/bhavika/Desktop/GIS/Metadata OGP/Alexandria_2007_DataCD/fgdc_output'
output_path = '/home/bhavika/Desktop/GIS/Metadata OGP/Alexandria_2007_DataCD/ogpIngest_fgdc'
metadata_path = '../metadata/'

tags = ['//abstract', '//srccitea', '//origin', '//purpose', '//publish', '//caldate', '//themekt',
        '//themekey', '//onlink', '//ftname']

citeinfo_tags = ['//srccitea', '//origin', '//purpose', '//publish', '//ftname', '//onlink']
theme_tags = ['//themekt', '//themekey']


def save_input_attributes(obj, name):
    with open(name+'.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_input_attributes(name):
    with open(metadata_path + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def get_missing_attributes(path):
    for dirpath, subdirs, files in os.walk(path):
        for f in files:
            p = os.path.join(input_basepath, f)
            doc = etree.parse(p)

            print(f)
            attributes = {}

            for t in tags:
                if doc.find(t) is None:
                    print("Enter input for {}".format(t))
                    input_text = raw_input()
                    attributes[t] = input_text
                    # print(t, doc.findtext(t) if doc.find(t) is not None else "{} not found.".format(t))
            print(attributes)
            save_input_attributes(attributes, f)


def create_fgdc_metadata(path):
    for dirpath, subdirs, files in os.walk(path):
        for f in files:
            p = os.path.join(input_basepath, f)
            doc = etree.parse(p)

            new_attributes = load_input_attributes(f)

            for k, v in new_attributes.items():
                key = k[2:]
                el = etree.Element(key)
                el.text = v

                if k in citeinfo_tags:
                    root = doc.find('//citeinfo')

                # elif k in theme_tags:
                #     root = doc.findall('.//theme').tag

                if root:
                    root.append(el)
                    fname_start_idx = f.find('_Original.xml')
                    fname = f[0:fname_start_idx]
                    ftname_el = etree.Element('ftname', Sync='TRUE')
                    ftname_el.text = fname.upper()
                    root.append(ftname_el)
                    # for el in root.iter(tag=etree.Element):
                    #     print(el.tag, el.text)
                else:
                    print("No root found :", f)

            with open(os.path.join(output_path, f), 'w') as f:
                f.write(etree.tostring(doc))


# get_missing_attributes(input_basepath)
create_fgdc_metadata(input_basepath)

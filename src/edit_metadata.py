"""
This script aims to automate the process of adding Abstract <abstract>, Purpose <purpose>, <origin>, <publish>, 
<publisher>, <srccitea>, <caldate>, <themekt>, <themekey> and <onlink> values to the metadata files in order 
to make them compliant with ogpIngest and Solr.
"""

from lxml import etree
import os
from Tkinter import *

input_basepath = '/home/bhavika/Desktop/GIS/Metadata OGP/Alexandria_2007_DataCD/fgdc_output'
output_path = 'home/bhavika/Desktop/GIS/Metadata OGP/Alexandria_2007_DataCD/ogpIngest_fgdc'


tags = ['//abstract', '//srccitea', '//origin', '//purpose', '//publish', '//caldate', '//themekt', '//themekey',
        '//onlink']


def edit_file(path):
    def enter_input(tb):
        text = tb.get('1.0', 'end-1c')
        print(text)

    for dirpath, subdirs, files in os.walk(path):
        for f in files:
            p = os.path.join(input_basepath, f)
            doc = etree.parse(p)

            print(f)

            for t in tags:
                if doc.find(t) is None:
                    print(t)
                    root = Tk()
                    tb = Text(root, height=10, width=50)
                    tb.pack()
                    btn = Button(root, height=2, width=10, text='Commit', command=enter_input(tb))
                    btn.pack()
                    root.mainloop()
                    # print(t, doc.findtext(t) if doc.find(t) is not None else "{} not found.".format(t))


edit_file(input_basepath)




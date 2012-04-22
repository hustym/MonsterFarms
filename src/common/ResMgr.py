# coding: utf-8
#!/usr/bin/python

from xml.dom import minidom

class XMLParser():

    def __init__(self, filenmae):
        self.filename = filename
        h = file(filename, 'r')
        self.string = h.read()
        h.close()

    def parse(self):
        dom = minidom.parseString(self.string)
        return dom




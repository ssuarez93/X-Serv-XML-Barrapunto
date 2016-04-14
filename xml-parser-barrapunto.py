#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Title: " + self.theContent + "."
                # To avoid Unicode trouble
                resp1 = line.encode('latin1') + "</br>"
                html_File.write(resp1)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                resp2 = " Link: " + "<a href='" + self.theContent + "'>" + self.theContent + "</a>" + "." + "</br>"
                html_File.write(resp2)
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv)<3:
    print "Usage: python xml-parser-barrapunto.py <document> <html_file>"
    print
    print " <document>: file name of the document to parse"
    print " <document_html>: file name of the html document to write"
    sys.exit(1)

# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")
html_File = open(sys.argv[2], "w")
theParser.parse(xmlFile)

print "Parse complete"

#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree

from google.appengine.ext import db

import pprint

pp = pprint.PrettyPrinter(indent=4)
tree = ElementTree()
tree.parse("test.xml")
crisis = tree.find("crises/crisis")
taglist = list(crisis.iter())
print taglist[1].text

class crisis (db.Model):
    name = db.StringProperty()


print "done"
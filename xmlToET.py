#!/usr/bin/env python
import sys


from xml.etree.ElementTree import ElementTree


import pprint

pp = pprint.PrettyPrinter(indent=4)
tree = ElementTree()
tree.parse("rss873-WC1.xml")
crisis = tree.findall("crises/crisis")
insideC = list(crisis[0].iter())
pp.pprint(insideC)


print "Last thing in the class"


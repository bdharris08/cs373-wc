import webapp2
import jinja2
import os
import urllib
import time
import re

from genxmlif import GenXmlIfError
from minixsv import pyxsval
    
from xml.etree.ElementTree import ElementTree
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import files

#  search branch
class MainPage(webapp2.RequestHandler):
    def get(self):
        wc = WorldCrises.all().fetch(1).pop()
        crises = wc.crises.fetch(None)
        orgs = wc.organizations.fetch(None)
        persons = wc.persons.fetch(None)
            
        path = os.path.join(os.path.dirname(__file__), 'splash.html')
        self.response.out.write(template.render(path, {"crises": crises, "orgs" : orgs, "persons" : persons}))

class TempHandler(webapp2.RequestHandler):
    def get(self):
        blob_info = blobstore.BlobInfo.all().filter("filename =", "db.txt").fetch(None)
        for b in blob_info:
            b.delete()
        upload_url = blobstore.create_upload_url('/temp_upload')
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
            name="submit" value="Submit"> </form></body></html>""")
        
class TempUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.response.out.write('<html><body>')
        self.response.out.write('''<form action="/search_result"> 
                                    Search: <input type="text" name="keyword" 
                                    /><br /> <input type="submit" value="Submit" 
                                    /> </form>''')
        self.response.out.write('</body></html>')
        
class SearchResultHandler(webapp2.RequestHandler):
    def get(self):
        keyword= self.request.get("keyword")
        baseurl = "http://www.jontitan-cs373-wc.appspot.com/"
        blob_info = blobstore.BlobInfo.all().filter("filename =", "db.txt").fetch(1).pop()
        blob_reader = blob_info.open()
        lines = blob_reader.readlines()
        articles = []
        temp = []
        for l in lines:
            if(baseurl in l):
                article = [re.split(" ", l, maxsplit =1), temp]  
                articles.append(article)
                temp = []
            else:
                temp.append(l)
        
        
        dictionary = {"keyword": keyword}
        matchedExact = []
        matchedAnd = []
        matchedOr = []
        keywordI = re.compile(keyword, re.IGNORECASE)
        """
        for a in articles:
            url = a[0][0]
            name = a[0][1]
            lines = a[1]
            for l in lines:
                parsedLine = re.split(":", l, maxsplit = 1)
                if(keyword.lower() in parsedLine):
                    parsedMatched = re.split(keywordI, l)
                    matchedExact.append([name, url, parsedMatched])
                
                elif

        """
        for i in range(len(lines)):
            if(not(baseurl in lines[i])):
                parsedLine = re.split(":", lines[i], maxsplit = 1)
                if(len(parsedLine) == 2):
                    line = parsedLine[1].lower()
                    if(keyword.lower() in line):
                        parsedMatched = re.split(keywordI, lines[i])
                        temp = []
                        temp.append(parsedMatched)
                        for j in range(i+1, len(lines)):                 
                            if(baseurl in lines[j]):
                                temp.append(lines[j])
                                temp.append(lines[j+1])
                                matched.append(temp)
                                break
            else:
                i += 2
                if(i >= len(lines)): break
        
        dictionary["matched"] = matched
        
        path = os.path.join(os.path.dirname(__file__), 'temp_search_result.html')
        self.response.out.write(template.render(path, dictionary))

        """
        print "In Temp page"
        db_txt = files.blobstore.create(mime_type='application/octet_stream')
        with files.open(db_txt, 'a') as f:
            f.write("first write\n")
            
        with files.open(db_txt, 'a') as f:
            f.write("second write\n")           
        files.finalize(db_txt)
        
        file_key = files.blobstore.get_blob_key(db_txt)
        file_reader = blobstore.BlobReader(file_key)
        print file_reader.readline()
        print file_reader.readline()
        """
            
class CrisisDisplayHandler(webapp2.RequestHandler):
    def get(self):
        dictionary = {}
        wc = WorldCrises.all().fetch(1).pop()
        crises = wc.crises.fetch(None)
        dictionary["crises"] = crises
        images = []
        for c in crises :
            extRefs = c.ref.fetch(None)
            for r in extRefs :
                if(r.ref_type == "primaryImage") :
                    images.append(r.url)
                    break
        dictionary["images"] = images
        path = os.path.join(os.path.dirname(__file__), 'crisis_display.html')
        self.response.out.write(template.render(path, dictionary))

class OrgDisplayHandler(webapp2.RequestHandler):
    def get(self):
        dictionary = {}
        wc = WorldCrises.all().fetch(1).pop()
        orgs = wc.organizations.fetch(None)
        dictionary["orgs"] = orgs
        images = []
        for o in orgs :
            extRefs = o.ref.fetch(None)
            for r in extRefs :
                if(r.ref_type == "primaryImage") :
                    images.append(r.url)
                    break
        dictionary["images"] = images
        path = os.path.join(os.path.dirname(__file__), 'org_display.html')
        self.response.out.write(template.render(path, dictionary))
        
class PersonDisplayHandler(webapp2.RequestHandler):
    def get(self):
        dictionary = {}
        wc = WorldCrises.all().fetch(1).pop()
        persons = wc.persons.fetch(None)
        dictionary["persons"] = persons
        images = []
        for p in persons :
            extRefs = p.ref.fetch(None)
            for r in extRefs :
                if(r.ref_type == "primaryImage") :
                    images.append(r.url)
                    break
        dictionary["images"] = images
        path = os.path.join(os.path.dirname(__file__), 'person_display.html')
        self.response.out.write(template.render(path, dictionary))
        
class CrisisHandler(webapp2.RequestHandler):
    def get(self, resource):
        dictionary = {}
        resource = str(urllib.unquote(resource))
        crisis = Crisis.all().filter("id =", resource).fetch(1).pop()
        dictionary["crisis"] = crisis
        crisisInfo = crisis.info.fetch(1).pop()
        dictionary["crisisInfo"] = crisisInfo
        time = crisisInfo.time.fetch(1).pop()
        dictionary["time"] = time
        loc = crisisInfo.location.fetch(1).pop()
        dictionary["loc"] = loc
        humanImpact = crisisInfo.humanImpact.fetch(1).pop()
        dictionary["humanImpact"] = humanImpact
        economicImpact = crisisInfo.economicImpact.fetch(1).pop()
        dictionary["economicImpact"] = economicImpact
        
        extRefs = crisis.ref.fetch(None)
        for r in extRefs :
            type = r.ref_type
            if(type in dictionary):
                value = dictionary[type]
                dictionary[type].append(r)
            else: 
                dictionary[type] = [r]
                
        qOrgRefs = crisis.crisisOrg.fetch(None)
        orgRefs = []
        for o in qOrgRefs :
            orgRefs.append(o.crisis)
        dictionary["orgRefs"] = orgRefs
        
        qPersonRefs = crisis.crisisPerson.fetch(None)
        personRefs = []
        for p in qPersonRefs :
            personRefs.append(p.crisis)
        dictionary["personRefs"] = personRefs
      
        path = os.path.join(os.path.dirname(__file__), 'temp_crisis.html')
        self.response.out.write(template.render(path, dictionary))
        
class OrgHandler(webapp2.RequestHandler):
    def get(self, resource):
        dictionary = {}
        resource = str(urllib.unquote(resource))
        organization = Organization.all().filter("id =", resource).fetch(1).pop()
        dictionary["organization"] = organization
        orgInfo = organization.info.fetch(1).pop()
        dictionary["orgInfo"] = orgInfo
        contact = orgInfo.contact.fetch(1).pop()
        dictionary["contact"] = contact
        loc = orgInfo.location.fetch(1).pop()
        dictionary["loc"] = loc
        address = contact.mail.fetch(1).pop()
        dictionary["address"] = address
        
        extRefs = organization.ref.fetch(None)
        for r in extRefs :
            type = r.ref_type
            if(type in dictionary):
                value = dictionary[type]
                dictionary[type].append(r)
            else: 
                dictionary[type] = [r]
                
        qCrisisRefs = organization.orgCrisis.fetch(None)
        crisisRefs = []
        for c in qCrisisRefs :
            crisisRefs.append(c.organization) 
        dictionary["crisisRefs"] = crisisRefs
        
        qPersonRefs = organization.orgPerson.fetch(None)
        personRefs = []
        for p in qPersonRefs :
            personRefs.append(p.organization)
        dictionary["personRefs"] = personRefs
      
        path = os.path.join(os.path.dirname(__file__), 'temp_org.html')
        self.response.out.write(template.render(path, dictionary))
        
class PersonHandler(webapp2.RequestHandler):
    def get(self, resource):
        dictionary = {}
        resource = str(urllib.unquote(resource))
        person = Person.all().filter("id =", resource).fetch(1).pop()
        dictionary["person"] = person
        personInfo = person.info.fetch(1).pop()
        dictionary["personInfo"] = personInfo
        birthdate = personInfo.birthdate.fetch(1).pop()
        dictionary["birthdate"] = birthdate
        
        extRefs = person.ref.fetch(None)
        for r in extRefs :
            type = r.ref_type
            if(type in dictionary):
                value = dictionary[type]
                dictionary[type].append(r)
            else: 
                dictionary[type] = [r]
                
        qOrgRefs = person.personOrg.fetch(None)
        orgRefs = []
        for o in qOrgRefs :
            orgRefs.append(o.person)
        dictionary["orgRefs"] = orgRefs
        
        qCrisisRefs = person.personCrisis.fetch(None)
        crisisRefs = []
        for p in qCrisisRefs :
            crisisRefs.append(p.person)
        dictionary["crisisRefs"] = crisisRefs
      
        path = os.path.join(os.path.dirname(__file__), 'temp_person.html')
        self.response.out.write(template.render(path, dictionary))
        
        
class ImportHandler(webapp.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/upload')
    self.response.out.write('<html><body>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
        name="submit" value="Submit"> </form></body></html>""")
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    blob_reader = blob_info.open()
    other_blob_reader = blob_info.open()
    tree = ElementTree()
    
    try:
        assert blob_info.content_type == "text/xml"
    except Exception as e:
        self.redirect("/xmlerror")
        
    xsdText = """<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">

<xsd:element name="worldCrises">
    <xsd:complexType>
        <xsd:sequence>
            <xsd:element name="crisis" type="crisisType"  maxOccurs="unbounded"/>
            <xsd:element name="organization" type="organizationType"  maxOccurs="unbounded"/>
            <xsd:element name="person" type="personType"  maxOccurs="unbounded"/>
        </xsd:sequence>
    </xsd:complexType>
</xsd:element>
 
<xsd:complexType name = "crisisType">
    <xsd:sequence>
        <xsd:element name="name" type="xsd:normalizedString"/>
        <xsd:element name="info" type="crisisInfoType"/>
        <xsd:element name="ref" type="extLinkType"/>
        <xsd:element name="misc" type="xsd:string"/>
        <xsd:element name="org" type="referenceType" maxOccurs="unbounded"/>
        <xsd:element name="person" type="referenceType" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="id" type="xsd:ID" use="required"/>
</xsd:complexType>
 
<xsd:complexType name="organizationType">
    <xsd:sequence>
        <xsd:element name="name" type="xsd:normalizedString"/>
        <xsd:element name="info" type="orgInfoType"/>
        <xsd:element name="ref" type="extLinkType"/>
        <xsd:element name="misc" type="xsd:string"/>
        <xsd:element name="crisis" type="referenceType" maxOccurs="unbounded"/>
        <xsd:element name="person" type="referenceType" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="id" type="xsd:ID" use="required"/>
</xsd:complexType>

<xsd:complexType name="personType">  
    <xsd:sequence>
        <xsd:element name="name" type="xsd:normalizedString"/>
        <xsd:element name="info" type="personInfoType"/>
        <xsd:element name="ref" type="extLinkType"/>
        <xsd:element name="misc" type="xsd:string"/>
        <xsd:element name="crisis" type="referenceType" maxOccurs="unbounded"/>
        <xsd:element name="org" type="referenceType" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="id" type="xsd:ID" use="required"/>
</xsd:complexType>

<xsd:complexType name="locationType">
    <xsd:sequence>
        <xsd:element name="city" type="xsd:normalizedString"/>
        <xsd:element name="region" type="xsd:normalizedString"/>
        <xsd:element name="country" type="xsd:normalizedString"/>
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="dateType">
    <xsd:sequence>
        <xsd:element name="time" type="xsd:string"/>
        <xsd:element name="day" type="xsd:integer"/>
        <xsd:element name="month" type="xsd:integer"/>
        <xsd:element name="year" type="xsd:integer"/>
        <xsd:element name="misc" type="xsd:string"/>
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="crisisInfoType">
    <xsd:sequence>
        <xsd:element name="history" type="xsd:string"/>
        <xsd:element name="help" type="xsd:string"/>
        <xsd:element name="resources" type="xsd:string"/>
        <xsd:element name="type" type="xsd:normalizedString"/>
        <xsd:element name="time" type="dateType"/>
        <xsd:element name="loc" type="locationType"/>
        <xsd:element name="impact" type="impactType"/>   
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="orgInfoType">
    <xsd:sequence>
        <xsd:element name="type" type="xsd:string"/>
        <xsd:element name="history" type="xsd:string"/>
        <xsd:element name="contact" type="contactsType"/>
        <xsd:element name="loc" type="locationType"/>
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="personInfoType">
    <xsd:sequence>
        <xsd:element name="type" type="xsd:normalizedString"/>
        <xsd:element name="birthdate" type="dateType"/>
        <xsd:element name="nationality" type="xsd:normalizedString"/>
        <xsd:element name="biography" type="xsd:string"/>
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="fulladdrType">
    <xsd:sequence>
        <xsd:element name="address" type="xsd:string"/>
        <xsd:element name="city" type="xsd:normalizedString"/>
        <xsd:element name="state" type="xsd:normalizedString"/>
        <xsd:element name="country" type="xsd:normalizedString"/>
        <xsd:element name="zip" type="xsd:normalizedString"/>
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="contactsType">
    <xsd:sequence>
        <xsd:element name="phone" type="xsd:normalizedString"/>
        <xsd:element name="email" type="xsd:normalizedString"/>
        <xsd:element name="mail" type="fulladdrType"/>
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="impactType">
    <xsd:sequence>
        <xsd:element name="human" type="humanImpType"/>
        <xsd:element name="economic" type="econImpType"/>
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="humanImpType">
    <xsd:sequence>
        <xsd:element name="deaths" type="xsd:integer"/>
        <xsd:element name="displaced" type="xsd:integer"/>
        <xsd:element name="injured" type="xsd:integer"/>
        <xsd:element name="missing" type="xsd:integer"/>
        <xsd:element name="misc" type="xsd:string"/>
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="econImpType">
    <xsd:sequence>
        <xsd:element name="amount" type="xsd:integer"/>
        <xsd:element name="currency" type="xsd:normalizedString"/>
        <xsd:element name="misc" type="xsd:string"/>
    </xsd:sequence>
</xsd:complexType>
   
<xsd:complexType name="extType">
    <xsd:sequence>
        <xsd:element name="site" type="xsd:normalizedString"/>
        <xsd:element name="title" type="xsd:normalizedString"/>
        <xsd:element name="url" type="xsd:token"/>
        <xsd:element name="description" type="xsd:string" minOccurs="0" maxOccurs="1" />
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="extLinkType">
    <xsd:sequence>
        <xsd:element name="primaryImage" type="extType" />
        <xsd:element name="image" type="extType" minOccurs="1" maxOccurs="unbounded"/>
        <xsd:element name="video" type="extType" minOccurs="1" maxOccurs="unbounded"/>
        <xsd:element name="social" type="extType" minOccurs="1" maxOccurs="unbounded"/>
        <xsd:element name="ext" type="extType" minOccurs="1" maxOccurs="unbounded"/>
    </xsd:sequence>
</xsd:complexType>

<xsd:complexType name="referenceType">
    <xsd:attribute name="idref" type="xsd:IDREF" use="required"/>
</xsd:complexType>

</xsd:schema>
"""    
        
    try:
        # call validator with non-default values
        elementTreeWrapper = pyxsval.parseAndValidateXmlInputString (other_blob_reader.read(), xsdText)

    except pyxsval.XsvalError, errstr:
        print errstr
        print "Validation aborted!"
    
    except GenXmlIfError, errstr:
        print errstr
        print "Parsing aborted!"
    
    tree.parse(blob_reader)

    crises = tree.findall("crisis")
    assert(crises != [])
    organizations = tree.findall("organization")
    assert(organizations != [])
    people = tree.findall("person")
    assert(people != [])
    
    #Wipe out the datastore data
    db.delete(WorldCrises.all())
    db.delete(Crisis.all())
    db.delete(Organization.all())
    db.delete(Person.all())
    db.delete(CrisisInfo.all())
    db.delete(OrgInfo.all())
    db.delete(PersonInfo.all())
    db.delete(ExternalLink.all())
    db.delete(Date.all())
    db.delete(Location.all())
    db.delete(Contact.all())
    db.delete(FullAddr.all())
    db.delete(HumanImpact.all())
    db.delete(EconomicImpact.all())
    db.delete(CrisisOrganization.all())
    db.delete(CrisisPerson.all())
    db.delete(OrganizationPerson.all())
   
    wc = WorldCrises()
    wc.put()
    
    for c in crises:
        crisis = Crisis()
        crisis.worldCrises = wc
        crisis.id = c.get("id")
        crisis.name = c.find("name").text
        crisis.put()
        
        ci = c.find("info")
        crisisInfo = CrisisInfo()
        crisisInfo.crisis = crisis
        crisisInfo.history = ci.find("history").text
        crisisInfo.help = ci.find("help").text
        crisisInfo.resources = ci.find("resources").text
        crisisInfo.type = ci.find("type").text
        crisisInfo.put()
        
        t = ci.find("time")
        time = Date()
        time.crisisInfo = crisisInfo
        time.time = t.find("time").text
        time.day = int(t.find("day").text)
        time.month = int(t.find("month").text)
        time.year = int(t.find("year").text)
        time.misc = t.find("misc").text
        time.put()
        
        l = ci.find("loc")
        location = Location()
        location.crisisInfo = crisisInfo
        location.city = l.find("city").text
        location.region = l.find("region").text
        location.country = l.find("country").text
        location.put()
        
        i = ci.find("impact")
        
        hi = i.find("human")
        humanImpact = HumanImpact()
        humanImpact.crisisInfo = crisisInfo
        humanImpact.deaths = int(hi.find("deaths").text)
        humanImpact.displaced = int(hi.find("displaced").text)
        humanImpact.injured = int(hi.find("injured").text)
        humanImpact.missing = int(hi.find("missing").text)
        humanImpact.misc = hi.find("misc").text
        humanImpact.put()
        
        ei = i.find("economic")
        economicImpact = EconomicImpact()
        economicImpact.crisisInfo = crisisInfo
        economicImpact.amount = int(ei.find("amount").text)
        economicImpact.currency = ei.find("currency").text
        economicImpact.misc = ei.find("misc").text
        economicImpact.put()
        
        r = c.find("ref")
        
        pi = r.find("primaryImage")
        piRef = ExternalLink()
        piRef.crisis = crisis
        piRef.ref_type = "primaryImage"
        piRef.site = pi.find("site").text
        piRef.title = pi.find("title").text
        piRef.url = pi.find("url").text
        piRef.description = pi.find("description").text
        piRef.put()
        
        image = r.findall("image")
        for i in image:
            ref = ExternalLink()
            ref.crisis = crisis
            ref.ref_type = "image"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()      
            
        v = r.findall("video")
        for i in v:
            ref = ExternalLink()
            ref.crisis = crisis
            ref.ref_type = "video"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
            
        s = r.findall("social")
        for i in s:
            ref = ExternalLink()
            ref.crisis = crisis
            ref.ref_type = "social"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()  
    
        e = r.findall("ext")
        for i in e:
            ref = ExternalLink()
            ref.crisis = crisis
            ref.ref_type = "ext"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
            
    for o in organizations:
        org = Organization()
        org.worldCrises = wc
        org.id = o.get("id")
        org.name = o.find("name").text
        org.misc = o.find("misc").text
        org.put()
        
        oi = o.find("info")
        orgInfo = OrgInfo()
        orgInfo.organization = org
        orgInfo.type = oi.find("type").text
        orgInfo.history = oi.find("history").text
        orgInfo.put()
        
        c = oi.find("contact")
        contact = Contact()
        contact.orgInfo = orgInfo
        contact.phone = c.find("phone").text
        contact.email = c.find("email").text
        contact.put()
        
        fa = c.find("mail")
        fullAddr = FullAddr()
        fullAddr.contact = contact
        fullAddr.address = fa.find("address").text
        fullAddr.city = fa.find("city").text
        fullAddr.state = fa.find("state").text
        fullAddr.country = fa.find("country").text
        fullAddr.zip = fa.find("zip").text
        fullAddr.put()
        
        l = oi.find("loc")
        loc = Location()
        loc.orgInfo = orgInfo
        loc.city = l.find("city").text
        loc.region = l.find("region").text
        loc.country = l.find("country").text
        loc.put()
        
        r = o.find("ref")
        
        pi = r.find("primaryImage")
        piRef = ExternalLink()
        piRef.organization = org
        piRef.ref_type = "primaryImage"
        piRef.site = pi.find("site").text
        piRef.title = pi.find("title").text
        piRef.url = pi.find("url").text
        piRef.description = pi.find("description").text
        piRef.put()
        
        image = r.findall("image")
        for i in image:
            ref = ExternalLink()
            ref.organization = org
            ref.ref_type = "image"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()      
            
        v = r.findall("video")
        for i in v:
            ref = ExternalLink()
            ref.organization = org
            ref.ref_type = "video"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
            
        s = r.findall("social")
        for i in s:
            ref = ExternalLink()
            ref.organization = org
            ref.ref_type = "social"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()  
    
        e = r.findall("ext")
        for i in e:
            ref = ExternalLink()
            ref.organization = org
            ref.ref_type = "ext"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
            
    for p in people :
        person = Person()
        person.worldCrises = wc
        person.id = p.get("id")
        person.name = p.find("name").text
        person.misc = p.find("misc").text
        person.put()
        
        pi = p.find("info")
        pInfo = PersonInfo()
        pInfo.person = person
        pInfo.type = pi.find("type").text
        pInfo.nationality = pi.find("nationality").text
        pInfo.biography = pi.find("biography").text
        pInfo.put()
        
        bd = pi.find("birthdate")
        birthDate = Date()
        birthDate.personInfo = pInfo
        birthDate.time = bd.find("time").text
        birthDate.day = int(bd.find("day").text)
        birthDate.month = int(bd.find("month").text)
        birthDate.year = int(bd.find("year").text)
        birthDate.misc = bd.find("misc").text
        birthDate.put()
        
        r = p.find("ref")
        
        pi = r.find("primaryImage")
        piRef = ExternalLink()
        piRef.person = person
        piRef.ref_type = "primaryImage"
        piRef.site = pi.find("site").text
        piRef.title = pi.find("title").text
        piRef.url = pi.find("url").text
        piRef.description = pi.find("description").text
        piRef.put()
        
        image = r.findall("image")
        for i in image:
            ref = ExternalLink()
            ref.person = person
            ref.ref_type = "image"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()      
            
        v = r.findall("video")
        for i in v:
            ref = ExternalLink()
            ref.person = person
            ref.ref_type = "video"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
            
        s = r.findall("social")
        for i in s:
            ref = ExternalLink()
            ref.person = person
            ref.ref_type = "social"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()  
    
        e = r.findall("ext")
        for i in e:
            ref = ExternalLink()
            ref.person = person
            ref.ref_type = "ext"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
    
    for c in crises :
        crisis = Crisis.all().filter("id =", c.get("id")).fetch(1).pop()
        
        relatedOrg = c.findall("org")
        for o in relatedOrg :
            org = Organization.all().filter("id =", o.get("idref")).fetch(1).pop()
            relation = CrisisOrganization()
            relation.organization = crisis
            relation.crisis = org
            relation.put()
            
        relatedPerson = c.findall("person")
        for p in relatedPerson :
            person = Person.all().filter("id =", p.get("idref")).fetch(1).pop()
            relation = CrisisPerson()
            relation.crisis = person
            relation.person = crisis
            relation.put()
            
    for o in organizations :
        org = Organization.all().filter("id =", o.get("id")).fetch(1).pop()
    
        relatedPerson = o.findall("person")
        for p in relatedPerson :
            person = Person.all().filter("id =", p.get("idref")).fetch(1).pop()
            relation = OrganizationPerson()
            relation.organization = person
            relation.person = org
            relation.put()
    
    #Build db.txt to cache data for efficient searching
    """
    key = dataCacheKey.all().fetch(None)
    assert(len(key) == 1)
    blob_info = key.blob_id.fetch(1).pop()
    blob_info.delete()
    key.delete()
    """
    
    dataCache = files.blobstore.create(mime_type='application/octet_stream')
    
    
    for c in crises:    
        ci = c.find("info")
        t = ci.find("time")
        l = ci.find("loc")
        i = ci.find("impact")
        hi = i.find("human")
        ei = i.find("economic")
        
        if(ci.find("history").text == None): history = " "
        else: history = ci.find("history").text
        if(ci.find("help").text == None): help = " "
        else: help = ci.find("help").text
        if(ci.find("resources").text == None): resources = " "
        else: resources = ci.find("resources").text
        if(ci.find("type").text == None): type = " "
        else: type = ci.find("type").text
        if(t.find("time").text == None): time = " "
        else: time = t.find("time").text
        if(t.find("day").text == None): day = " "
        else: day = t.find("day").text
        if(t.find("month").text == None): month = " "
        else: month = t.find("month").text
        if(t.find("year").text == None): year = " "
        else: year = t.find("year").text
        if(t.find("misc").text == None): miscT = " "
        else: miscT = t.find("misc").text
        if(l.find("city").text == None): city = " "
        else: city = l.find("city").text
        if(l.find("region").text == None): region = " "
        else: region = l.find("region").text
        if(l.find("country").text == None): country = " "
        else: country = l.find("country").text
        if(hi.find("deaths").text == None): deaths = " "
        else: deaths = hi.find("deaths").text
        if(hi.find("displaced").text == None): displaced = " "
        else: displaced = hi.find("displaced").text
        if(hi.find("injured").text == None): injured = " "
        else: injured = hi.find("injured").text
        if(hi.find("missing").text == None): missing = " "
        else: missing = hi.find("missing").text
        if(hi.find("misc").text == None): miscHi = " "
        else: miscHi = hi.find("misc").text
        if(ei.find("amount").text == None): amount = " "
        else: amount = ei.find("amount").text
        if(ei.find("currency").text == None): currency = " "
        else: currency = ei.find("currency").text
        if(ei.find("misc").text == None): miscEi = " "
        else: miscEi = ei.find("misc").text
        if(c.find("name").text == None): name = " "
        else: name = c.find("name").text
        if(c.get("id") == None): id = " "
        else: id = c.get("id")
        
        
        with files.open(dataCache, 'a') as f:
            f.write("History: " + history + "\n" +
                    "Help: " + help + "\n" +
                    "Resources: " + resources + "\n" +
                    "Type: " + type + "\n" +
                    "Time: " + time + "\n" + 
                    "Day: " + day + "\n" +
                    "Month: " + month + "\n" +
                    "Year: " + year + "\n" +
                    "Misc: " + miscT + "\n" +
                    "City: " + city + "\n" +
                    "Region: " + region + "\n" +
                    "Country: " + country + "\n" +
                    "Deaths: " + deaths + "\n" +
                    "Displaced: " + displaced + "\n" +
                    "Injured: " + injured + "\n" +
                    "Missing: " + missing + "\n" +
                    "Misc: " + miscHi + "\n" +
                    "Amount: " + amount + "\n" +
                    "Currency: " + currency + "\n" +
                    "Misc: " + miscEi + "\n" +
                    "http://www.jontitan-cs373-wc.appspot.com/crisis/" + id +
                    " " + name + "\n")
        
    files.finalize(dataCache)    
    file_key = files.blobstore.get_blob_key(dataCache)
    file_reader = blobstore.BlobReader(file_key)
    self.response.out.write('<html><body>')
    for i in range(0, 84):
        self.response.out.write(file_reader.readline() + "<br>")
    #print file_reader.readline()    

    """
            
    for o in organizations:
        org = Organization()
        org.worldCrises = wc
        org.id = o.get("id")
        org.name = o.find("name").text
        org.misc = o.find("misc").text
        org.put()
        
        oi = o.find("info")
        orgInfo = OrgInfo()
        orgInfo.organization = org
        orgInfo.type = oi.find("type").text
        orgInfo.history = oi.find("history").text
        orgInfo.put()
        
        c = oi.find("contact")
        contact = Contact()
        contact.orgInfo = orgInfo
        contact.phone = c.find("phone").text
        contact.email = c.find("email").text
        contact.put()
        
        fa = c.find("mail")
        fullAddr = FullAddr()
        fullAddr.contact = contact
        fullAddr.address = fa.find("address").text
        fullAddr.city = fa.find("city").text
        fullAddr.state = fa.find("state").text
        fullAddr.country = fa.find("country").text
        fullAddr.zip = fa.find("zip").text
        fullAddr.put()
        
        l = oi.find("loc")
        loc = Location()
        loc.orgInfo = orgInfo
        loc.city = l.find("city").text
        loc.region = l.find("region").text
        loc.country = l.find("country").text
        loc.put()
        
        r = o.find("ref")
        
        pi = r.find("primaryImage")
        piRef = ExternalLink()
        piRef.organization = org
        piRef.ref_type = "primaryImage"
        piRef.site = pi.find("site").text
        piRef.title = pi.find("title").text
        piRef.url = pi.find("url").text
        piRef.description = pi.find("description").text
        piRef.put()
        
        image = r.findall("image")
        for i in image:
            ref = ExternalLink()
            ref.organization = org
            ref.ref_type = "image"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()      
            
        v = r.findall("video")
        for i in v:
            ref = ExternalLink()
            ref.organization = org
            ref.ref_type = "video"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
            
        s = r.findall("social")
        for i in s:
            ref = ExternalLink()
            ref.organization = org
            ref.ref_type = "social"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()  
    
        e = r.findall("ext")
        for i in e:
            ref = ExternalLink()
            ref.organization = org
            ref.ref_type = "ext"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
            
    for p in people :
        person = Person()
        person.worldCrises = wc
        person.id = p.get("id")
        person.name = p.find("name").text
        person.misc = p.find("misc").text
        person.put()
        
        pi = p.find("info")
        pInfo = PersonInfo()
        pInfo.person = person
        pInfo.type = pi.find("type").text
        pInfo.nationality = pi.find("nationality").text
        pInfo.biography = pi.find("biography").text
        pInfo.put()
        
        bd = pi.find("birthdate")
        birthDate = Date()
        birthDate.personInfo = pInfo
        birthDate.time = bd.find("time").text
        birthDate.day = int(bd.find("day").text)
        birthDate.month = int(bd.find("month").text)
        birthDate.year = int(bd.find("year").text)
        birthDate.misc = bd.find("misc").text
        birthDate.put()
        
        r = p.find("ref")
        
        pi = r.find("primaryImage")
        piRef = ExternalLink()
        piRef.person = person
        piRef.ref_type = "primaryImage"
        piRef.site = pi.find("site").text
        piRef.title = pi.find("title").text
        piRef.url = pi.find("url").text
        piRef.description = pi.find("description").text
        piRef.put()
        
        image = r.findall("image")
        for i in image:
            ref = ExternalLink()
            ref.person = person
            ref.ref_type = "image"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()      
            
        v = r.findall("video")
        for i in v:
            ref = ExternalLink()
            ref.person = person
            ref.ref_type = "video"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
            
        s = r.findall("social")
        for i in s:
            ref = ExternalLink()
            ref.person = person
            ref.ref_type = "social"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()  
    
        e = r.findall("ext")
        for i in e:
            ref = ExternalLink()
            ref.person = person
            ref.ref_type = "ext"
            ref.site = i.find("site").text
            ref.title = i.find("title").text
            ref.url = i.find("url").text
            ref.description = i.find("description").text
            ref.put()
    
    for c in crises :
        crisis = Crisis.all().filter("id =", c.get("id")).fetch(1).pop()
        
        relatedOrg = c.findall("org")
        for o in relatedOrg :
            org = Organization.all().filter("id =", o.get("idref")).fetch(1).pop()
            relation = CrisisOrganization()
            relation.organization = crisis
            relation.crisis = org
            relation.put()
            
        relatedPerson = c.findall("person")
        for p in relatedPerson :
            person = Person.all().filter("id =", p.get("idref")).fetch(1).pop()
            relation = CrisisPerson()
            relation.crisis = person
            relation.person = crisis
            relation.put()
            
    for o in organizations :
        org = Organization.all().filter("id =", o.get("id")).fetch(1).pop()
    
        relatedPerson = o.findall("person")
        for p in relatedPerson :
            person = Person.all().filter("id =", p.get("idref")).fetch(1).pop()
            relation = OrganizationPerson()
            relation.organization = person
            relation.person = org
            relation.put()
     
    
        
    with files.open(db_txt, 'a') as f:
        f.write("second write\n")           
    files.finalize(db_txt)
    
    file_key = files.blobstore.get_blob_key(db_txt)
    file_reader = blobstore.BlobReader(file_key)
    print file_reader.readline()
    print file_reader.readline()
    
    
    
    self.redirect('/')
"""
class ExportHandler(webapp.RequestHandler):
    def get(self):
        CrisisQuery = Crisis.all().fetch(None)
        OrgQuery = Organization.all().fetch(None)
        PeopleQuery = Person.all().fetch(None)
        COQuery = CrisisOrganization.all().fetch(None)
        CPQuery = CrisisPerson.all().fetch(None)
        OPQuery = OrganizationPerson.all().fetch(None)

        crisisList = []
        orgList = []
        personList = []
        
        for c in CrisisQuery :
            clist = [c]
            cinfo = c.info.fetch(None).pop()
            clist.append(cinfo)
            clist.append(cinfo.time.fetch(None).pop())
            clist.append(cinfo.location.fetch(None).pop())
            clist.append(cinfo.humanImpact.fetch(None).pop())
            clist.append(cinfo.economicImpact.fetch(None).pop())
            reflist = c.ref.fetch(None)
            for pi in reflist :
                if pi.ref_type == 'primaryImage' :
                    clist.append(pi)
            images = []
            for i in reflist :
                if i.ref_type == 'image' :
                    images.append(i)
            clist.append(images)
            videos = []
            for v in reflist :
                if v.ref_type == 'video' :
                    videos.append(v)
            clist.append(videos)
            socials = []
            for s in reflist :
                if s.ref_type == 'social' :
                    socials.append(s)
            clist.append(socials)
            exts = []
            for e in reflist :
                if e.ref_type == 'ext' :
                    exts.append(e)
            clist.append(exts)
            colist = []
            for co in COQuery :
                if co.organization.name == c.name :
                    colist.append(co.crisis)
            clist.append(colist)
            cplist = []
            for cp in CPQuery : 
                if cp.person.name == c.name :
                    cplist.append(cp.crisis)
            clist.append(cplist)

            crisisList.append(clist)
            
        for o in OrgQuery :
            olist = [o]
            oinfo = o.info.fetch(None).pop()
            olist.append(oinfo)
            ocontact = oinfo.contact.fetch(None).pop()
            olist.append(ocontact)
            olist.append(ocontact.mail.fetch(None).pop())
            olist.append(oinfo.location.fetch(None).pop())
            reflist = o.ref.fetch(None)
            for pi in reflist :
                if pi.ref_type == 'primaryImage' :
                    olist.append(pi)
            images = []
            for i in reflist :
                if i.ref_type == 'image' :
                    images.append(i)
            olist.append(images)
            videos = []
            for v in reflist :
                if v.ref_type == 'video' :
                    videos.append(v)
            olist.append(videos)
            socials = []
            for s in reflist :
                if s.ref_type == 'social' :
                    socials.append(s)
            olist.append(socials)
            exts = []
            for e in reflist :
                if e.ref_type == 'ext' :
                    exts.append(e)
            olist.append(exts)
            colist = []
            for co in COQuery :
                if co.crisis.name == o.name :
                    colist.append(co.organization)
            olist.append(colist)
            oplist = []
            for op in OPQuery :
                if op.person.name == o.name :
                    oplist.append(op.organization)
            olist.append(oplist)
            orgList.append(olist)
            
        for p in PeopleQuery :
            plist = [p]
            pinfo = p.info.fetch(None).pop()
            plist.append(pinfo)
            plist.append(pinfo.birthdate.fetch(None).pop())
            reflist = p.ref.fetch(None)
            for pi in reflist :
                if pi.ref_type == 'primaryImage' :
                    plist.append(pi)
            images = []
            for i in reflist :
                if i.ref_type == 'image' :
                    images.append(i)
            plist.append(images)
            videos = []
            for v in reflist :
                if v.ref_type == 'video' :
                    videos.append(v)
            plist.append(videos)
            socials = []
            for s in reflist :
                if s.ref_type == 'social' :
                    socials.append(s)
            plist.append(socials)
            exts = []
            for e in reflist :
                if e.ref_type == 'ext' :
                    exts.append(e)
            plist.append(exts)
            cplist = []
            for cp in CPQuery :
                if cp.crisis.name == p.name :
                    cplist.append(cp.person)
            plist.append(cplist)   
            oplist = []
            for op in OPQuery :
                if op.organization.name == p.name :
                    oplist.append(op.person)
            plist.append(oplist)
            personList.append(plist)
        
        path2 = os.path.join(os.path.dirname(__file__), 'export.xml')
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write(template.render(path2, {"crises": crisisList, "orgs" : orgList, "persons" : personList},'text/xml'))
        

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
    
    
class WorldCrises (db.Model):
    #crises
    #organizations
    #persons
    countCrisis = db.IntegerProperty()
    countOrg = db.IntegerProperty()
    countPerson = db.IntegerProperty()
    
    
class Crisis (db.Model):
    worldCrises = db.ReferenceProperty(WorldCrises , collection_name = 'crises')
    id = db.StringProperty()
    name = db.StringProperty()
    #info
    #ref
    misc = db.StringProperty()
    
class Organization(db.Model):
    worldCrises  = db.ReferenceProperty(WorldCrises, collection_name = 'organizations')
    id = db.StringProperty()
    name = db.StringProperty()
    #info
    #ref  
    misc = db.StringProperty()
    
class Person(db.Model):
    worldCrises  = db.ReferenceProperty(WorldCrises, collection_name = 'persons')
    id = db.StringProperty()
    name = db.StringProperty()
    #info
    #ref
    misc = db.StringProperty()
    
class CrisisInfo (db.Model):
    crisis = db.ReferenceProperty(Crisis, collection_name = 'info')
    history = db.TextProperty()
    help = db.TextProperty()
    resources = db.TextProperty()
    type = db.StringProperty() 
    #time
    #location
    #humanImpact
    #economicImpact
    
class OrgInfo (db.Model):
    organization = db.ReferenceProperty(Organization, collection_name = 'info')
    type = db.StringProperty()
    history = db.TextProperty() 
    #contact
    #location
    
class PersonInfo (db.Model):
    person = db.ReferenceProperty(Person, collection_name = 'info')
    type = db.StringProperty()
    #birthdate
    nationality = db.StringProperty() 
    biography = db.TextProperty()

    
class ExternalLink (db.Model):
    crisis = db.ReferenceProperty(Crisis, collection_name = 'ref')
    organization = db.ReferenceProperty(Organization, collection_name = 'ref')
    person = db.ReferenceProperty(Person, collection_name = 'ref')
    ref_type = db.StringProperty(choices=('primaryImage', 'image', 'video', 'social', 'ext'))
    site = db.StringProperty()
    title = db.StringProperty()
    url = db.StringProperty()
    description = db.StringProperty()
    
    
class Date(db.Model):
    crisisInfo = db.ReferenceProperty(CrisisInfo, collection_name = 'time')
    personInfo = db.ReferenceProperty(PersonInfo, collection_name = 'birthdate')
    time = db.StringProperty()
    day = db.IntegerProperty()
    month = db.IntegerProperty()
    year = db.IntegerProperty()
    misc = db.StringProperty()
    
class Location (db.Model):
    crisisInfo = db.ReferenceProperty(CrisisInfo, collection_name = 'location')
    orgInfo = db.ReferenceProperty(OrgInfo, collection_name = 'location')
    city = db.StringProperty()
    region = db.StringProperty()
    country = db.StringProperty() 

class Contact (db.Model):
    orgInfo = db.ReferenceProperty(OrgInfo, collection_name = 'contact')
    phone = db.StringProperty()
    email = db.StringProperty()
    #mail
           
class FullAddr (db.Model):
    contact = db.ReferenceProperty(Contact, collection_name = 'mail')
    address = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    zip = db.StringProperty()

class HumanImpact (db.Model):
    crisisInfo = db.ReferenceProperty(CrisisInfo, collection_name = 'humanImpact')
    deaths = db.IntegerProperty()
    displaced = db.IntegerProperty()
    injured = db.IntegerProperty()
    missing = db.IntegerProperty()
    misc = db.StringProperty()
    
class EconomicImpact (db.Model):
    crisisInfo = db.ReferenceProperty(CrisisInfo, collection_name = 'economicImpact')
    amount = db.IntegerProperty()
    currency = db.StringProperty()
    misc = db.StringProperty()
    
class CrisisOrganization (db.Model):
    crisis = db.ReferenceProperty(Organization, collection_name = 'orgCrisis')
    organization = db.ReferenceProperty(Crisis, collection_name = 'crisisOrg')

class CrisisPerson (db.Model):
    crisis = db.ReferenceProperty(Person, collection_name = 'personCrisis')
    person = db.ReferenceProperty(Crisis, collection_name = 'crisisPerson')
    
class OrganizationPerson (db.Model):
    organization = db.ReferenceProperty(Person, collection_name = 'personOrg')
    person = db.ReferenceProperty(Organization, collection_name = 'orgPerson')

class dataCacheKey (db.Model):
    blob_id = blobstore.BlobReferenceProperty()
    
app = webapp2.WSGIApplication([('/', MainPage), ('/import', ImportHandler), ('/upload', UploadHandler),
                            ('/serve/([^/]+)?', ServeHandler), ('/export', ExportHandler), 
                            ('/temp_upload', TempUploadHandler),
                            ('/search_result', SearchResultHandler),
                            ('/crisis/([^/]+)?', CrisisHandler),
                            ('/org/([^/]+)?', OrgHandler), 
                            ('/person/([^/]+)?', PersonHandler),
                            ('/temp', TempHandler),
                            ('/crisis', CrisisDisplayHandler),
                            ('/org', OrgDisplayHandler),
                            ('/person', PersonDisplayHandler)], debug=True)

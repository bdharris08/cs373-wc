import webapp2
import jinja2
import os
import urllib

from genxmlif import GenXmlIfError
from minixsv import pyxsval


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    
from xml.etree.ElementTree import ElementTree
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app



class MainPage(webapp2.RequestHandler):
    def get(self):
        # wc = WorldCrisis.all()
        # counts
        qCrises = Crisis.all()
        crises = qCrises.fetch(4)
        
        path = os.path.join(os.path.dirname(__file__), 'splash.html')
        self.response.out.write(template.render(path, {"crises": crises}))
        
        #template = jinja_environment.get_template('splash.html')
        #self.response.out.write(template.render())

class CrisisHandler(webapp2.RequestHandler):
    def get(self):
        
        path = os.path.join(os.path.dirname(__file__), 'crisisTemp.html')
        self.response.out.write(template.render(path, {}))
        
class tibet(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('crisis-Tibet.html')
        self.response.out.write(template.render())
        
class gec(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('crisis-GlobalFinancialCrisis.html')
        self.response.out.write(template.render())
        
class bathsalts(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('crisis-BathSalts.html')
        self.response.out.write(template.render())
        
class nkorea(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('crisis-NorthKorea.html')
        self.response.out.write(template.render())

class un(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('org-UN.html')
        self.response.out.write(template.render())

class frs(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('org-FRS.html')
        self.response.out.write(template.render())

class dea(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('org-DEA.html')
        self.response.out.write(template.render())

class dod(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('org-DepartmentOfDefense.html')
        self.response.out.write(template.render())

class dali(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('person_dalailama.html')
        self.response.out.write(template.render())

class mml(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('person_leonhart.html')
        self.response.out.write(template.render())

class obama(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('person_BarackObama.html')
        self.response.out.write(template.render())
        
class kju(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('person_KimJungUn.html')
        self.response.out.write(template.render())
        
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
    
    wc = WorldCrises()
    wc.put()
    
    for c in crises:
        
        crisis = Crisis()
        crisis.worldCrises = wc
        crisis.id = c.get("id")
        crisis.name = c.find("name").text
        crisis.put()
        #print "dummy"
        #print "id: " + crisis.id
        #print "name: " + crisis.name
        
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
        location.crsisInfo = crisisInfo
        location.city = l.find("city").text
        location.region = l.find("region").text
        location.country = l.find("country").text
        location.put()
        
        i = ci.find("impact")
        
        hi = i.find("human")
        humanImpact = HumanImpact()
        humanImpact.deaths = int(hi.find("deaths").text)
        humanImpact.displaced = int(hi.find("displaced").text)
        humanImpact.injured = int(hi.find("injured").text)
        humanImpact.missing = int(hi.find("missing").text)
        humanImpact.misc = hi.find("misc").text
        humanImpact.put()
        
        ei = i.find("economic")
        economicImpact = EconomicImpact()
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
        
        fa = c.find("fulladdrType")
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
        
        pi = p.find("personInfoType")
        pInfo = PersonInfo()
        pInfo.person = person
        pInfo.type = pi.find("type").text
        pInfo.nationality = pi.find("nationality").text
        pInfo.biography = pi.find("biography").text
        pInfo.put()
        
        bd = pi.find("dateType")
        birthDate = Date()
        birthDate.personInfo = pInfo
        birthDate.time = bd.find("time").text
        birthDate.day = bd.find("day").text
        birthDate.month = bd.find("month").text
        birthDate.year = bd.find("year").text
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

    #self.redirect('/serve/%s' % blob_info.key())
    #blobkey = blob_info.key()
    self.redirect('/')

class ExportHandler(webapp.RequestHandler):
    def get(self):
        CrisisQuery = Crisis.all().fetch(1000)
        OrgQuery = Organization.all()
        PeopleQuery = Person.all()
        #tree = ElementTree()
        #treebuilder = tree.TreeBuilder()
        #build tree using models
        #write .xml file to blobstore using tree.write
        #redirect to servehandler to output
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<worldCrises>\n\t<crises>'
        for c in CrisisQuery:
            xml = xml + c.to_xml()
        #self.response.headers['Content-Type']='text/xml; charset=utf-8'
        #self.response.out.write(xml)
        #self.redirect('/serve/%s' % blob_info.key())
        BlobQuery = blobstore.BlobInfo.gql("Order BY creation DESC")
        blob = BlobQuery.get()
        self.redirect('/serve/%s' % blob.key())
        
        

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
    orgs = db.ListProperty(db.Key)
    person = db.ListProperty(db.Key)
    
class Organization(db.Model):
    worldCrises  = db.ReferenceProperty(WorldCrises, collection_name = 'organizations')
    id = db.StringProperty()
    name = db.StringProperty()
    #info
    #ref  
    misc = db.StringProperty()
    crisis = db.ListProperty(db.Key)
    person = db.ListProperty(db.Key)
    
class Person(db.Model):
    worldCrises  = db.ReferenceProperty(WorldCrises, collection_name = 'persons')
    id = db.StringProperty()
    name = db.StringProperty()
    #info
    #ref
    misc = db.StringProperty()
    crisis = db.ListProperty(db.Key)
    org = db.ListProperty(db.Key)
    
class CrisisInfo (db.Model):
    crisis = db.ReferenceProperty(Crisis, collection_name = 'info')
    history = db.StringProperty()
    help = db.StringProperty()
    resources = db.StringProperty()
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
    biography = db.StringProperty()

    
class ExternalLink (db.Model):
    crisis = db.ReferenceProperty(Crisis, collection_name = 'ref')
    organization = db.ReferenceProperty(Organization, collection_name = 'ref')
    person = db.ReferenceProperty(Person, collection_name = 'ref')
    ref_type = db.StringProperty(choices=('primaryImage', 'image', 'video', 'social', 'ext'))
    site = db.StringProperty()
    title = db.StringProperty()
    url = db.LinkProperty()
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
    


app = webapp2.WSGIApplication([('/', MainPage), ('/tibet', tibet), ('/gec', gec), 
							('/bathsalts', bathsalts), ('/nkorea', nkorea), ('/un', un), 
							('/frs', frs), ('/dea', dea), ('/dod', dod), 
							('/dali', dali), ('/mml', mml), ('/obama', obama), 
							('/kju', kju), ('/import', ImportHandler), ('/upload', UploadHandler),
                            ('/serve/([^/]+)?', ServeHandler), ('/export', ExportHandler)], 
                            ('/crisis/([^/]+)?', CrisisHandler),debug=True)

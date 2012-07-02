import webapp2
import jinja2
import os
import urllib


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
        template = jinja_environment.get_template('splash.html')
        self.response.out.write(template.render())
        
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
    tree = ElementTree()
    assert blob_info.content_type == "text/xml"
    tree.parse(blob_reader)

    
    crises = tree.findall("crises/crisis")
    organizations = tree.findall("organizations/organization")
    people = tree.findall("people/person")
    
    c1 = Crisis()
    c2 = Crisis()
    c3 = Crisis()
    c4 = Crisis()
    clist = [c1, c2, c3, c4]
    o1 = Organization()
    o2 = Organization()
    o3 = Organization()
    o4 = Organization()
    olist = [o1, o2, o3, o4]
    p1 = Person()
    p2 = Person()
    p3 = Person()
    p4 = Person()
    plist = [p1,p2,p3,p4]
    
    count = 0
    for c in crises:
        it = c.iter()
        clist[count].id = it.next().get("id")
        clist[count].name = it.next().text
        clist[count].kindd = it.next().text
        clist[count].description = it.next().text
        clist[count].date = it.next().text
        clist[count].location = it.next().text
        clist[count].humanImpact = it.next().text
        clist[count].economicImpact = it.next().text
        clist[count].resourceNeeded = it.next().text
        clist[count].wayToHelp = it.next().text
        images = Images()
        videos = Videos()
        socials = Socials()
        extLinks = ExtLinks()
        while(True):
            x = it.next().text
            if (x == "image"):
                images.urls.append(it.next().text)
                images.titles.append(it.next().text)
            elif (x == "video"):
                videos.urls.append(it.next().text)
                videos.titles.append(it.next().text)
            elif (x == "social"):
                socials.urls.append(it.next().text)
                socials.titles.append(it.next().text)
            elif (x == "extLink"):
                extLinks.urls.append(it.next().text)
                extLinks.titles.append(it.next().text)
            else :
                images.put()
                videos.put()
                socials.put()
                extLinks.put()
                clist[count].organizationRef = x
                clist[count].personRef = it.next().text
                break
                
        clist[count].images = images
        clist[count].videos = videos
        clist[count].socials = socials
        clist[count].extLinks = extLinks
        count+= 1
    
    count = 0            
    for o in organizations:
        it = o.iter()
        olist[count].id = it.next().get("id")
        olist[count].name = it.next().text
        olist[count].kindd = it.next().text
        olist[count].description = it.next().text
        olist[count].dateFounded = it.next().text
        olist[count].location = it.next().text
        olist[count].humanImpact = it.next().text
        olist[count].economicImpact = it.next().text
        olist[count].resourceNeeded = it.next().text
        olist[count].wayToHelp = it.next().text
        images = Images()
        videos = Videos()
        socials = Socials()
        extLinks = ExtLinks()
        while(True):
            x = it.next().text
            if (x == "image"):
                images.urls.append(it.next().text)
                images.titles.append(it.next().text)
            elif (x == "video"):
                videos.urls.append(it.next().text)
                videos.titles.append(it.next().text)
            elif (x == "social"):
                socials.urls.append(it.next().text)
                socials.titles.append(it.next().text)
            elif (x == "extLink"):
                extLinks.urls.append(it.next().text)
                extLinks.titles.append(it.next().text)
            else :
                images.put()
                videos.put()
                socials.put()
                extLinks.put()
                olist[count].crisisRef = x
                olist[count].personRef = it.next().text
                break
                
        olist[count].images = images
        olist[count].videos = videos
        olist[count].socials = socials
        olist[count].extLinks = extLinks
        count+= 1
        
    count = 0   
    for p in people:
        it = p.iter()
        plist[count].id = it.next().get("id")
        plist[count].name = it.next().text
        plist[count].birthday = it.next().text
        plist[count].nationality = it.next().text
        plist[count].description = it.next().text
        images = Images()
        videos = Videos()
        socials = Socials()
        extLinks = ExtLinks()
        while(True):
            x = it.next().text
            if (x == "image"):
                images.urls.append(it.next().text)
                images.titles.append(it.next().text)
            elif (x == "video"):
                videos.urls.append(it.next().text)
                videos.titles.append(it.next().text)
            elif (x == "social"):
                socials.urls.append(it.next().text)
                socials.titles.append(it.next().text)
            elif (x == "extLink"):
                extLinks.urls.append(it.next().text)
                extLinks.titles.append(it.next().text)
            else :
                images.put()
                videos.put()
                socials.put()
                extLinks.put()
                plist[count].crisisRef = x
                plist[count].personRef = it.next().text
                break
                
        plist[count].images = images
        plist[count].videos = videos
        plist[count].socials = socials
        plist[count].extLinks = extLinks
        count+= 1
        
    #put all the models
    c1.put()
    c2.put()
    c3.put()
    c4.put()
    o1.put()
    o2.put()
    o3.put()
    o4.put()
    p1.put()
    p2.put()
    p3.put()
    p4.put()
    
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
    

class Images (db.Model):
    urls = db.ListProperty(str)
    titles = db.ListProperty(str)
    
class Videos (db.Model):
    urls = db.ListProperty(str)
    titles = db.ListProperty(str)
    
class Socials (db.Model):
    urls = db.ListProperty(str)
    titles = db.ListProperty(str)
    
class ExtLinks (db.Model):
    urls = db.ListProperty(str)
    titles = db.ListProperty(str)

    
class Crisis (db.Model):
    id = db.StringProperty()
    name = db.StringProperty()
    kindd = db.StringProperty()
    decription = db.TextProperty()
    date = db.StringProperty()
    location = db.StringProperty()
    humanImpact = db.StringProperty()
    economicImpact = db.StringProperty()
    resourceNeeded = db.StringProperty()
    wayToHelp = db.StringProperty()
    images = db.ReferenceProperty(reference_class=Images) 
    videos = db.ReferenceProperty(reference_class=Videos)
    socials = db.ReferenceProperty(reference_class=Socials)
    extLinks = db.ReferenceProperty(reference_class=ExtLinks)
    organizationRef = db.TextProperty()
    personRef = db.TextProperty()
    
class Organization(db.Model):
    id = db.StringProperty()
    name = db.StringProperty()
    kindd = db.StringProperty()
    description = db.TextProperty()
    relationToCrisis = db.TextProperty()
    dateFounded = db.StringProperty()
    location = db.StringProperty()
    images = db.ReferenceProperty(reference_class=Images) 
    videos = db.ReferenceProperty(reference_class=Videos)
    socials = db.ReferenceProperty(reference_class=Socials)
    extLinks = db.ReferenceProperty(reference_class=ExtLinks)
    cririsRef = db.TextProperty()
    personRef = db.TextProperty()
    
class Person(db.Model):
    id = db.StringProperty()
    name = db.StringProperty()
    birthday = db.StringProperty()
    nationality = db.StringProperty()
    description = db.TextProperty()
    images = db.ReferenceProperty(reference_class=Images) 
    videos = db.ReferenceProperty(reference_class=Videos)
    socials = db.ReferenceProperty(reference_class=Socials)
    extLinks = db.ReferenceProperty(reference_class=ExtLinks)
    crisisRef = db.TextProperty()
    organizationRef = db.TextProperty()
    
    



app = webapp2.WSGIApplication([('/', MainPage), ('/tibet', tibet), ('/gec', gec), 
							('/bathsalts', bathsalts), ('/nkorea', nkorea), ('/un', un), 
							('/frs', frs), ('/dea', dea), ('/dod', dod), 
							('/dali', dali), ('/mml', mml), ('/obama', obama), 
							('/kju', kju), ('/import', ImportHandler), ('/upload', UploadHandler),
                            ('/serve/([^/]+)?', ServeHandler), ('/export', ExportHandler)], debug=True)
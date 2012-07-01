import webapp2
import jinja2
import os
import urllib
import pprint


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    
from xml.etree.ElementTree import ElementTree
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import xmlToET

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
        
class MainHandler(webapp.RequestHandler):
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
    self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    #self.send_blob(blob_info)
    blob_reader = blob_info.open()
    tree = ElementTree()
    assert blob_info.content_type == "text/xml"
    tree.parse(blob_reader)
    
    crisis = tree.findall("crises/crisis")
    
    c1 = Crisis()
    c2 = Crisis()
    c3 = Crisis()
    c4 = Crisis()
    clist = [c1, c2, c3, c4]
    count = 0
    
    for c in crisis:
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
    personRef = db.StringProperty()
    
    



app = webapp2.WSGIApplication([('/', MainPage), ('/tibet', tibet), ('/gec', gec), 
							('/bathsalts', bathsalts), ('/nkorea', nkorea), ('/un', un), 
							('/frs', frs), ('/dea', dea), ('/dod', dod), 
							('/dali', dali), ('/mml', mml), ('/obama', obama), 
							('/kju', kju), ('/import', MainHandler), ('/upload', UploadHandler),
                            ('/serve/([^/]+)?', ServeHandler)], debug=True)
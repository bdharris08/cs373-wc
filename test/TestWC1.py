import unittest
import wc
from google.appengine.ext import db
from google.appengine.ext import webapp
import webapp2
from webtest import TestApp

class webTest(unittest.TestCase):
    def setUp(self):
        self.application = webapp2.WSGIApplication([('/', wc.MainPage), ('/tibet', wc.tibet), ('/gec', wc.gec), 
							('/bathsalts', wc.bathsalts), ('/nkorea', wc.nkorea), ('/un', wc.un), 
							('/frs', wc.frs), ('/dea', wc.dea), ('/dod', wc.dod), 
							('/dali', wc.dali), ('/mml', wc.mml), ('/obama', wc.obama), 
							('/kju', wc.kju), ('/import', wc.ImportHandler), ('/upload', wc.UploadHandler),
                            ('/serve/([^/]+)?', wc.ServeHandler), ('/export', wc.ExportHandler)], debug=True)

    def test_index(self):
        app = TestApp(self.application)
        response = app.get('/')
        self.assertTrue('Splash Page' in response)    
    
    def test_tibet(self):
        app = TestApp(self.application)
        response = app.get('/tibet')
        self.assertTrue('Crisis: Tibetan Occupation' in response) 
    
    def test_gec(self):
        app = TestApp(self.application)
        response = app.get('/gec')
        self.assertTrue('Crisis: Global Financial Crisis' in response)     
    def test_bathsalts(self):
        app = TestApp(self.application)
        response = app.get('/bathsalts')
        self.assertTrue('Crisis: Bath Salts' in response)     
    def test_nkorea(self):
        app = TestApp(self.application)
        response = app.get('/nkorea')
        self.assertTrue('North Korea and Nuclear Weapons' in response)     
    def test_UN(self):
        app = TestApp(self.application)
        response = app.get('/un')
        self.assertTrue('Organization: United Nations' in response) 
    def test_fed(self):
        app = TestApp(self.application)
        response = app.get('/frs')
        self.assertTrue('Organization: The Federal Reserve' in response)         
    
    def test_dea(self):
        app = TestApp(self.application)
        response = app.get('/dea')
        self.assertTrue('Organization: Drug Enforcement Administration' in response)         
    
    def test_dod(self):
        app = TestApp(self.application)
        response = app.get('/dod')
        self.assertTrue('United States Department of Defense' in response)
    
    def test_dalailama(self):
        app = TestApp(self.application)
        response = app.get('/dali')
        self.assertTrue('Person: Dalai Lama (Tenzin Gyatso)' in response)  
    
    def test_obama(self):
        app = TestApp(self.application)
        response = app.get('/obama')
        self.assertTrue('Person: President Barack Obama' in response)         
    
    def test_leonhart(self):
        app = TestApp(self.application)
        response = app.get('/mml')
        self.assertTrue('Person: Michele M. Leonhart' in response)  
    
    def test_kimjongun(self):
        app = TestApp(self.application)
        response = app.get('/kju')
        self.assertTrue('Person: Kim Jong-un' in response)
    '''    
    def test_import(self):
        app = TestApp(self.application)
        response = app.get('/import')
        self.assertTrue('Upload File' in response)         
    
    def test_export(self):
        app = TestApp(self.application)
        response = app.get('/export')
        self.assertTrue('<worldCrises>' in response)
    '''
   
       
class ModelTest(unittest.TestCase):
    def test_new_Images_entity(self):
        entity = wc.Images(urls = ["link"], titles = ["title"])
        self.assertTrue(entity.urls == ["link"])
        self.assertTrue(entity.titles == ["title"])
    
    def test_new_Videos_entity(self):
        entity = wc.Videos(urls = ["video"], titles = ["title", "title1"])
        self.assertTrue(entity.urls == ["video"])
        self.assertTrue(entity.titles[1] == "title1")
    
    def test_new_Socials_entity(self):
        entity = wc.Socials(urls = ["twitter.com"], titles = ["useless"])
        self.assertTrue(entity.urls == ["twitter.com"] and entity.titles[0] == "useless")
    
    def test_new_ExtLinks_entity(self):
        entity = wc.ExtLinks(urls = ["0", "1", "2", "3", "4"], titles = ["obamacare"])
        self.assertTrue(entity.urls[2] == "2" and entity.titles[0] == "obamacare")

    def test_new_Crisis_entity1(self):
        entity = wc.Crisis(name = "crisis", location = "location")
        self.assertTrue(entity.name == "crisis")
        self.assertTrue(entity.location == "location")
        
    def test_new_Crisis_entity2(self):
        entity = wc.Crisis(id = "tibet", kindd = "tibet")
        self.assertTrue(entity.id == "tibet")
        self.assertTrue(entity.kindd == "tibet")
           
    def test_new_Crisis_entity3(self):
        entity = wc.Crisis(date = "12/21/2012", humanImpact = "nothing really")
        self.assertTrue(entity.date == "12/21/2012")
        self.assertTrue(entity.humanImpact == "nothing really")
    
    def test_new_Org_entity1(self):
        entity = wc.Organization(id = "DEA", name = "Drug Enforcement Administration")
        self.assertTrue(entity.id == "DEA")
        self.assertTrue(entity.name == "Drug Enforcement Administration")
    
    def test_new_Org_entity2(self):
        entity = wc.Organization(kindd = "federal agency", dateFounded = "9/9/99")
        self.assertTrue(entity.kindd == "federal agency")
        self.assertTrue(entity.dateFounded == "9/9/99")
    
    def test_new_Org_entity3(self):
        entity = wc.Organization(location = "Virginia, USA")
        self.assertTrue(entity.location == "Virginia, USA")

    def test_new_Person_entity1(self):
    	entity = wc.Person(id = "Dalai", name = "Dalai Lama")
        self.assertTrue(entity.id == "Dalai")
        self.assertTrue(entity.name == "Dalai Lama")
    
    def test_new_person_entity2(self):
        entity = wc.Person(birthday = "July 6, 1935", nationality = "Tibet")
        self.assertTrue(entity.birthday == "July 6, 1935")
        self.assertTrue(entity.nationality == "Tibet")
        
    def test_new_person_entity3(self):
        entity = wc.Person(description = "14th and current head of Tibetan Buddhism")
        self.assertTrue(entity.description == "14th and current head of Tibetan Buddhism")
            

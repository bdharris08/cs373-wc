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
   
"""        
class ModelTest(unittest.TestCase):
    def test_new_Crisis_entity1(self):
        entity = model.Crisis()
        self.assertEqual('', entity.)
        
    def test_new_Crisis_entity2(self):
    
    def test_new_Crisis_entity3(self):
    
    def test_new_Org_entity1(self):
    
    def test_new_Org_entity2(self):
    
    def test_new_Org_entity3(self):
    
    def test_new_Person_entity1(self):
    
    def test_new_person_entity2(self):
    
    def test_new_person_entity3(self):"""
    
            

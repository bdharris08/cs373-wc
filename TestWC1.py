import unittest
import model
from google.appengine.ext import db
from google.appengine.ext import webapp

class webTest(unittest.TestCase):
    def setUp(self):
        self.application = webapp2.WSGIApplication([('/', MainPage), ('/tibet', tibet), ('/gec', gec), 
							('/bathsalts', bathsalts), ('/nkorea', nkorea), ('/un', un), 
							('/frs', frs), ('/dea', dea), ('/dod', dod), 
							('/dali', dali), ('/mml', mml), ('/obama', obama), 
							('/kju', kju), ('/import', ImportHandler), ('/upload', UploadHandler),
                            ('/serve/([^/]+)?', ServeHandler), ('/export', ExportHandler)], debug=True)
    
    def test_index(self):
        app = TestApp(self.application)
        response = app.get('/')
        self.assertTrue('Splash Page' in response)    
    
    def test_tibet(self):
    
    def test_gec(self):
    
    def test_bathsalts(self):
    
    def test_nkorea(self):
    
    def test_UN(self):
    
    def test_fed(self):
    
    def test_dea(self):
    
    def test_dod(self):
    
    def test_dalailama(self):
    
    def test_obama(self):
    
    def test_leonhart(self):
    
    def test_kimjongun(self):
    
    def test_import(self):
    
    def test_export(self):

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
    
    def test_new_person_entity3(self):
    
            
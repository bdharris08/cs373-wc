from __future__ import with_statement
import unittest
import wc
from StringIO import StringIO
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import files
import webapp2
from webtest import TestApp

class webTest(unittest.TestCase):
    def setUp(self):
        self.application = webapp2.WSGIApplication([('/', wc.MainPage), ('/import', wc.ImportHandler), ('/upload', wc.UploadHandler),
                            ('/serve/([^/]+)?', wc.ServeHandler), ('/export', wc.ExportHandler), 
                            ('/crisis/([^/]+)?', wc.CrisisHandler),
                            ('/org/([^/]+)?', wc.OrgHandler), 
                            ('/person/([^/]+)?', wc.PersonHandler),
                            ('/temp', wc.TempHandler),
                            ('/crisis', wc.CrisisDisplayHandler),
                            ('/org', wc.OrgDisplayHandler),
                            ('/person', wc.PersonDisplayHandler)], debug=True)
        

    def test_index(self):
        app = TestApp(self.application)
        wc.WorldCrises().put()
        wc.Crisis(id = "bath_salts", name = "Bath Salts").put()
        wc.Organization(id = "drug_enforcement_admin", name = "Drug Enforcement Administration").put()
        wc.Person(id = "michele_leonhart", name = "Michele M. Leonhart").put()
        response = app.get('/')
        self.assertTrue('' in response)    
    
    def test_tibet(self):
        app = TestApp(self.application)
        crisis = wc.Crisis(id = "tibet", name = "Tibetan Occupation").put()
        crisisInfo = wc.CrisisInfo(crisis = crisis).put()
        wc.ExternalLink(crisis = crisis).put()
        wc.Date(crisisInfo = crisisInfo).put()
        wc.Location(crisisInfo = crisisInfo).put()
        wc.HumanImpact(crisisInfo = crisisInfo).put()
        wc.EconomicImpact(crisisInfo = crisisInfo).put()
        response = app.get('/crisis/tibet')
        self.assertTrue('Tibetan Occupation' in response) 
    
    def test_gec(self):
        app = TestApp(self.application)
        crisis = wc.Crisis(id = "global_economic_crisis", name = "Global Financial Crisis").put()
        crisisInfo = wc.CrisisInfo(crisis = crisis).put()
        wc.ExternalLink(crisis = crisis).put()
        wc.Date(crisisInfo = crisisInfo).put()
        wc.Location(crisisInfo = crisisInfo).put()
        wc.HumanImpact(crisisInfo = crisisInfo).put()
        wc.EconomicImpact(crisisInfo = crisisInfo).put()
        response = app.get('/crisis/global_economic_crisis')
        self.assertTrue('Global Financial Crisis' in response)     
    def test_bathsalts(self):
        app = TestApp(self.application)
        crisis = wc.Crisis(id = "bath_salts", name = "Bath Salts").put()
        crisisInfo = wc.CrisisInfo(crisis = crisis).put()
        wc.ExternalLink(crisis = crisis).put()
        wc.Date(crisisInfo = crisisInfo).put()
        wc.Location(crisisInfo = crisisInfo).put()
        wc.HumanImpact(crisisInfo = crisisInfo).put()
        wc.EconomicImpact(crisisInfo = crisisInfo).put()
        response = app.get('/crisis/bath_salts')
        self.assertTrue('Bath Salts' in response)     
    def test_nkorea(self):
        app = TestApp(self.application)
        crisis = wc.Crisis(id = "north_korea", name = "North Korea and Nuclear Weapons").put()
        crisisInfo = wc.CrisisInfo(crisis = crisis).put()
        wc.ExternalLink(crisis = crisis).put()
        wc.Date(crisisInfo = crisisInfo).put()
        wc.Location(crisisInfo = crisisInfo).put()
        wc.HumanImpact(crisisInfo = crisisInfo).put()
        wc.EconomicImpact(crisisInfo = crisisInfo).put()
        response = app.get('/crisis/north_korea')
        self.assertTrue('North Korea and Nuclear Weapons' in response)     
    def test_UN(self):
        app = TestApp(self.application)
        org = wc.Organization(id = "united_nations", name = "United Nations").put()
        orgInfo = wc.OrgInfo(organization = org).put()
        wc.ExternalLink(organization = org).put()
        contact = wc.Contact(orgInfo = orgInfo).put()
        wc.FullAddr(contact = contact).put()
        wc.Location(orgInfo = orgInfo).put()
        response = app.get('/org/united_nations')
        self.assertTrue('United Nations' in response) 
    def test_fed(self):
        app = TestApp(self.application)
        org = wc.Organization(id = "federal_reserve_system", name = "The Federal Reserve").put()
        orgInfo = wc.OrgInfo(organization = org).put()
        wc.ExternalLink(organization = org).put()
        contact = wc.Contact(orgInfo = orgInfo).put()
        wc.FullAddr(contact = contact).put()
        wc.Location(orgInfo = orgInfo).put()
        response = app.get('/org/federal_reserve_system')
        self.assertTrue('The Federal Reserve' in response)         
    
    def test_dea(self):
        app = TestApp(self.application)
        org = wc.Organization(id = "drug_enforcement_admin", name = "Drug Enforcement Administration").put()
        orgInfo = wc.OrgInfo(organization = org).put()
        wc.ExternalLink(organization = org).put()
        contact = wc.Contact(orgInfo = orgInfo).put()
        wc.FullAddr(contact = contact).put()
        wc.Location(orgInfo = orgInfo).put()
        response = app.get('/org/drug_enforcement_admin')
        self.assertTrue('Drug Enforcement Administration' in response)         
    
    def test_dod(self):
        app = TestApp(self.application)
        org = wc.Organization(id = "department_of_defense", name = "United States Department of Defense").put()
        orgInfo = wc.OrgInfo(organization = org).put()
        wc.ExternalLink(organization = org).put()
        contact = wc.Contact(orgInfo = orgInfo).put()
        wc.FullAddr(contact = contact).put()
        wc.Location(orgInfo = orgInfo).put()
        response = app.get('/org/department_of_defense')
        self.assertTrue('United States Department of Defense' in response)
    
    def test_dalailama(self):
        app = TestApp(self.application)
        person = wc.Person(id = "dalai_lama", name = "Dalai Lama (Tenzin Gyatso)").put()
        personInfo = wc.PersonInfo(person = person).put()
        wc.Date(personInfo = personInfo).put()
        wc.ExternalLink(person = person).put()
        response = app.get('/person/dalai_lama')
        self.assertTrue('Dalai Lama (Tenzin Gyatso)' in response)  
    
    def test_obama(self):
        app = TestApp(self.application)
        person = wc.Person(id = "barack_obama", name = "President Barack Obama").put()
        personInfo = wc.PersonInfo(person = person).put()
        wc.Date(personInfo = personInfo).put()
        wc.ExternalLink(person = person).put()
        response = app.get('/person/barack_obama')
        self.assertTrue('President Barack Obama' in response)         
    
    def test_leonhart(self):
        app = TestApp(self.application)
        person = wc.Person(id = "michele_leonhart", name = "Michele M. Leonhart").put()
        personInfo = wc.PersonInfo(person = person).put()
        wc.Date(personInfo = personInfo).put()
        wc.ExternalLink(person = person).put()
        response = app.get('/person/michele_leonhart')
        self.assertTrue('Michele M. Leonhart' in response)  
    
    def test_kimjongun(self):
        app = TestApp(self.application)
        person = wc.Person(id = "kim_jong_un", name = "Kim Jong-un").put()
        personInfo = wc.PersonInfo(person = person).put()
        wc.Date(personInfo = personInfo).put()
        wc.ExternalLink(person = person).put()
        response = app.get('/person/kim_jong_un')
        self.assertTrue('Kim Jong-un' in response)
    

    """def test_ImportHandler(self):
        app = TestApp(self.application)
        response = app.get('/import')
        self.assertTrue('Upload File' in response) 
    
    def test_UploadHandler(self):
        app = TestApp(self.application)
        
    '''
    def test_export(self):
        app = TestApp(self.application)
        response = app.get('/export')
        self.assertTrue('<worldCrises>' in response)''' """

   
       
class ModelTest(unittest.TestCase):
    def test_new_Crisis_entity1(self):
        entity = wc.Crisis(name = "crisis")
        self.assertTrue(entity.name == "crisis")
        
    def test_new_Crisis_entity2(self):
        entity = wc.Crisis(id = "tibet")
        self.assertTrue(entity.id == "tibet")
           
    def test_new_Crisis_entity3(self):
        entity = wc.Crisis(misc = "nothing really")
        self.assertTrue(entity.misc == "nothing really")
    
    def test_new_Org_entity1(self):
        entity = wc.Organization(id = "DEA", name = "Drug Enforcement Administration")
        self.assertTrue(entity.id == "DEA")
        self.assertTrue(entity.name == "Drug Enforcement Administration")
    
    def test_new_Org_entity2(self):
        entity = wc.Organization(misc = "nothing really")
        self.assertTrue(entity.misc == "nothing really")

    def test_new_Person_entity1(self):
    	entity = wc.Person(id = "Dalai", name = "Dalai Lama")
        self.assertTrue(entity.id == "Dalai")
        self.assertTrue(entity.name == "Dalai Lama")


import threading
import psycopg2
from selenium.webdriver.common.by import By
import pathlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

class Vmesnik():
    def __init__(self):
        pot = pathlib.Path().absolute()
        WEB_DRIVER_LOCATION = str(pot) + "\..\chromedriver.exe"
        lastnosti = Options()
        lastnosti.add_argument("--headless")
        self.vmesnik = webdriver.Chrome(WEB_DRIVER_LOCATION, options=lastnosti)

    def poisci_povezave(self):
        #self.vmesnik.get(povezava)
        povezave = self.vmesnik.find_elements("xpath", "//*[@href]")
        #TREBA JIH BO OBDELAT
        return povezave
    
    def poisci_slike(self):
        #self.vmesnik.get(povezava)
        slike = self.vmesnik.find_elements("xpath", "//*[@href]")
        #TREBA JIH BO OBDELAT
        return slike
    
    def odpri_stran(self, povezava):
        self.vmesnik.get(povezava)
        return
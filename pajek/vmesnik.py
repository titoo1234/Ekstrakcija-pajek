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
        povezave = self.vmesnik.find_elements(By.TAG_NAME, "a")
        #TREBA JIH BO OBDELAT
        return povezave
    
    def poisci_slike(self):
        #self.vmesnik.get(povezava)
        slike = self.vmesnik.find_elements(By.TAG_NAME, "img")
        #TREBA JIH BO OBDELAT
        return slike
    
    def odpri_stran(self, povezava): #VRNE HTML
        self.vmesnik.get(povezava)
        return self.vmesnik.page_source

    def robot(self, link, domena):
        #self.vmesnik.get(link + "/robots.txt")
        dolzina_domene = len(domena)
        for i in range(len(link)):
            if link[i:(i+dolzina_domene)] == domena:
                j = i + dolzina_domene
        robot_link = link[:j] + "/robots.txt"
        self.vmesnik.get(robot_link)
        html_robot = self.vmesnik.page_source
        if "Not Found" in html_robot:
            return "", ""
        #iz html robot je treba vn pobrat še sitemap
        sitemap = html_robot.split("Sitemap:")[1].split("\n")[0].strip()
        return html_robot, sitemap # UPAM DA JE PRAVI FORMAT

    def poisci_nedovoljene(self):
        #TREBA JE ODPRET link/robots.txt in pogledat vrstice ki se začenjo z "Disallow:" in te linke je treba ignorirat i guess
        return # NEKI SM NAREDO V BAZA.PY nevem a je to potrebno
import threading
import psycopg2
from selenium.webdriver.common.by import By
import pathlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    
    def poisci_linke(self, url):
        self.vmesnik.get(url)
        povezave = self.vmesnik.find_elements(By.XPATH, "//a[@href]")
        #TREBA JIH BO OBDELAT
        return povezave
    
    def poisci_slike(self):
        #self.vmesnik.get(povezava)
        slike = self.vmesnik.find_elements(By.TAG_NAME, "img")
        #TREBA JIH BO OBDELAT
        return slike
    
    def pojdi_na_stran(self, povezava):
        return self.vmesnik.get(povezava) 
    
    def odpri_stran(self, povezava): #VRNE HTML
        self.vmesnik.get(povezava)
        return self.vmesnik.page_source
    
    def vrni_vsebino(self, url): #VRNE HTML
        self.vmesnik.get(url)
        try:
            pocakaj = WebDriverWait(self.vmesnik, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            return self.vmesnik.find_element(By.TAG_NAME, "body").text
        except TimeoutException:
            "Predolgo čakanje na stran"
        

    def robot(self, link, domena):
        #self.vmesnik.get(link + "/robots.txt")
        self.vmesnik.get(link)
        dolzina_domene = len(domena)
        for i in range(len(link)):#komentar??!!??
            if link[i:(i+dolzina_domene)] == domena:
                j = i + dolzina_domene
        robot_link = link+'/robots.txt'
        print(robot_link)
        # link[:j] + "/robots.txt"
        self.vmesnik.get(robot_link)
        html_robot = self.vmesnik.page_source
        
        #izberi tistega kjer je sitemap

        if "Not Found" in html_robot:
            return "", ""
        #iz html robot je treba vn pobrat še sitemap
        try:
            sitemap = html_robot.split("Sitemap:")[1].split("\n")[0].strip()
        except :
            sitemap = 'ninaslo'
        print("Sitemap:" + sitemap)
        return html_robot, sitemap # UPAM DA JE PRAVI FORMAT

    def poisci_nedovoljene(self):
        #TREBA JE ODPRET link/robots.txt in pogledat vrstice ki se začenjo z "Disallow:" in te linke je treba ignorirat i guess
        return # NEKI SM NAREDO V BAZA.PY nevem a je to potrebno
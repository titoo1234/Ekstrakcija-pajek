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
        povezave = self.vmesnik.find_elements(By.TAG_NAME, "a")
        return povezave
    
    def poisci_linke(self):
        pocakaj = WebDriverWait(self.vmesnik, 3).until(EC.presence_of_element_located((By.XPATH, "//a|//button")))
        povezave = self.vmesnik.find_elements(By.XPATH, "//a|//button")
        linki = []
        for link in povezave:
            if link.tag_name == "a":
                linki.append(link.get_attribute("href"))
            elif link.tag_name == "button":
                dodaj_link = link.get_attribute("onclick")
                if dodaj_link:
                    linki.append(dodaj_link)
        return linki
    
    def nastavi_stran(self,url):
        self.vmesnik.get(url)

    def preveri_sliko(self,slika):
        '''
            preveri ali je forma slike OK(slike v string formatu ne shranimo...)
        '''
        dovoljene_koncnice = ['.ico', '.cur','.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp','.png','.svg','.apng','.gif']
        for koncina in dovoljene_koncnice:
            if koncina in slika:
                return True
        return False
    
    def poisci_slike(self):
        try:
            pocakaj = WebDriverWait(self.vmesnik, 3).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
            slike = self.vmesnik.find_elements(By.TAG_NAME, "img")
        except Exception as ex:
            slike = []
        slike = [slika.get_attribute("src") for slika in slike]
        slike = [slika for slika in slike if self.preveri_sliko(slika)]

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
            vsebina = self.vmesnik.find_element(By.TAG_NAME, "body").text
            return vsebina.replace("\'", "\"")
        except TimeoutException:
            print(f"Predolgo čakanje na stran: {url}")
            return ""
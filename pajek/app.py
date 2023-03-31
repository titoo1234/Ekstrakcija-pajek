import threading
import psycopg2
from selenium.webdriver.common.by import By
import pathlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from frontier import Frontier
#import funkcije
from vmesnik import Vmesnik
from baza import Baza
from vec_nitni_pajek import VecNitniPajek

SEMENSKE_STRANI = ["http://gov.si/",
                   "http://evem.gov.si/",
                   "http://e-uprava.gov.si/",
                   "http://e-prostor.gov.si/"]
ST_PAJKOV = 1
DOMENA = "gov.si"


if __name__ == '__main__':
    pajek = VecNitniPajek(SEMENSKE_STRANI, ST_PAJKOV, DOMENA, False)
    pajek.zazeni_pajka()
    pajek.info()

# pot = pathlib.Path().absolute()
# WEB_DRIVER_LOCATION = str(pot) + "\..\chromedriver.exe"
# frontier = Frontier()
# vmesnik = Vmesnik()
# baza = Baza()


# ZA IZBRIS PODATKOV IZ BAZE IN DODAJANJE SEED-OV    
# ======================================================================
#baza.zbrisi_vse_iz_baze(frontier,vmesnik)
# ======================================================================
# lastnosti = Options()
# lastnosti.add_argument("--headless")
# # ZANKA
# vmesnik = webdriver.Chrome(WEB_DRIVER_LOCATION, options=lastnosti)

#while True:

# id, link = frontier.vrni_naslednjega()
#VMESNIK. najdi  povezavoi
#preden odprem stran, sparsam domeno
# id_domena, domena = baza.poglej_domeno(link)
# if id_domena == 0: #take domene še nimamo
#     html_robot, sitemap = vmesnik.robot(link, domena)
#     baza.dodaj_domeno(domena, html_robot, sitemap)


# html = vmesnik.odpri_stran(link) #VRNE HTML
# linki = vmesnik.poisci_povezave()
# slike = vmesnik.poisci_slike()
# PODATKI O STRANI HEAD...

#SIMETRIČNO ZA SLIKE

#IN DATOTEKE

#NAFILI VSE V BAZO

#PAZI VRSTNI RED
# LAHKO MAMO SAMO ENO METODO V BAZA (KI SPREJME VELIKO ARGUMENTOV) IN POTEM V PRAVEM VRSTEM REDU KLICE SVOJE METODE (FILA BAZOs)
#baza.dodaj_vse_v_bazo(link, html, slike) #id nerabis ker tisto je id od frontierja
# frontier.dodaj_vec_linkov(linki, id_domena)
# frontier.obdelan_link(id)




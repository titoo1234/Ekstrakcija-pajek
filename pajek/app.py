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

# pot = pathlib.Path().absolute()
# WEB_DRIVER_LOCATION = str(pot) + "\..\chromedriver.exe"
frontier = Frontier()
vmesnik = Vmesnik()
# lastnosti = Options()
# lastnosti.add_argument("--headless")
# # ZANKA
# vmesnik = webdriver.Chrome(WEB_DRIVER_LOCATION, options=lastnosti)


#while True:

id, link = frontier.vrni_naslednjega()
#VMESNIK. najdi  povezavoi

vmesnik.odpri_stran(link)
linki = vmesnik.poisci_povezave()
#slike = vmesnik.poisci_slike()
# PODATKI O STRANI HEAD...

#SIMETRIČNO ZA SLIKE

#IN DATOTEKE

#NAFILI VSE V BAZO


frontier.dodaj_vec_linkov(linki)
frontier.obdelan_link(id)




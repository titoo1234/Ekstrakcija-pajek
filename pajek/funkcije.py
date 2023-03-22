import threading
import psycopg2
from selenium.webdriver.common.by import By
import pathlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

pot = pathlib.Path().absolute()
WEB_DRIVER_LOCATION = str(pot) + "\..\chromedriver.exe"

lastnosti = Options()
lastnosti.add_argument("--headless")

vmesnik = webdriver.Chrome(WEB_DRIVER_LOCATION, options=lastnosti)

def poisci_povezave(vmesnik, povezava):
    vmesnik.get(povezava)
    
    # povezave = vmesnik.find_elements("xpath", "//*[@href]")
    tekst = vmesnik.find_element(By.XPATH, "/html/body")
    print(tekst.text)
    # for pov in povezave:
    #     print(pov.get_attribute("href"))

def dodaj_v_frontier(conn, link):
    cur = conn.cursor()
    cur.execute(f"Insert into crawldb.frontier (link, status) values ('{link}', 0)")
    cur.close()
    #value = cur.fetchall()
    return None

SEEDs = ["http://gov.si/",
             "http://evem.gov.si/",
             "http://e-uprava.gov.si/",
             "http://e-prostor.gov.si/"]

poisci_povezave(vmesnik, SEEDs[0])
# conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
# conn.autocommit = True
# for seed in SEEDs:
#     dodaj_v_frontier(conn, seed)

# cur = conn.cursor()
# cur.execute("select * from crawldb.frontier")
# values = cur.fetchall()
# print(values)
# cur.close()
# conn.close()

def dovoljena_domena(link):
    """
    Funkcija vrne True, če imamo opravka z domen *.gov.si
    """
    if link[-7:] == ".gov.si": 
        return True 
    return False 
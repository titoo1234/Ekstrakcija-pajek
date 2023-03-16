import threading
import psycopg2
from selenium.webdriver.common.by import By
import pathlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urlparse, urljoin
from frontier import Frontier

class Baza():
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
        self.conn.autocommit = True

    def dodaj_vse_v_bazo(self, slike):
        #self.dodaj_stran()
        self.dodaj_slike(slike)

    #def dodaj_stran(self,): #site_id nevem
        #time.time() za accessed time?

    #def dodaj_povezave(self, id1, id2):

    def poglej_domeno(self, link):
        domena = urlparse(link).netloc
        cur = self.conn.cursor()
        cur.execute(f"SELECT id FROM crawldb.site WHERE domain = '{domena}'")
        id_domene = cur.fetchone()
        if id_domene is None: #take domene še nimamo zato jo bomo dodali v vmesniku
            id = 0
        else: #tako domeno že imamo zato vrnemo id domene
            id = id_domene[0]
        cur.close()
        return id, domena
    
    def dodaj_domeno(self, domena, html_robot, sitemap):
        cur = self.conn.cursor()
        print('dodajam domeno')
        cur.execute(f"INSERT INTO crawldb.site (domain, robots_content, sitemap_content) VALUES ('{domena}', '{html_robot}', '{sitemap}')")
        cur.close()
        return


    def dodaj_slike(self, slike):
        cur = self.conn.cursor()
        for slika in slike:
            s = slika.get_attribute("src")
            #cur.execute(f"Insert into crawldb.image (link, status) values ('{link}', 0)")
            #TREBA DODAT OB PRAVEM ČASU KER SO V BAZI TUJI KLJUČI
        cur.close()
        return
    
    def zbrisi_vse_iz_baze(self,frontier,vmesnik):
        cur = self.conn.cursor()
        cur.execute(f"delete from crawldb.page")
        cur.execute(f"delete from crawldb.site")
        cur.execute(f"delete from crawldb.image")
        cur.execute(f"delete from crawldb.frontier")
        SEEDs = [
            "http://gov.si/",
                    "http://evem.gov.si/",
                    "http://e-uprava.gov.si/",
                    "http://e-prostor.gov.si/"
                    ]
        
        for link in SEEDs:
            print("prvi link:" + link)
            vmesnik.vmesnik.get(link)
            redirect_link = vmesnik.vmesnik.current_url
            print("redirect:" + link)
            id_domena, domena = self.poglej_domeno(redirect_link)
            if id_domena == 0: #take domene še nimamo
                html_robot, sitemap = vmesnik.robot(redirect_link, domena)
                self.dodaj_domeno(domena, html_robot, sitemap)
                id_domena, domena = self.poglej_domeno(redirect_link)#POPRAVI TO JE ZAČASNO DA SE SPREMNI ID_DOMENE
            frontier.dodaj_v_frontier(link, id_domena)

        # cur.execute(f'''INSERT INTO crawldb.frontier (link, status) VALUES 
        #                 ('http://gov.si/', 0),
        #                 ('http://evem.gov.si/', 0),
        #                 ('http://e-uprava.gov.si/', 0),
        #                 ('http://e-prostor.gov.si/', 0);''')

        cur.close()
        return
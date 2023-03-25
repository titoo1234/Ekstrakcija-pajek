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
from robots import Robot,RobotsFile
import os
from datetime import datetime, timezone
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



    def dodaj_slike(self, slike,link_id):
        cur = self.conn.cursor()
        for slika in slike:
            koncnica = slika.split('.')[-1]
            filename = os.path.basename(slika)
            # ZAENKRAT NE DODAJAMO DATA!!!
            cur.execute(f"Insert into crawldb.image (page_id,filename,content_type,accessed_time) values ('{link_id}',{filename},{koncnica},{time.time()})")
        cur.close()
        return
    
    def id_strani(self,url):
        cur = self.conn.cursor()
        cur.execute(f"SELECT id FROM crawldb.page WHERE url = '{url}'")
        rez = cur.fetchone()
        cur.close()
        return rez
    
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
    
    def preveri_in_dodaj_domeno(self,link2,vmesnik):
        if self.poglej_domeno(link2)[0] == 0: #Domena še ne obstaja
            robotsfile = RobotsFile(link2,self,vmesnik)
            self.dodaj_domeno(robotsfile.domena, robotsfile.vsebina, robotsfile.sitemap,robotsfile.robot.crawl_delay)
            
    def dodaj_link_frontier(self,link1,link2,nepreskoci = True):
        '''
            doda link v bazo z lastnostjo FRONTIER, doda se tudi v tabelo link1 -> link2 
        '''
        # NE BO TREBA PREVERJAT KER SMO ŽE PREJ ZAGOTOVILI DA JE DOMENA V BAZI!!!
        # preverimo ali je že domena od linka2 v bazi:
        # robotsfile = RobotsFile(link2,self.baza,self.vmesnik)
        # robot = robotsfile.robot
        # if self.baza.poglej_domeno(link2)[0] == 0: #Domena še ne obstaja
        #     self.baza.dodaj_domeno(robot.domena, robot.vsebina, robot.sitemap)
        if nepreskoci:
            id = self.baza.poglej_domeno(link2)[0]
            cur = self.conn.cursor()
            if self.tuja_domena(link2):
                cur.execute(f"INSERT INTO crawldb.page (site_id, page_type_code, url) VALUES ({id}, 'ZUNANJA', {link2})")
            else:
                cur.execute(f"INSERT INTO crawldb.page (site_id, page_type_code, url) VALUES ({id}, 'FRONTIER', {link2})")

        cur.execute(f"SELECT id FROM crawldb.page WHERE url = {link1}")
        id_link1 = cur.fetchone()
        cur.execute(f"SELECT id FROM crawldb.page WHERE url = {link2}")
        id_link2 = cur.fetchone()
        # dodamo še link1 -> link2 
        cur.execute(f"INSERT INTO crawldb.link (from_page, to_page) VALUES ({id_link1}, {id_link2})")
        cur.close()
        return
    
    def tuja_domena(self,link):
        domena = urlparse(link).netloc
        if "gov.si" in domena:
            return False
        return True
        
    def pridobi_robots_datoteko(self, link):
        cur = self.conn.cursor()
        domena = urlparse(link).netloc
        cur.execute(f"SELECT robots-content FROM crawldb.site WHERE domain = {domena}")
        robots = cur.fetchone()
        cur.close()
        return robots


        
    def dodaj_domeno(self, domena, robot_txt, sitemap,crawl_delay):
        cur = self.conn.cursor()
        trenutni_cas = datetime.now()
        print('dodajam domeno')
        cur.execute(f"INSERT INTO crawldb.site (domain, robots_content, sitemap_content,crawl_delay,zadnji_dostop) VALUES ('{domena}', '{robot_txt}', '{sitemap}',{crawl_delay},'{trenutni_cas}')")
        cur.close()
        return
    
    def spremenini_obstojeci_page(self,url,vsebina,http_status_koda):
        cur = self.conn.cursor()
        if self.je_duplikat(vsebina):
            cur.execute(f"UPDATE crawldb.page SET (page_type_code,http_status_code,accessed_time) = ('DUPLICATE',{http_status_koda},{time.time()}) WHERE url = {url}")
        else:
            cur.execute(f"UPDATE crawldb.page SET (page_type_code,html_content,http_status_code,accessed_time) = ('HTML','{vsebina}',{http_status_koda},{time.time()}) WHERE url = {url}")

    def je_duplikat(self,vsebina):
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) from crawldb.page WHERE html_content = {vsebina}")
        stevilo_istih_strani = cur.fetchone()
        cur.close()
        if stevilo_istih_strani > 0:
            return True
        return False
            
        




    
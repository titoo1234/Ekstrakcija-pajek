import threading
import psycopg2
from selenium.webdriver.common.by import By
import pathlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urlparse, urljoin

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
        a = cur.fetchone()
        if a is None: #take domene še nimamo zato jo bomo dodali v vmesniku
            id = 0
        else: #tako domeno že imamo zato vrnemo id domene
            id = a[0]
        cur.close()
        return id, domena
    
    def dodaj_domeno(self, domena, html_robot, sitemap):
        cur = self.conn.cursor()
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
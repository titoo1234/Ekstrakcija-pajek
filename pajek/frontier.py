import threading
import psycopg2
from selenium.webdriver.common.by import By
import pathlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


class Frontier():
    def __init__(self) -> None:
        self.conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
        self.conn.autocommit = True
        self.lock = threading.Lock()

    def dodaj_v_frontier(self, link, id_domena, cur=None):
        if link == "":
            return
        if cur is None:
            cur = self.conn.cursor()
            #prvo dodamo v .page stran - možnost napake zaradi ponavljanja
            # try:
            cur.execute(f"INSERT INTO crawldb.page (site_id, page_type_code, url) VALUES ({id_domena}, 'FRONTIER', '{link}')")
            cur.execute(f"Insert into crawldb.frontier (link, status) values ('{link}', 0)")
            # except: #upam da je samo napaka za duplikat
            #     pass
        else:
            #prvo dodamo v .page stran - možnost napake zaradi ponavljanja
            try:
                cur.execute(f"INSERT INTO crawldb.page (site_id, page_type_code, url) VALUES ({id_domena}, 'FRONTIER', '{link}')")
                cur.execute(f"Insert into crawldb.frontier (link, status) values ('{link}', 0)")
            except Exception as e: #upam da je samo napaka za duplikat
                print(e)

        cur.close()
        return
    
    def dodaj_vec_linkov(self, linki, id_domena):
        cur = self.conn.cursor()
        for link in linki:
            self.dodaj_v_frontier(link.get_attribute("href"), id_domena, cur)
        cur.close()
        return
    
    def vrni_naslednjega(self):
        with self.lock:
            cur = self.conn.cursor()
            cur.execute(f"select id, link from crawldb.frontier where status = 0 ORDER BY id LIMIT 1")
            id, rez = cur.fetchone()
            cur.execute(f"UPDATE crawldb.frontier SET status = 1 WHERE id = {id};")
            #cur.execute(f"INSERT INTO crawldb.page")
            cur.close()
            return id, rez
    
    def obdelan_link(self, id):
        cur = self.conn.cursor()
        cur.execute(f"UPDATE crawldb.frontier SET status = 2 WHERE id = {id};")
        cur.close()
        return
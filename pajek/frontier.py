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

    def dodaj_v_frontier(self, link, cur=None):
        if cur is None:
            cur = self.conn.cursor()
            cur.execute(f"Insert into crawldb.frontier (link, status) values ('{link}', 0)")
            cur.close()
        else:
            cur.execute(f"Insert into crawldb.frontier (link, status) values ('{link}', 0)")
        return
    
    def dodaj_vec_linkov(self, linki):
        cur = self.conn.cursor()
        for link in linki:
            self.dodaj_v_frontier(link.get_attribute("href"), cur)
        cur.close()
        return
    
    def vrni_naslednjega(self):
        with self.lock:
            cur = self.conn.cursor()
            cur.execute(f"select id, link from crawldb.frontier where status = 0 ORDER BY id LIMIT 1")
            id, rez = cur.fetchone()
            cur.execute(f"UPDATE crawldb.frontier SET status = 1 WHERE id = {id};")
            cur.close()
            return id, rez
    
    def obdelan_link(self, id):
        cur = self.conn.cursor()
        cur.execute(f"UPDATE crawldb.frontier SET status = 2 WHERE id = {id};")
        cur.close()
        return
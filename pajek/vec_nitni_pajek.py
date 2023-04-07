import multiprocessing
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import requests
from baza import Baza
from vmesnik import Vmesnik
from robots import Robot,RobotsFile
import time
from page import *

class VecNitniPajek:

    def __init__(self, semenske_strani, st_pajkov, domena, zacetek=True):
        self.semenske_strani = semenske_strani
        self.st_pajkov = st_pajkov
        self.domena = domena
        self.pool = ThreadPoolExecutor(max_workers=self.st_pajkov)
        self.preverjeni_linki = set()
        self.nedovoljene_strani = set() # tukaj se hranijo strani ki zaradi robots.txt niso dovoljene
        self.frontier = Queue()
        self.vmesnik = Vmesnik()
        self.baza = Baza()
        # Napolnimo frontier s semenskimi stranmi 
        if zacetek:
            self.obdelaj_semenske_strani()
        else:
            self.napolni_frontier_iz_baze()
            self.napolni_preverjene_linke_iz_baze()
    
    def obdelaj_semenske_strani(self):
        for url in self.semenske_strani:
            try:
                self.vmesnik.pojdi_na_stran(url)
                page = Page(url, self.vmesnik, self.baza)
                page.dodaj_v_bazo()
                self.obdelaj_linke(page)
                page.http_status_code = page.pridobi_http_status_code()
                page.html_content = page.pridobi_html_content()
                page.posodobi_v_bazi()

            except Exception as e:
                print(f"Napaka: obdelaj_semenske_strani: {e}")
                continue

    def napolni_preverjene_linke_iz_baze(self):
        """
        Funkcija doda med obiskane strani vse url-je iz baze, ki nimajo oznake FRONTIER
        """
        linki = self.baza.pridobi_obiskane_strani()
        for link in linki:
            self.preverjeni_linki.add(link[0])

    def napolni_frontier_iz_baze(self):
        """
        Funkcija v frontier doda vse url-je, ki imajo oznako FRONTIER iz baze
        """
        linki = self.baza.pridobi_frontier()
        for link in linki:
            self.frontier.put(link[0])

    def zazeni_pajka(self):
        """
        Ta metoda dodaja nove linke, ki jih najde v html-ju, v frontier
        """
        while True:
            try:
                naslednji_url = self.frontier.get(timeout=60)
                pajek = self.pool.submit(self.obdelaj_stran, naslednji_url)
                pajek.add_done_callback(self.konec_obdelave_strani)
            except Empty:
                # v frontierju ni več linkov na razpolago
                return
            except Exception as e:
                print(f"Napaka: zazeni_pajka: {e}")
                continue

    def  obdelaj_stran(self, url):
        """
        Metoda odpre podano stran
        """
        try:
            stran = Page(url, self.vmesnik, self.baza)
            return stran
        except requests.RequestException as e:
            print(f"Napaka: obdelaj_stran: {e}")
            return 
        
    def nedovoljena_stran(self,link,tab_ned_strani):
        for dis in tab_ned_strani:
            ujemanje = dis.replace('*','')
            if ujemanje[1:] in link:
                return True
        return False 


    def obdelaj_linke(self, stran):
        """
        Metoda podane linke doda v bazo
        """
        dodani = set()
        linki = stran.pridobi_linke()
        for page in linki:
            try:
                if page.nepravilen_url():# če link nima ustrezne končnice ga izpustimo
                    continue
                #PRIDOBI NEDOVOLJENE STRANI
                domena = urlparse(page.url).netloc
                site = self.baza.pridobi_site(domena)
                try:
                    robot = Robot(site[2]) # site[2] je ravno robots datoteka
                    nedovoljene_strani = robot.disallow
                except:
                    nedovoljene_strani = []

                if page.url in self.preverjeni_linki and page.url not in dodani:
                    dodani.add(page.url)
                    self.baza.dodaj_link_frontier(stran.url,page.url,False)#false -> doda samo v tabelo linkov 
                    continue
                elif not self.nedovoljena_stran(page.url, nedovoljene_strani) and page.url not in dodani:
                    dodani.add(page.url)
                    if not page.je_zunanji():
                        self.frontier.put(page.url)
                    page.dodaj_v_bazo()
                    self.preverjeni_linki.add(page.url)  
            except Exception as e:
                # ce pride do napake nadaljujemo na naslednji link
                print(f"Napaka: obdelaj_link: {e}")  
                continue
    
    def konec_obdelave_strani(self, stran):
        try:
            page = stran.result()
            self.vmesnik.pojdi_na_stran(page.url) # vmesniku nastavimo trenutno stran (da ni ponovljenih klicev)
            #TUKAJ ŠE NI HTML_CONTENT
            #pridobi podatke 
            page.http_status_code = page.pridobi_http_status_code()
            #http_status_code = page.http_status_code
            page.html_content = page.pridobi_html_content()
            
            je_duplikat = page.preveri_duplikat()
            if not je_duplikat:
                self.obdelaj_linke(page)
            page.posodobi_v_bazi()
            return
            
        except Exception as e:
            # ce pride do napake, koncamo s pregledom strani in gremo na novo stran
            print(f"Napaka: konec_obdelave_strani: {e}")
            return

    def info(self):
        print('\n Pridobljeni linki: ', self.preverjeni_linki, '\n')


    



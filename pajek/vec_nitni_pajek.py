import multiprocessing
from bs4 import BeautifulSoup
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
                                        # TODO: dodaj strani ki so ze v bazi
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
            except Exception as e:
                print(f"\n NAPAKA (obdelaj_semenske_strani) --> {url}. Izpis napake: {e}")
                continue

    def napolni_preverjene_linke_iz_baze(self):
        """
        Funkcija doda med obiskane strani vse url-je iz baze, ki nimajo oznake FRONTIER
        """
        linki = self.baza.pridobi_obiskane_strani()
        for link in linki:
            self.preverjeni_linki.add(link)

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
                print("\nTrenutni proces: ", multiprocessing.current_process().name, '\n')
                print("\nPridobivanje URL-ja iz frontier-ja...")
                naslednji_url = self.frontier.get(timeout=60)
                print(f"\nURL: {naslednji_url} je bil pridobljen iz frontier-ja.")
                print(f"\nPreverjanje in dodajanje domene ...")
                self.baza.preveri_in_dodaj_domeno(naslednji_url,self.vmesnik)
                print("\nDomena je bila preverjenja oz. dodana.")
                print(f"\nOdpiranje strani: {naslednji_url}\n")
                pajek = self.pool.submit(self.obdelaj_stran, naslednji_url)

                print(f"\nPreglejevanje strani in ekstrakcija: {naslednji_url}\n")
                pajek.add_done_callback(self.konec_obdelave_strani)
                print(f"\nKonec preglejevanja strani: {naslednji_url}\n")
            except Empty:
                # v frontierju ni več linkov na razpolago
                return
            except Exception as e:
                print(e)
                continue

    def  obdelaj_stran(self, url):
        """
        Metoda odpre podano stran
        """
        try:
            stran = Page(url, self.vmesnik, self.baza)
            return stran
        except requests.RequestException:
            return 
        
    def zadosca_domeni(self, link):
        """
        Funkcija vrne true, če podana povezava zadošča izbrani domeni
        """
        povezava = urlparse(link).netloc
        if povezava.endswith(self.domena):
            return True
        return False
        
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
        linki = stran.pridobi_linke()
        for page in linki:
            print(page.url)
            #PRIDOBI NEDOVOLJENE STRANI
            domena = urlparse(page.url).netloc
            site = self.baza.pridobi_site(domena) # to bi naredil drugače !!!
            robot = Robot(site[2]) # site[2] je ravno robots datoteka
            nedovoljene_strani = robot.disallow

            if page.url in self.preverjeni_linki:
                self.baza.dodaj_link_frontier(stran.url,page.url,False)#false -> doda samo v tabelo linkov 
                continue

            if not self.nedovoljena_stran(page.url, nedovoljene_strani):
                if not page.je_zunanji():
                    self.frontier.put(page.url)
                page.dodaj_v_bazo()
                self.preverjeni_linki.add(page.url)    
    
    def konec_obdelave_strani(self, stran):
        page = stran.result()
        self.vmesnik.pojdi_na_stran(page.url) # vmesniku nastavimo trenutno stran (da ni ponovljenih klicev)
        je_duplikat = page.preveri_duplikat()
        page.posodobi_v_bazi()
        if not je_duplikat:
            self.obdelaj_linke(page)
        return

    def shrani_slike(self,id_strani):
        slike = self.vmesnik.poisci_slike()
        self.baza.dodaj_slike(slike,id_strani)

    def shrani_v_bazo(self,url,vsebina,http_status_koda):
        '''
            napolni podatke o strani: poišče page in ga spremeni
        '''
        self.baza.spremenini_obstojeci_page(url,vsebina,http_status_koda)
 
    def pridobi_vsebino(self, url):
        """
        Metoda pridobi html vsebino strani in jo doda v bazo
        """
        vsebina = self.vmesnik.vrni_vsebino(url)

        # TODO DAJMO SI SHRANJEVAT ČE PRIDE KJE DO NAPAKE IN SICER V NEKO NOVO TABELO, DA BOMO LAHKO VEDELI
        # SHANIMO SI LINK IN PA BESEDILO NAPAKE
        # TA LINK MORAMO PONOVNO PREGLEDATI!!! 

    def info(self):
        print('\n Pridobljeni linki: ', self.preverjeni_linki, '\n')


    



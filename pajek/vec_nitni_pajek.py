import multiprocessing
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import requests
from baza import Baza
from vmesnik import Vmesnik
from robots import Robots
import time

class VecNitniPajek:

    def __init__(self, semenske_strani, st_pajkov, domena):
        self.semenske_strani = semenske_strani
        self.st_pajkov = st_pajkov
        self.domena = domena
        self.pool = ThreadPoolExecutor(max_workers=self.st_pajkov)
        self.obiskane_strani = set([])
        self.nedovoljene_strani = set([]) # tukaj se hranijo strani ki zaradi robots.txt niso dovoljene
        self.frontier = Queue()
        self.vmesnik = Vmesnik()
        self.baza = Baza()
        self.robots = Robots()
        # Napolnimo frontier s semenskimi stranmi
        for semenska_stran in semenske_strani: self.frontier.put(semenska_stran)

    def zazeni_pajka(self):
        """
        Ta metoda dodaja nove linke, ki jih najde v html-ju, v frontier
        """
        i = 1
        while i < 5:
            try:
                print("\nTrenutni proces: ", multiprocessing.current_process().name, '\n')
                naslednji_url = self.frontier.get(timeout=60)

                if naslednji_url not in self.obiskane_strani:
                    print(f"\nPreglejevanje strani: {naslednji_url}\n")
                    self.obiskane_strani.add(naslednji_url)
                    i +=1
                    pajek = self.pool.submit(self.obdelaj_stran, naslednji_url)
                    pajek.add_done_callback(self.konec_obdelave_strani)
            except Empty:
                # v frontierju ni več linkov na razpolago
                return
            except Exception as e:
                print(e)
                continue

    def obdelaj_stran(self, url):
        """
        Metoda odpre podano stran in iz nje pobere vsebino
        """
        try:
            stran = requests.get(url, timeout=(3, 30))
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
        
    def pridobi_linke(self, url):
        """
        Metoda pridobi vse linke na trenutni strani
        """
        linki = self.vmesnik.poisci_linke(url)
        for link in linki:
            print(link)
            link = link.get_property("href")
            print(link)
            # Pogledamo ali najden url ustreza zahtevam domene ter robots.txt datoteke 
            # TODO - POTREBNO JE PREGLEDATI ROBOTS DATOTEKO IN USTREZNO REAGIRATI!!!
            #        ČE NI ROBOTS.TXT DATOTEKE PA ČASOVNO OMEJITI ŠTEVILO DOSTOPOV 
            if self.zadosca_domeni(link) and self.robots.zadosca_robots_datoteki(link):
                # Pogledamo ali je najden url že slučanjo med pregledanimi stranmi ali med nedovoljenimi stranmi
                if link not in self.obiskane_strani and link not in self.nedovoljene_strani:
                    self.frontier.put(link)

    def konec_obdelave_strani(self, stran):
        rezultat_strani = stran.result()
        # TODO - ČE STATUS_CODE != 200 JE POTREBNO VSEENO ZABELEŽITI V BAZO
        if rezultat_strani and rezultat_strani.status_code == 200:
            # najprej pridobimo nedovoljene strani iz robots.txt
            self.nedovoljene_strani.union(self.robots.vrni_nedovoljene_strani(rezultat_strani.url))
            self.pridobi_linke(rezultat_strani.url)
            self.pridobi_vsebino(rezultat_strani.url)
            # TODO - POTREBNO JE TUDI PREVERITI LINKE SLIK IN JIH USTREZNO DODATI V BAZO

    def pridobi_vsebino(self, url):
        """
        Metoda pridobi html vsebino strani in jo doda v bazo
        """
        vsebina = self.vmesnik.vrni_vsebino(url)
        # TODO - TU BI DODALI VSE PODATKE O STRANI V BAZO IN USTREZNO SPREMENILI PAGE_TYPE
        #      - TU BI LAHKO PREVERILI TUDI DUPLIKATE
        #self.baza.dodaj_vsebino(vsebina)
        print(vsebina)
        print("\nDodano v bazo\n")

    def info(self):
        print('\n Obdelane strani: ', self.obiskane_strani, '\n')



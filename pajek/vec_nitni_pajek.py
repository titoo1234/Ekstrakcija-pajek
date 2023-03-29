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

    def __init__(self, semenske_strani, st_pajkov, domena):
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
        # self.robots = Robot('')
        # Napolnimo frontier s semenskimi stranmi
        for semenska_stran in semenske_strani: self.frontier.put(semenska_stran)

    def zazeni_pajka(self):
        """
        Ta metoda dodaja nove linke, ki jih najde v html-ju, v frontier
        """
        i = 1
        while i < 8:
            try:
                i +=1
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
        # TODO POGLEDAMO V ROBOTSE DOMENE, KI SO ŽE ZAPISANI V BAZI
        # čas = robot.čas
        # pogledamo dovoljeni čas
        # POGLEDAMO, KDAJ JE BILA NAZADNJE DODANA STRAN IZ TE DOMENE
        # ČE JE ČAS OK, POTEM GA SPUSTI NAPREJ DA OBDELA STRAN SICER POČAKAJ...
        # KO ČAS PRETEČE PONOVNO PREVERI ALI JE DOVOLJENO NA STRAN(ČAS ZANDNJE DODANE STRANI IZ DOMENE)
        
        try:
            stran = Page(url, self.vmesnik, self.baza)
            # stran = requests.get(url, timeout=(3, 30))
            #TRENUTNI ČAS ZABELEŽI V BAZO PRI DOMENI
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
            link = link.get_property("href") 
            print(link)
            #POGLEJMO DOMENO ČE JE NI JO DODAJ
            self.baza.preveri_in_dodaj_domeno(link,self.vmesnik)
            #PRIDOBI NEDOVOLJENE STRANI
            domena = urlparse(url).netloc
            site = self.baza.pridobi_site(domena) # to bi naredil drugače !!!
            robot = Robot(site[2]) # site[2] je ravno robots datoteka
            nedovoljene_strani = robot.disallow
            # KAJ JE TU MIŠLJENO?
            if link in self.preverjeni_linki:
                self.baza.dodaj_link_frontier(url,link,False)#TRUE -> doda samo v tabelo linkov 

            if link not in self.preverjeni_linki and not self.nedovoljena_stran(link,nedovoljene_strani):
                if not self.baza.tuja_domena(link):
                    self.frontier.put(link)
                self.baza.dodaj_link_frontier(url,link)#doda v bazo, tudi tujo stran
                self.preverjeni_linki.add(link)

    def nedovoljena_stran(self,link,tab_ned_strani):
        for dis in tab_ned_strani:
            ujemanje = dis.replace('*','')
            if ujemanje[1:] in link:
                return True
        return False 
    
    def konec_obdelave_strani(self, stran):
        page = stran.result()
        self.vmesnik.pojdi_na_stran(page.url)
        # TODO - ČE STATUS_CODE != 200 JE POTREBNO VSEENO ZABELEŽITI V BAZO
        # najprej pridobimo nedovoljene strani iz robots.txt
        # TO NASLEDNJO VRSTICO MISLIM DA NE RABIMO....
        # self.nedovoljene_strani.union(self.robots.vrni_nedovoljene_strani(page.url)) 

        print(f"\n Pridobivanje vsebine iz strani: {page.url}...\n")
        page.html_content = page.pridobi_html()
        je_duplikat = page.preveri_duplikat()
        print(f"\n Konec pridobivanja vsebine iz strani: {page.url}\n")
        print(f"\n Shranjevanje vsebine iz strani: {page.url} v bazo...\n")
        page.dodaj_ali_posodobi()
        # self.shrani_v_bazo(page.url,vsebina,page.status_code)
        print(f"\n Konec shranjevanja vsebine iz strani: {page.url} v bazo...\n")
        id_strani = self.baza.id_strani(page.url)

        print(f"\n Preglejevanje duplikatov...\n")
        if not je_duplikat:
            print(f"\n Stran: {page.url} ni duplikat!!\n")
            print(f"\n Pridobivanje linkov iz strani: {page.url}...\n")
            self.pridobi_linke(page.url)
            print(f"\n Konec pridobivanja linkov iz strani: {page.url}...\n")
            print(f"\n Shranjevanje slik iz strani: {page.url}...\n")
            self.shrani_slike(id_strani)
            print(f"\n Konec shranjevanja slik iz strani: {page.url}...\n")
            # self.shrani_datoteke(vsebina)
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
        # TODO - TU BI DODALI VSE PODATKE O STRANI V BAZO IN USTREZNO SPREMENILI PAGE_TYPE
        #      - TU BI LAHKO PREVERILI TUDI DUPLIKATE
        #self.baza.dodaj_vsebino(vsebina)


        # TODO DAJMO SI SHRANJEVAT ČE PRIDE KJE DO NAPAKE IN SICER V NEKO NOVO TABELO, DA BOMO LAHKO VEDELI
        # SHANIMO SI LINK IN PA BESEDILO NAPAKE
        # TA LINK MORAMO PONOVNO PREGLEDATI!!! 

    def info(self):
        print('\n Pridobljeni linki: ', self.preverjeni_linki, '\n')


    



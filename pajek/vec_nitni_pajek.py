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
        self.robots = Robot()
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
                # ne smem narediti robotsfile, najprej pogledamo če obstaja
                # robotsfile = RobotsFile(naslednji_url,self.baza,self.vmesnik)
                # robot = robotsfile.robot
                self.baza.preveri_in_dodaj_domeno(naslednji_url)
                # if self.baza.poglej_domeno(naslednji_url)[0] == 0: #Domena še ne obstaja
                #     robotsfile = RobotsFile(naslednji_url,self.baza,self.vmesnik)
                #     robot = robotsfile.robot
                #     self.baza.dodaj_domeno(robot.domena, robot.vsebina, robot.sitemap,robot.crawl_delay)

                #Domena obstaja:

                crawl_delay = 5 #crawl_delay_domene(naslednji_url) 
                #spustimo naprej ko bomo lahko...

                # MISLIM DA NAM TUKAJ NI POTREBNO PREVERJATI STRANI KER BOMO V FRONTIER DODAJALI SAMO STRANI KI SO DOVOLJENE
                # if not robot.preveri_link_iz_baze(naslednji_url):
                #     #ali moramo preveriti stran?
                #     continue

                # TUDI MISLIM DA NI TREBA PREVERITI ALI JE LINK ŽE PREGLEDAN?
                if (naslednji_url not in self.obiskane_strani):
                    

                    
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
            stran = requests.get(url, timeout=(3, 30))
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
            #POGLEJMO DOMENO ČE JE NI JO DODAJ
            
            self.baza.preveri_in_dodaj_domeno(link)

            #PRIDOBI NEDOVOLJENE STRANI
            nedovoljene_strani = []# TODO potrebno narediti funkcijo ki iz baze vzame robots.txt in vrne nedovoljene strani za dano domeno

            if link in  self.obiskane_strani:
                self.baza.dodaj_link_frontier(url,link,True)#TRUE -> doda samo v tabelo linkov 
            #TO NE VEM ZAKA JE?
            # if self.robots.zadosca_robots_datoteki(link):
                # Pogledamo ali je najden url že slučanjo med pregledanimi stranmi ali med nedovoljenimi stranmi
            if link not in self.obiskane_strani and not self.nedovoljena_stran(link,nedovoljene_strani):#link not in self.nedovoljene_strani:
                if not self.baza.tuja_domena(link):
                    self.frontier.put(link)
                self.baza.dodaj_link_frontier(url,link)#doda v bazo, tudi tujo stran

    def nedovoljena_stran(self,link,tab_ned_strani):
        for dis in tab_ned_strani:
            ujemanje = dis.replace('*','')
            if ujemanje[1:] in link:
                return True
        return False 
    def konec_obdelave_strani(self, stran):
        rezultat_strani = stran.result()
        # TODO - ČE STATUS_CODE != 200 JE POTREBNO VSEENO ZABELEŽITI V BAZO
        if rezultat_strani and rezultat_strani.status_code == 200:
            # najprej pridobimo nedovoljene strani iz robots.txt
            # TO NASLEDNJO VRSTICO MISLIM DA NE RABIMO....
            # self.nedovoljene_strani.union(self.robots.vrni_nedovoljene_strani(rezultat_strani.url)) 
            vsebina = self.pridobi_vsebino(rezultat_strani.url)
            self.shrani_v_bazo(rezultat_strani.url,vsebina,rezultat_strani.status_code)
            id_strani = self.baza.id_strani(rezultat_strani.url)
            if not self.baza.je_duplikat(vsebina):
                self.pridobi_linke(rezultat_strani.url)
                self.shrani_slike(id_strani)
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
        print('\n Obdelane strani: ', self.obiskane_strani, '\n')


    



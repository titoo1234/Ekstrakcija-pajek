import time
import requests
from urllib.parse import urljoin, urlparse
from datetime import datetime, timezone
import os
from robots import *

HTML = "HTML"
BINARY = "BINARY"
DUPLICATE = "DUPLICATE"
ZUNANJI = "ZUNANJI"
FRONTIER = "FRONTIER"

FORMATI_SLIK = ['.ico', '.cur','.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp','.png','.svg','.apng','.gif']

class Page:
    def __init__(self, url, vmesnik, baza):
        self.url = url
        self.vmesnik = vmesnik
        self.baza = baza
        self._site_id = self.pridobi_site_id()
        self._page_type_code = None
        self._html_content = None
        self._accessed_time = None
        self._http_status_code = None
        self._filename = None
        self._content_type = None
        self._data_type_code = None
        self._page_id = None
        self._data = None
        self.preveri_url()

    @property
    def http_status_code(self):
        return self._http_status_code
    
    @http_status_code.setter
    def http_status_code(self, vrednost):
        self._http_status_code = vrednost 
    
    @property
    def accessed_time(self):
        return self._accessed_time
    
    @accessed_time.setter
    def accessed_time(self, vrednost):
        self._accessed_time = vrednost 

    @property
    def dobljena_stran(self):
        return self.pridobi_stran()
    
    @dobljena_stran.setter
    def dobljena_stran(self, vrednost):
        self._dobljena_stran = vrednost
    
    @property
    def site_id(self):
        return self._site_id
    
    @site_id.setter
    def site_id(self, vrednost):
        self._site_id = vrednost 
    
    @property
    def html_content(self):
        return self._html_content
    
    @html_content.setter
    def html_content(self, vrednost):
        self._html_content = vrednost 

    @property
    def page_type_code(self):
        return self._page_type_code
    
    @page_type_code.setter
    def page_type_code(self, vrednost):
        self._page_type_code = vrednost

    @property
    def page_id(self):
        return self._page_id
    
    @page_id.setter
    def page_id(self, vrednost):
        self._page_id = vrednost 

    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, vrednost):
        self._filename = vrednost 

    @property
    def content_type(self):
        return self._content_type
    
    @content_type.setter
    def content_type(self, vrednost):
        self._content_type = vrednost

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, vrednost):
        self._data = vrednost

    @property
    def data_type_code(self):
        return self._data_type_code
    
    @data_type_code.setter
    def data_type_code(self, vrednost):
        self._data_type_code = vrednost

    def pridobi_http_status_code(self):
        try:
            self.preveri_dostop_in_cakaj() # preverimo robots in po potrebi cakamo
            response = requests.get(self.url, timeout=(3, 30))
            return response.status_code
        except Exception as e:
            print(f"Napaka: http_status_code: {e}")
            return None
        
    def pridobi_accessed_time(self):
        if not self._accessed_time: # ce ga se nismo nastavili, ga nastavimo sedaj
            return datetime.now()
    
    def pridobi_site_id(self):
        "Funkcija pridobi pripadajoči site_id domene"
        domena = urlparse(self.url).netloc
        self.baza.preveri_in_dodaj_domeno(self.url,self.vmesnik)
        return self.baza.pridobi_site(domena)[0] # vzamemo id

    def pridobi_html_content(self):
        "Funckija obisce stran ter vrne html vsebino."
        try:
            if self.http_status_code < 400:
                self.preveri_dostop_in_cakaj()
                vsebina = self.vmesnik.vrni_vsebino(self.url)
                self.page_type_code = HTML
                self.accessed_time = self.pridobi_accessed_time()
                return vsebina
            return ""
        except Exception as e:
            print(f"Napaka: pridobi_html: {e}")
            return None

    
    def preveri_duplikat(self):
        "Funkcija v primeru, da je stran duplikat ustrezno zamenja page_type_code strani"
        try:
            if self.baza.je_duplikat(self.html_content):
                self.page_type_code = DUPLICATE
                return True
            return False
        except Exception as e:
            print(f"Napaka: preveri_duplikat: {e}")
            return False
    
    def preveri_url(self):
        """Funkcija pogleda url strani, in če je:
            - pdf
            - doc
            - docx
            - ppt
            - pptx
        ustrezno reagira (spremeni page_type_code)"""
        formati_dat = self.baza.pridobi_data_type()
        # preverimo ali je datoteka
        for format in formati_dat:
            format = format[0]
            if self.url.endswith(format.lower()):
                self.page_type_code = BINARY
                self.data = None
                self.data_type_code = format.upper()
                return
        # preverimo ali je slika
        for format in FORMATI_SLIK:
            if self.url.endswith(format):
                self.page_type_code = BINARY
                self.filename = os.path.basename(self.url)
                self.content_type = self.vrni_koncnico(self.url)
                self.data = None
                self.html_content = None
                self.http_status_code = None
                return 

        #preverimo ali ima tujo domeno 
        if self.baza.tuja_domena(self.url):
            self.page_type_code = ZUNANJI
            return 

        # drugače je frontier  
        self.page_type_code = FRONTIER

    def nepravilen_url(self):
        """
        metoda preveri url in če nima ustrezne končnice vrne true
        """
        koncnica = self.vrni_koncnico(self.url)
        if koncnica != "": 
            # url ima koncnico - ni navaden url
            formati_dat = self.baza.pridobi_data_type()
            map(lambda x: x[0].lower(), formati_dat) # to naredimo, ker imamo opravka s tupli npr. ('PDF',)
            dovoljene_koncnice = FORMATI_SLIK + formati_dat + [".html"]
            if koncnica not in dovoljene_koncnice:
                return True
            return False
        else:
            return True


    def pridobi_linke(self):
        """
        Metoda pridobi linke is spletne strani
        """
        strani = self.vmesnik.poisci_linke()
        slike = self.vmesnik.poisci_slike()
        linki = strani + slike
        return [Page(link, self.vmesnik, self.baza) for link in linki]
    
    def je_binary(self):
        return self.page_type_code == BINARY
    
    def je_frontier(self):
        return self.page_type_code == FRONTIER
    
    def je_duplicat(self):
        return self.page_type_code == DUPLICATE
    
    def je_html(self):
        return self.page_type_code == HTML
    
    def je_zunanji(self):
        return self.page_type_code == ZUNANJI

    @staticmethod
    def vrni_koncnico(url):
        tuple = os.path.splitext(url)
        return tuple[1]

    def dodaj_ali_posodobi(self):
        page = self.baza.pridobi_page(self.url)
        if page:
            self.posodobi_v_bazi()
        else:
            self.dodaj_v_bazo()

    def posodobi_v_bazi(self):
        self.http_status_code = self.pridobi_http_status_code()
        self.html_content = self.pridobi_html_content()
        id = self.baza.posodobi_page(self.site_id, 
                                        self.page_type_code,
                                        self.url,
                                        self.html_content,
                                        self.http_status_code,
                                        self.accessed_time)
            
    def dodaj_v_bazo(self):
        self.page_id = self.baza.dodaj_page_v_bazo(self.site_id, 
                                                    self.page_type_code,
                                                    self.url,
                                                    self.html_content,
                                                    self.http_status_code,
                                                    self.accessed_time)
        
        if self.je_binary():
            # lahko je slika ali dokument
            if not self.filename:
                self.baza.dodaj_page_data_v_bazo(self.page_id,
                                                 self.data_type_code,
                                                 self.data)
            else:
                self.baza.dodaj_image_v_bazo(self.page_id,
                                             self.filename,
                                             self.content_type,
                                             self.data,
                                             self.accessed_time)
            
    def pridobi_data(self):
        # TODO - pridobi binary podatke 
        return ""
    
    def preveri_dostop_in_cakaj(self):
        domena = urlparse(self.url).netloc
        format = "%Y-%m-%d %H:%M:%S.%f"
        cas = 0
        while cas < 60: # cakamo najvec eno minuto!!
            try:
                id, domena, robot_content, sitemap_content, crawl_delay, zadnji_dostop_str  = self.baza.pridobi_site(domena)
            except Exception as e:
                print(f"Napaka: preveri_dostop_in_cakaj: {e}")
                return 
            zadnji_dostop = datetime.strptime(str(zadnji_dostop_str), format)
            pretecen_cas = abs(zadnji_dostop - datetime.now())
            print(f"preveri_dostop_in_cakaj: Pretecen cas je: {pretecen_cas}")
            if pretecen_cas.seconds < crawl_delay:
                print(f"\n Čakamo, da bo dovoljeno dostopati do strani: {self.url}")
                time.sleep(crawl_delay - pretecen_cas.seconds) # pocakaj da bo dovoljeno
                cas += crawl_delay - pretecen_cas.seconds
            # if pretecen_cas.seconds < 1:
            #     print(f"\n Čakamo, da bo dovoljeno dostopati do strani: {self.url}")
            #     time.sleep(1) # pocakaj da bo dovoljeno
            #     cas += 1
            else:
                self.baza.spremeni_cas_domene(id) # nastavimo nov čas zadnjega dostopa
                return 

    def pridobi_stran(self):
        try:
            self.preveri_dostop_in_cakaj() # preverimo robots in po potrebi cakamo
            response = requests.get(self.url, timeout=(3, 30))
            return response
        except Exception as e:
            print(f"Napaka: pridobi_stran: {e}")
            return None

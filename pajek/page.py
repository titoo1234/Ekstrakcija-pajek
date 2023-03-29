import time
import requests
from urllib.parse import urljoin, urlparse
from datetime import datetime, timezone

class Page:
    def __init__(self, url, vmesnik, baza):
        self.url = url
        self.vmesnik = vmesnik
        self.baza = baza
        self.site_id = self.pridobi_site_id()
        self.accessed_time = datetime.now()
        self.dobljena_stran = self.pridobi_stran(self.url)
        self.page_type_code = "FRONTIER" #stran smo dobili iz frontierja, zato je ob icinializaciji to zagotovo frontier
        self.html_content = None # ob inicializaciji nastavimo html_content na prazen niz

    @property
    def http_status_code(self):
        if self.dobljena_stran:
            # stran obstaja
            return self.dobljena_stran.status_code
        print(f"\nStran: {self.url} ni bila pridobljena\n")
        return 400 # vračamo kar 400
    
    def pridobi_site_id(self):
        "Funkcija pridobi pripadajoči site_id domene"
        domena = urlparse(self.url).netloc
        return self.baza.pridobi_site(domena) # vzamemo id

    def pridobi_html(self):
        "Funckija obisce stran ter vrne html vsebino."
        if self.http_status_code < 400:
            self.page_type_code = "HTML"
            return self.vmesnik.vrni_vsebino(self.url)
        return ""
    
    def preveri_duplikat(self):
        "Funkcija v primeru, da je stran duplikat ustrezno zamenja page_type_code strani"
        if self.baza.je_duplikat(self.html_content):
            self.page_type_code = "DUPLICATE"
            return True
        return False

    def dodaj_v_bazo(self):
        self.baza.dodaj_page_v_bazo(self.site_id, 
                                     self.page_type_code,
                                     self.url,
                                     self.html_content,
                                     self.http_status_code,
                                     self.accessed_time)

    @staticmethod
    def pridobi_stran(url):
        try:
            return requests.get(url, timeout=(3, 30))
        except Exception as e:
            print(e)
            return None


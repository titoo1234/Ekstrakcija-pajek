import re
import requests
from urllib.parse import urljoin, urlparse

class RobotsFile:
    def __init__(self, url, baza, vmesnik):
        self._url = url 
        self.baza = baza
        self.vmesnik = vmesnik

    @property
    def vsebina(self):
        try:
            obdelan_niz = requests.get(self.url, timeout=(3, 30))
            if obdelan_niz.status_code > 299:
                return ''
            obdelan_niz = obdelan_niz.text
            if "html" in obdelan_niz: # bili smo redirectani oz robots.txt ne obstaja
                return ''
            obdelan_niz = re.sub('#.*','',obdelan_niz)
            obdelan_niz = re.sub('\n\n','\n',obdelan_niz)
            obdelan_niz = re.sub('User-agent','\nUser-agent',obdelan_niz)
            obdelan_niz = re.sub('Sitemap:','\nSitemap:',obdelan_niz)
            return obdelan_niz[1:]
        except Exception as e:
            print(e)
            return ''
        
    @property
    def url(self):
        return "http://" + urlparse(self._url).netloc + "/robots.txt"

    @property
    def domena(self):
        return urlparse(self.url).netloc        
    
    @property
    def roboti(self):
        if not self.vsebina:
            return [Robot('')]
        tab_robots_dat = self.razdeli_robots_datoteko(self.vsebina)
        # za vsak user-agent naredimo svojega robota
        return [Robot(niz) for niz in tab_robots_dat]
    
    @property
    def robot(self):
        """
        Zanima nas samo robots datoteka, kjer je user-agent = '*'
        """
        for robot in self.roboti:
            if robot.user_agent == '*':
                return robot
        
    @property
    def sitemap(self):  
        for vrstica in self.vsebina.split('\n'):
            if vrstica.startswith('Sitemap'):
                # pogledamo od 'Sitemap:' naprej in stripamo ter naredimo objekt Sitemap
                return vrstica[8:].strip()
        return ''
    
    @staticmethod
    def razdeli_robots_datoteko(niz):
        """
        Metoda razdeli podano robots datoteko (niz) na posamezne user-agente
        Vrne tabelo nizov, ki se začnejo z posmeznim 'User-agent'-om
        """
        return niz.split('\n\n')
    
    def zadosca_robots_datoteki(self, link):
        return True
    
    def vrni_nedovoljene_strani(self, url):
        """
        Metoda na podlagi url-ja poišče url/robots.txt datoteko, če obstaja
        in vrne vse nedovoljene strani.
        """
        nedovoljene_strani = set([])
        return nedovoljene_strani

class Robot:
    def __init__(self, robots_dat):
        self.robots_dat = robots_dat

    @property
    def disallow(self):
        return self.beri_robots_datoteko(self.robots_dat, "Disallow")
    
    @property
    def user_agent(self):
        user_agent_tab = self.beri_robots_datoteko(self.robots_dat, "User-agent")
        if user_agent_tab == []:
            return '*'
        return user_agent_tab[0]
    
    @property
    def allow(self):
        return self.beri_robots_datoteko(self.robots_dat, "Allow")
    
    @property
    def noindex(self):
        return self.beri_robots_datoteko(self.robots_dat, "Noindex")
    
    @property
    def crawl_delay(self):
        crawl_delay_tab = self.beri_robots_datoteko(self.robots_dat, "Crawl-delay")
        if crawl_delay_tab == []:
            return 5
        return float(crawl_delay_tab[0])

    @staticmethod
    def beri_robots_datoteko(niz, atribut):
        """
        Metoda v podanem nizu poišče url-je pred katerimi nasopa podan atribut:
        npr.: - Disallow: /admin 
                Disallow: /resources --> ['/admin', '/resources']
              - Sitemap: https://www.gov.si/sitemap.xml --> ['https://www.gov.si/sitemap.xml']
              - User-agent: * --> ['*']
        """
        tab_nizov = []
        vrstice = niz.split('\n')
        for vrstica in vrstice:
            if vrstica.startswith(atribut):
                dolzina_atributa = len(atribut)
                # gledamo kaj je desno od atributa (upostevamo se ':')
                niz = vrstica[dolzina_atributa+1:]
                # 'ocistimo' kar je desno in levo od nasega niza ki nas zanima in dodamo med tab_nizov
                tab_nizov.append(niz.strip())
        return tab_nizov
    
    def preveri_link(self, link):
        for dis in self.disallow:
            ujemanje = dis.replace('*','')
            if ujemanje[1:] in link:
                return False
        return True 

class Sitemap:
    def __init__(self, url):
        self.url = url

    @property
    def vsebina(self):
        stran = None
        try:
            stran = requests.get(self.url,
                                    timeout=(5, 10))
            stran.raise_for_status()
    
        except requests.exceptions.RequestException:
            print(f"\nPriplo je do napaka pri dostopu do strani: {self.url}\n")
            # ce pride do napake vrnemo prazen niz
            return ''
        
        return stran.text
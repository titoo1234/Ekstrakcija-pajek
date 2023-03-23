import re

class RobotsFile:
    def __init__(self, url, baza, vmesnik):
        self.url = url
        self.baza = baza
        self.vmesnik = vmesnik

    @property
    def vsebina(self):
        try:
            self._vsebina = self.vmesnik.vrni_vsebino(self.url)
        except Exception as e:
            print(e)
        return self._vsebina
    
    @property
    def url(self):
        return self._url
        
    
    @url.setter
    def url(self, vrednost):
        # osnovnemu url-ju dodamo končnico /robots.txt
        self._url = vrednost + "/robots.txt" 

    @property
    def roboti(self):
        tab_robots_dat = self.razdeli_robots_datoteko(self.vsebina)
        # za vsak user-agent naredimo svojega robota
        return [Robot(niz) for niz in tab_robots_dat]
    
    @property
    def robot(self):
        """
        Zanima nas samo robots datoteka, kjer je user-agent = '*'
        """
        pravi_robot = None
        for robot in self.roboti:
            if robot.user_agent == '*':
                pravi_robot = robot
        return pravi_robot
    
    @property
    def sitemap(self):
        razdeljena_dat = self.razdeli_robots_datoteko(self.vsebina)
        zadnja_vrstica = razdeljena_dat[-1]
        if zadnja_vrstica.startswith('Sitemap'):
            # pogledamo od Sitemap: naprej in stripamo
            return zadnja_vrstica[8:].strip()
        return None
    
    @staticmethod
    def razdeli_robots_datoteko(niz):
        """
        Metoda razdeli podano robots datoteko (niz) na posamezne user-agente
        Vrne tabelo nizov, ki se začnejo z posmeznim 'User-agent'-om
        """
        return niz.split('\n\n')
    
    def zadosca_robots_datoteki(self, link):
        # TODO dodaj omejitve!!!
        return True
    
    def vrni_nedovoljene_strani(self, url):
        """
        Metoda na podlagi url-ja poišče url/robots.txt datoteko, če obstaja
        in vrne vse nedovoljene strani.
        """
        nedovoljene_strani = set([])
        # TODO - poišči url/robots.txt in dodaj strani ki so pod "disallowed"
        return nedovoljene_strani

    # TODO - ustvari metode za ostale omejitve glede robots.txt datotek
    # - disallow
    # - allow
    # - user-agent
    # - crawl-delay
    # - sitmap

class Robot:
    def __init__(self, robots_dat):
        self.robots_dat = robots_dat

    @property
    def disallow(self):
        return self.beri_robots_datoteko(self.vsebina, "Disallow")
    
    @property
    def user_agent(self):
        return self.beri_robots_datoteko(self.vsebina, "User-agent")
    
    @property
    def allow(self):
        return self.beri_robots_datoteko(self.vsebina, "Allow")
    
    @property
    def crawl_delay(self):
        return self.beri_robots_datoteko(self.vsebina, "Crawl-delay")

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
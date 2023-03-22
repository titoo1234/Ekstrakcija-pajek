class Robots:
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
    # - user-agent
    # - 
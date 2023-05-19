from baza import Baza
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import re
class Beseda():
    def __init__(self,beseda,dokument):
        self.beseda = beseda
        self.dokument = dokument
        self.frekvenca = 0
        self.indeks = ""
        self.baza = Baza()

    def dodaj_v_bazo(self):
        if not self.baza.preveri_besedo(self):
            self.baza.dodaj_besedo_v_index_word(self)
        self.baza.dodaj_besedo_v_bazo(self)

    def nastavi_indeks(self):
        # pattern = re.compile(re.escape(self.beseda))  
        # TODO tukaj bomo morali iskati iz prejšnje tabele tokensov-tam ko so vezaji itd zraven!!!
        # matches = pattern.finditer(self.dokument.tekst)
        # occurrences = [match.span() for match in matches]
        # tab = list(re.finditer(self.dokument.tekst,self.beseda))
        indexes = []
        for index, item in enumerate(self.dokument.tokens_celoten):
            if item == self.beseda:
                indexes.append(index)
        indexes = [str(i) for i in indexes]
        self.frekvenca = len(indexes)
        self.indeks = ','.join(indexes)

    

        
    

    
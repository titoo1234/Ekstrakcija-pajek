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
        # tukaj bomo morali iskati iz prejšnje tabele tokensov-tam ko so vezaji itd zraven!!! JE NAREJENO
        # TO TABELO FILAMO TUDI V BAZO, KER BOMO TAKO LAŽJE POTEM PREBRALI SNIPETE....

        # TEGA NE BOMO RABLI VERJETN:

        # pattern = re.compile(r"\b\S*" + re.escape(self.beseda) + r"\b\S*") 
        # matches = pattern.finditer(self.dokument.tekst)
        # occurrences = [match.span() for match in matches]
        # self.frekvenca = len(occurrences)
        # self.indeks = ','.join([str(par[0]) for par in occurrences])
        # return

        indexes = []
        for index, item in enumerate(self.dokument.tokens_celoten):
            if item == self.beseda:
                indexes.append(index)
        indexes = [str(i) for i in indexes]
        self.frekvenca = len(indexes)
        self.indeks = ','.join(indexes)

    

        
    

    
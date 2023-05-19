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

    def dodaj_v_bazo(self):
        if not Baza.preveri_besedo(self):
            Baza.dodaj_besedo_v_index_word(self)
        Baza.dodaj_besedo_v_bazo(self)

    def nastavi_indeks(self):
        tab = list(re.finditer(self.dokument.tekst,self.beseda))
        return tab
    
    def nastavi_frekvenco(self):
        return len(self.indeks)
    

        
    

    
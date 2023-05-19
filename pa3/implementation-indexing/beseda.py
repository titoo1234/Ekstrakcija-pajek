from baza import Baza
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
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
        
    

    
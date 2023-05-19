from baza import Baza
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
class Beseda():
    def __init__(self,beseda,dokument,frekvenca,indeks):
        self.beseda = beseda
        self.dokument = dokument
        self.frekvenca = frekvenca
        self.indeks = indeks


    def dodaj_v_bazo(self):
        if not Baza.preveri_besedo(self):
            Baza.dodaj_besedo_v_index_word(self)
        Baza.dodaj_besedo_v_bazo(self)


    @staticmethod
    def obdelaj_dokument(dokument):
        text = BeautifulSoup(dokument,'html.parser').text() 
        Baza.dodaj_dokument(dokument,text)

    @staticmethod
    def obdelaj_vse_dokumente(dokumenti):
        for dokument in dokumenti:
            Beseda.obdelaj_dokument(dokument)
    
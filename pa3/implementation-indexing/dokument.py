from baza import Baza
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from stopwords import stop_words_slovene
import string
from beseda import Beseda

class Dokument:
    def __init__(self, ime, pot):
        self.ime = ime
        self.pot =  pot
        self.baza = Baza()
        self.tekst = self.vrni_tekst(self.pot)
        self.tokens,self.tokens_celoten = self.vrni_tokense(self.tekst)
        

    @staticmethod
    def odpri_dokument(pot):
        with open(pot, "r", encoding="utf-8") as dat:
            return dat.read()
       
    @staticmethod
    def vrni_tekst(pot):
        dat = Dokument.odpri_dokument(pot)
        return BeautifulSoup(dat, "html.parser").get_text()
    
    @staticmethod
    def vrni_tokense(tekst):
        tokens = word_tokenize(tekst,language='slovene')
        filtered_tokens = [token for token in tokens if token.lower() not in stop_words_slovene]
        filtered_tokens = set([token for token in filtered_tokens if token not in string.punctuation]) # ne potrebujemo duplikatov 
        return list(filtered_tokens),tokens
    
    def obdelaj_dokument(self):
        ''' Funkcija gre čez vse tokense in indeksira besede v originalnem besedilu'''
        self.baza.dodaj_dokument(self.ime, self.tekst, ','.join(self.tokens_celoten))
        for token in self.tokens: 
            beseda = Beseda(token,self)
            beseda.nastavi_indeks()#tukaj se nastavi tudi frekvenca
            beseda.dodaj_v_bazo()


        
    # def obdelaj_vse_dokumente(self):
    #     for dokument in dokumenti:
    #         Beseda.obdelaj_dokument(dokument)
        
    

from baza import Baza
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from stopwords import stop_words_slovene
import string

class Dokument:
    def __init__(self, ime, pot):
        self.ime = ime
        self.pot =  pot
        self.tekst = self.vrni_tekst(self.pot)
        self.tokens = self.vrni_tokense(self.tekst)

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
        filtered_tokens = set([token.lower() for token in filtered_tokens if token not in string.punctuation]) # ne potrebujemo duplikatov 
        return list(filtered_tokens)
    
    def obdelaj_dokument(self):
        ''' Funkcija gre čez vse tokense in indeksira besede v originalnem besedilu'''
        Baza.dodaj_dokument(self.ime, self.tekst)
        
    # def obdelaj_vse_dokumente(self):
    #     for dokument in dokumenti:
    #         Beseda.obdelaj_dokument(dokument)
        
    

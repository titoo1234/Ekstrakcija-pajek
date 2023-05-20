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
        rez = BeautifulSoup(dat, "html.parser").find('body')
        rez = rez.get_text()
        return ' '.join(rez.split())
    
    @staticmethod
    def vrni_tokense(tekst):
        tokens = word_tokenize(tekst,language='slovene')
        tokens_vrni =  [token.lower() for token in tokens if token not in string.punctuation]
        # TODO??? IZBRIŠEMO PIKO NA PRVEM MESTU ČE JE
        filtered_tokens = [token for token in tokens if token.lower() not in stop_words_slovene]
        filtered_tokens = set([token.lower() for token in filtered_tokens if token not in string.punctuation]) # ne potrebujemo duplikatov 
        return list(filtered_tokens),tokens_vrni
    
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

    def pridobi_snippet(self):
        poizvedba = '''SELECT 
                        document,
                        '...' || substr(text, instr(text, ?) - 2, 5) as snippet
                       FROM 
                        document
                       WHERE
                        text LIKE '%' || ? || '%' 
                    '''  # verjetno ne dela xD
        #TODO - vrni poizvedbo
        return [("evem.gov.si/evem.gov.si.666.html", "Sistem SPOT je eden boljši ... dosedanje delovanje SPOT ni zadovoljivo za ... je bila zaključena. Sistem ni deloval dobro ..."),("e-uprava.gov.si/e-uprava.gov.si.42.html", "... ministrstvo je nadgradilo sistem za učinkovitejšo uporabo.")]
        
    

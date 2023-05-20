from time import time
from tabulate import tabulate
from beseda import Beseda
from nltk.tokenize import word_tokenize
from dokument import Dokument
from baza import Baza
import os
import os.path



def naredi_slovar_poti():
    ''' Funkcija vsakemu dokumentu pripiše njegovo ustrezno pot'''
    slovar = {}
    for mapa in os.listdir(POT):
        pot = os.path.join(POT, mapa)
        for dokument in os.listdir(pot): # treba je se počistit __MACOS in druge
            slovar[dokument] = pot
    return slovar

def razbij_poizvedbo_na_besede(niz):
    ''' Metoda razdeli niz na posamezne besede in vrne tabelo besed '''
    besede = word_tokenize(niz, language="slovene")
    besede = [beseda.lower() for beseda in besede]
    return besede

def poisci_podatke(beseda):
    baza = Baza()
    pass
if __name__ == '__main__':
    POT = r"PA3-data/"
    SLOVAR_POTI = naredi_slovar_poti()
    

    vhod = input("Results for a query: ")
    print("\n\n")
    zacetek = time()
    # pridobivanje podatkov iz baze...
    tab_besed = razbij_poizvedbo_na_besede(vhod)
    slovar_dokumenti = dict()
    for beseda in tab_besed:
        rezultat = poisci_podatke(beseda) #rezultat = (beseda,dokument,frekvenca,indeksi,tekst,tokens)

        # slovar_dokumenti[dokument] = 

    # frekvence = Beseda.pridobi_frekvence(tab_besed)
    # rezultati = []
    # for frekvenca, dokument_ime in frekvence:
    #     dokument = Dokument(dokument_ime, )
    # snippeti = Dokument.pridobi_snippet()
    # # ...
    konec = time()
    print(f"\tResults faoud in {konec}ms.")
    print("\n\n")
    table = [["Frequencies", "Document", "Snnippet"]]



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
    rezultat = baza.poisci_podatke(beseda)
    return rezultat
def izpisi_snipet(indeksi,tokens,tekst):
    snipet  = ''
    for index in indeksi: 
        # snipet += '...' + tekst[index-30:index+30] + '...\n'
        snipet +=  '...'+ ' '.join(tokens[index-2:index+2])+ '...\n'
    print(snipet)


if __name__ == '__main__':
    os.chdir(r'pa3/implementation-indexing')
    # POT = r"PA3-data/"
    # SLOVAR_POTI = naredi_slovar_poti()
    

    vhod = 'sistem'#input("Results for a query: ")
    print("\n\n")
    zacetek = time()
    # pridobivanje podatkov iz baze...
    tab_besed = razbij_poizvedbo_na_besede(vhod)
    slovar_dokumenti = dict()
    for beseda in tab_besed:
        for vrstica in poisci_podatke(beseda):
            beseda,dokument,frekvenca,indeksi,tekst,tokens_celoten = vrstica #rezultat = (beseda,dokument,frekvenca,indeksi,tekst,tokens)
            if dokument in slovar_dokumenti: 
                slovar_dokumenti[dokument][2].extend([int(i) for i in indeksi.split(',')]) 
            else:
                slovar_dokumenti[dokument] = (tekst,tokens_celoten,[int(i) for i in indeksi.split(',') if indeksi != ''])
    # print(slovar_dokumenti)
    sorted_dict = dict(sorted(slovar_dokumenti.items(), key=lambda item: len(item[1][2]),reverse=True))
    i = 0
    for dokument,(tekst,tokens,indeksi) in sorted_dict.items():
        print(dokument)
        print(len(indeksi))
        izpisi_snipet(indeksi,tokens.split(','),tekst)
        i+=1
        if i > 3:
            break
        

         
         
    

    # frekvence = Beseda.pridobi_frekvence(tab_besed)
    # rezultati = []
    # for frekvenca, dokument_ime in frekvence:
    #     dokument = Dokument(dokument_ime, )
    # snippeti = Dokument.pridobi_snippet()
    # # ...
    konec = time()
    
    print(f"\tResults faoud in {konec-zacetek}ms.")
    # print("\n\n")
    # table = [["Frequencies", "Document", "Snnippet"]]



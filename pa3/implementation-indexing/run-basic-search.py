import os 
from time import time
from nltk.tokenize import word_tokenize
from tabulate import tabulate
from beseda import Beseda
from dokument import Dokument


def naredi_tabelo_poti():
    ''' Funkcija vsakemu dokumentu pripiše njegovo ustrezno pot'''
    tab = []
    for mapa in os.listdir("PA3-data"):
        if mapa.endswith(".si"):
            pot = os.path.join("PA3-data", mapa)
            for dokument in os.listdir(pot): # treba je se počistit __MACOS in druge
                if dokument.endswith(".html"):
                    tab.append(os.path.join(pot, dokument))
    return tab

def razbij_poizvedbo_na_besede(niz):
    ''' Metoda razdeli niz na posamezne besede in vrne tabelo besed '''
    besede = word_tokenize(niz, language="slovene")
    besede = [beseda.lower() for beseda in besede]
    return besede

def poisci_indekse(tokensi, beseda):
        indexes = []
        for index, item in enumerate(tokensi):
            if item == beseda:
                indexes.append(index)
        return indexes

def uredi_indekse(tab):
    '''
       naredi pare zacetek,konec
       zdruzi indekse, ce so le ti dovolj skupaj
    '''
    pari = []
    prejsni = -5
    zac = -5
    kon = -5
    zacetek = True
    n = len(tab)
    i = 0
    for indeks in tab:
        i +=1
        if zacetek:
            zac = indeks
            kon = indeks
            zacetek = False
            prejsni = indeks
            if i == n:
                pari.append((zac,kon))
        else:
            if indeks - prejsni < 3:#sta dovolj skupaj
                prejsni = indeks
                kon = indeks
                if i == n:
                    pari.append((zac,kon))
            else:
                pari.append((zac,kon))
                zac = indeks
                kon = indeks
                prejsni = indeks
                if i == n:
                    pari.append((zac,kon))
                # pari.append(zacetek,konec)
    return pari
        
def vrni_snipet(indeksi,tokens,tekst):
    snipet  = ''
    indeksi.sort()
    indeksi = uredi_indekse(indeksi) 
    for levi,desni in indeksi: 
        # snipet += '...' + tekst[index-30:index+30] + '...\n'
        snipet +=  '...'+ ' '.join(tokens[levi-2:desni+3])+ '...\n'
    return snipet

def poisci_podatke(beseda, dokumenti):
    ''' Metoda poišče vse podatke o besedi v vseh dokumentih '''
    slovar = {} # polnili bomo slovar dokumentov oblike {'ime_dokumenta': [frekvenca, snippet]}
    for dokument in dokumenti:
        # najprej pogledamo ali je beseda sploh v dokumentu
        ime_dokumenta = os.path.basename(dokument)
        tekst = Dokument.vrni_tekst(dokument)
        tokensi = Dokument.vrni_tokense(tekst)[0]
        print(tokensi)
        if beseda in tokensi:
            print("tukaj sem")
            # če je, pa poiščemo frekvenco in pa snippet
            frekvenca = tokensi.count(beseda)
            indeksi = poisci_indekse(tokensi, beseda)
            snippet = vrni_snipet(indeksi, tokensi, tekst)
            slovar[ime_dokumenta] = [frekvenca, snippet]
    print(slovar)
    return slovar 

if __name__ == '__main__':
    dokumenti = naredi_tabelo_poti()
    slovar = poisci_podatke("sistem", dokumenti)

    # tab = [1]
    # vhod = input("Results for a query: ")
    # print("\n\n")
    # zacetek = time()
    # # pridobivanje podatkov 
    # tab_besed = razbij_poizvedbo_na_besede(vhod)
    # slovar_dokumenti = dict()
    # for beseda in tab_besed:
    #     for vrstica in poisci_podatke(beseda, dokumenti):
    #         beseda,dokument,frekvenca,indeksi,tekst,tokens_celoten = vrstica #rezultat = (beseda,dokument,frekvenca,indeksi,tekst,tokens)
    #         if dokument in slovar_dokumenti: 
    #             slovar_dokumenti[dokument][2].extend([int(i) for i in indeksi.split(',')]) 
    #         else:
    #             slovar_dokumenti[dokument] = (tekst,tokens_celoten,[int(i) for i in indeksi.split(',') if indeksi != ''])
    # # print(slovar_dokumenti)
    # sorted_dict = dict(sorted(slovar_dokumenti.items(), key=lambda item: len(item[1][2]),reverse=True))
    # i = 0
    # for dokument,(tekst,tokens,indeksi) in sorted_dict.items():
    #     print(dokument)
    #     print(len(indeksi))
    #     izpisi_snipet(indeksi,tokens.split(','),tekst)
    #     i+=1
    #     if i > 3:
    #         break
    # # frekvence = Beseda.pridobi_frekvence(tab_besed)
    # # rezultati = []
    # # for frekvenca, dokument_ime in frekvence:
    # #     dokument = Dokument(dokument_ime, )
    # # snippeti = Dokument.pridobi_snippet()
    # # # ...
    # konec = time()
    
    # print(f"\tResults faoud in {konec-zacetek}ms.")
    # print("\n\n")
    # table = [["Frequencies", "Document", "Snnippet"]]
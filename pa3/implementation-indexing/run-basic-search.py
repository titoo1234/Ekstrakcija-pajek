import os 
from time import time
from nltk.tokenize import word_tokenize
from tabulate import tabulate
from beseda import Beseda
from dokument import Dokument
from stopwords import stop_words_slovene
from time import sleep
from tqdm import tqdm
import string


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
    snipet  = []
    indeksi.sort()
    indeksi = uredi_indekse(indeksi) 
    for levi,desni in indeksi: 
        # snipet += '...' + tekst[index-30:index+30] + '...\n'
        snipet.append(' '.join(tokens[levi-2:desni+3]))
    return "... " + " ... ".join(snipet) + " ..."

def vrni_tokense(tekst):
        tokens = word_tokenize(tekst,language='slovene')
        # tokens_vrni =  [token.lower() for token in tokens if token not in string.punctuation]
        # TODO??? IZBRIŠEMO PIKO NA PRVEM MESTU ČE JE
        filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words_slovene]
        return filtered_tokens
        # filtered_tokens = set([token.lower() for token in filtered_tokens if token not in string.punctuation]) # ne potrebujemo duplikatov 
        # return list(filtered_tokens),tokens_vrni

def poisci_podatke(besede, dokumenti):
    ''' Metoda poišče vse podatke o besedi v vseh dokumentih '''
    slovar = {} # polnili bomo slovar dokumentov oblike {'ime_dokumenta': [frekvenca, snippet]}
    i = 0
    for i in tqdm(range(len(dokumenti))):
        dokument = dokumenti[i] 
        i +=1
        ime_dokumenta = os.path.basename(dokument)
        tekst = Dokument.vrni_tekst(dokument)
        tokensi = vrni_tokense(tekst)
        frekvenca = 0
        indeksi = []
        snippet = ""
        for beseda in besede:
            # najprej pogledamo ali je beseda sploh v dokumentu
            if beseda in tokensi:
                # če je, pa poiščemo frekvenco in pa indekse
                frekvenca += tokensi.count(beseda)
                indeksi += poisci_indekse(tokensi, beseda)
        indeksi = sorted(indeksi)
        # naredimo snippet
        snippet = vrni_snipet(indeksi, tokensi, tekst)
        if frekvenca > 0:
            slovar[ime_dokumenta] = [frekvenca, snippet]
        sleep(0.01)
    return slovar 

if __name__ == '__main__':
    dokumenti = naredi_tabelo_poti()
    # slovar = poisci_podatke(["sistem", "spot"], ["PA3-data/evem.gov.si/evem.gov.si.66.html"])
    # print(slovar)
    vhod = input("\nResults for a query: ")
    zacetek = time()
    # # pridobivanje podatkov 
    tab_besed = razbij_poizvedbo_na_besede(vhod)
    print("\nPreglejujem dokumente...\n")
    slovar_dokumentov = poisci_podatke(tab_besed, dokumenti)
    tab_dokumentov = sorted(slovar_dokumentov.items(), key=lambda x: x[1][0], reverse=True)
    # lep izpis
    glava = ["Frequencies", "Document", "Snippet"]
    tabela = []
    for izhod in tab_dokumentov: # vzamemo samo prvih pet elementov
        tabela.append([izhod[1][0], izhod[0], izhod[1][1]])
    konec = time() 
    print(f"\nResults found in {round(konec-zacetek,0)}s\n\n")
    # Zapis na datoteko
    with open("testne_dat.txt", "w") as dat:
        print(tabulate(tabela, headers=glava), file=dat)

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
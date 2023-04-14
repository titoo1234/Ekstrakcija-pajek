from parsel import Selector
import re
import json

def odpri_datoteko(datoteka):
    try:
        with open(datoteka, encoding="utf-8") as dat:
            text = dat.read()
    except:
        with open(datoteka, encoding="windows-1252") as dat:
            text = dat.read()
    return text

def rtv_slo(htmls):
    """
    Metoda iz podanih html textov prebere podatke:
     - Title
     - SubTitle
     - Lead
     - Content
     - Author
     - PublishedTime
    ter vrne slovar kjer so zgoraj nasteta poglavja kljuci slovarja
    """
    slovar = {}
    xpaths_slovar = {'Title': '//*[@id="main-container"]/div[3]/div/header/h1/text()',
                     'SubTitle': '//*[@id="main-container"]/div[3]/div/header/div[2]/text()',
                     'Lead': '//*[@id="main-container"]/div[3]/div/header/p/text()',
                     'Content': '//*[@id="main-container"]/div[3]/div/div[2]/article/p/text()',
                     'Author': '//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()',
                     'PublishedTime': '//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]'}
    for html in htmls:
        sel = Selector(html)
        for kljuc, vrednost in xpaths_slovar.items():
            if kljuc == "Content":
                tab_paragrafov = sel.xpath(vrednost).getall()
                slovar[kljuc] = pocisti_content_rtvslo(tab_paragrafov)
            else:
                niz = sel.xpath(vrednost).get()
                if kljuc == "PublishedTime":
                    slovar[kljuc] = pocisti_publishedTime_rtvslo(niz)
                else:
                    slovar[kljuc] = niz
    return slovar

def pocisti_content_rtvslo(tab):
    """ Iz tabele nizov naredi niz ki zdruzi vse elemente te tabele. Nato pocisti znake \n in \t"""
    niz = ' '.join(tab)
    niz = re.sub("\n", " ", niz)
    niz = re.sub("\t", " ", niz)
    return niz

def pocisti_publishedTime_rtvslo(niz):
    """ Iz tabele nizov naredi niz ki zdruzi vse elemente te tabele. Nato pocisti znake \n in \t"""
    niz = re.sub("\n", " ", niz)
    niz = re.sub("\t", " ", niz)
    return niz

def overstock(htmls):
    """ 
    Metoda iz podanih html textov prebere podatke:
     - Title
     - ListPrice
     - Price
     - Saving
     - SavingPercent
     - Content
    ter vrne slovar kjer so zgoraj nasteta poglavja kljuci slovarja
    """
    slovar = {}
    xpaths_slovar = {'Title':  '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a/b/text()',
                     'ListPrice': '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()',
                     'Price': '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()',
                     'Saving': '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()',
                     'SavingPercent': '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()',
                     'Content': '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span/text()'}
    for html in htmls:
        sel = Selector(html)
        for kljuc, vrednost in xpaths_slovar.items():
            tab_vrednosti = sel.xpath(vrednost).getall()
            for item_st in range(len(tab_vrednosti)):
                item = "item " + str(item_st+1) # kljuc po katerem bomo locevali izdelke
                if item in slovar:
                    if kljuc == 'Title':
                        slovar[item][kljuc] = tab_vrednosti[item_st] 
                    elif kljuc == 'ListPrice':
                        slovar[item][kljuc] = tab_vrednosti[item_st] 
                    elif kljuc == 'Price':
                        slovar[item][kljuc] = tab_vrednosti[item_st] 
                    elif kljuc == 'Saving':
                        slovar[item][kljuc] = pocisti_saving_overstock(tab_vrednosti[item_st]) 
                    elif kljuc == 'SavingPercent':
                        slovar[item][kljuc] = pocisti_savingPercent_overstock(tab_vrednosti[item_st])
                    elif kljuc == 'Content':
                        slovar[item][kljuc] = pocisti_content_overstock(tab_vrednosti[item_st])
                else:
                    slovar[item] = {}
                    slovar[item][kljuc] = tab_vrednosti[item_st]
    return slovar

def pocisti_content_overstock(niz):
    """ Funkcija iz content-a pocisti znake \\n in \\t"""
    niz = re.sub("\n", " ", niz)
    niz = re.sub("\t", " ", niz)
    return niz

def pocisti_savingPercent_overstock(niz):
    """ Funkcija iz niza kjer nastopata tako saving kot savinPercent izlusci savingPercent"""
    tab = re.split("\s", niz)
    niz = tab[1]
    niz = re.sub("\(", "", niz)
    niz = re.sub("\)", "", niz)
    return niz

def pocisti_saving_overstock(niz):
    """ Funkcija iz niza kjer nastopata tako saving kot savinPercent izlusci saving"""
    tab = re.split("\s", niz)
    niz = tab[0]
    return niz
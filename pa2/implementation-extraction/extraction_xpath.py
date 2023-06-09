from parsel import Selector
import re
import json
import codecs

def odpri_datoteko(datoteka):
    try:
        with open(datoteka, encoding="utf-8") as dat:
            text = dat.read()
    except Exception as e:
        print(e)
        with open(datoteka, encoding="windows-1252",errors='ignore') as dat:
            print('asd')
            text = dat.read()
    return text

# RTVSLO
# ================================================================

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
    htmls = [htmls]
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

# OVERSTOCK
# ================================================================

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
    htmls = [htmls]
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

# IMDB
# ================================================================

def imdb(htmls):
    """ 
    Metoda iz podanih html textov prebere podatke:
     - Title
     - Year
     - Runtime
     - Genre
     - Rating
     - Content
    ter vrne slovar kjer so zgoraj nasteta poglavja kljuci slovarja
    """
    htmls = [htmls]
    slovar = {}
    xpaths_slovar = {'Title': '//*[@id="main"]/div/div[3]/div/div/div[3]/h3/a/text()',
                     'Year': '//*[@id="main"]/div/div[3]/div/div/div[3]/h3/span[2]/text()',
                     'Runtime': '//*[@id="main"]/div/div[3]/div/div/div[3]/p[1]/span[@class="runtime"]/text()',
                     'Genre': '//*[@id="main"]/div/div[3]/div/div/div[3]/p[1]/span[@class="genre"]/text()',
                     'Rating': '//*[@id="main"]/div/div[3]/div/div/div[3]/div/div[1]/strong/text()',
                     'Content': '//*[@id="main"]/div/div[3]/div/div/div[3]/p[2]'}
    for html in htmls:
        sel = Selector(html)
        for kljuc, vrednost in xpaths_slovar.items():
            tab_vrednosti = sel.xpath(vrednost).getall()
            for item_st in range(len(tab_vrednosti)):
                item = "movie " + str(item_st+1) # kljuc po katerem bomo locevali izdelke
                if item in slovar:
                    if kljuc == 'Title':
                        slovar[item][kljuc] = pocisti_title_imdb(tab_vrednosti[item_st]) 
                    elif kljuc == 'Year':
                        slovar[item][kljuc] = pocisti_year_imdb(tab_vrednosti[item_st]) 
                    elif kljuc == 'Runtime':
                        slovar[item][kljuc] = pocisti_runtime_imdb(tab_vrednosti[item_st]) 
                    elif kljuc == 'Genre':
                        slovar[item][kljuc] = pocisti_genre_imdb(tab_vrednosti[item_st]) 
                    elif kljuc == 'Rating':
                        slovar[item][kljuc] = pocisti_raiting_imdb(tab_vrednosti[item_st])
                    elif kljuc == 'Content':
                        slovar[item][kljuc] = pocisti_content_imdb(tab_vrednosti[item_st])
                else:
                    slovar[item] = {}
                    slovar[item][kljuc] = tab_vrednosti[item_st]
    return slovar

def pocisti_title_imdb(niz):
    """ Funkcija izlusci title"""
    # zaenkrat ne naredimo ničesar
    return niz

def pocisti_year_imdb(niz):
    """ Funkcija odstrani oklepaj in zaklepaj nizu"""
    niz = re.sub("\(", "", niz)
    niz = re.sub("\)", "", niz)
    return niz

def pocisti_runtime_imdb(niz):
    """ Funkcija izlusci runtime"""
    # zaenkrat ne naredimo ničesar
    return niz

def pocisti_genre_imdb(niz):
    """ Funkcija odstrani prehode v novo vrstico ter prazne nize"""
    niz = re.sub("\n", "", niz)
    niz = re.sub("  ", "", niz)
    return niz

def pocisti_raiting_imdb(niz):
    """ Funkcija pocisti raiting"""
    # zaenkrat ne naredimo ničesar
    return niz

def pocisti_content_imdb(niz):
    """ Funkcija iz content-a pocisti znake \\n in \\t"""
    niz = re.sub("\n", "", niz)
    niz = re.sub("\t", " ", niz)
    # odstraniti je potrebmo značke <p ...></p>
    niz = re.sub(r"<p(.*?)>", "", niz)
    niz = re.sub(r"</p>", "", niz)
    # če content slučajno vsebuje tudi kakšne hiperpovezave odstranimo
    # tudi značke tipa <a href="..."></a>
    niz = re.sub(r"<a(.*?)>", "", niz)
    niz = re.sub(r"</a>", "", niz)
    return niz


def zazeni():
    path1_overstock = r'../input-extraction/WebPages/overstock.com/jewelry01.html'
    path2_overstock = r'../input-extraction/WebPages/overstock.com/jewelry02.html'
    path_imdb1 = r'../input-extraction/WebPages/imdb.com/imdb1.html'
    path_imdb2 = r'../input-extraction/WebPages/imdb.com/imdb2.html'
    path_rtvslo1 = r'../input-extraction/WebPages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html'
    path_rtvslo2 = r'../input-extraction/WebPages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljs╠îe v razredu - RTVSLO.si.html'
    
    print("XPATAHS:")
    print("==================================================================")
    print("Overstock.com")
    print("-------------------------------------------")
    pageContent = codecs.open(path1_overstock, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(overstock(pageContent), indent = 4,ensure_ascii=False) 
    print(json_object)
    print("-------------------------------------------")
    pageContent = codecs.open(path2_overstock, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(overstock(pageContent), indent = 4,ensure_ascii=False) 
    print(json_object)
    print("\n\n")

    print("Rtvslo.si")
    print("-------------------------------------------")
    pageContent = codecs.open(path_rtvslo1, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(rtv_slo(pageContent), indent = 4,ensure_ascii=False) 
    print(json_object)
    pageContent = codecs.open(path_rtvslo2, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(rtv_slo(pageContent), indent = 4,ensure_ascii=False) 
    print("-------------------------------------------")
    print(json_object)
    print("\n\n")

    print("Imdb.si")
    print("-------------------------------------------")
    pageContent = codecs.open(path_imdb1, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(imdb(pageContent), indent = 4,ensure_ascii=False) 
    print(json_object)
    pageContent = codecs.open(path_imdb2, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(imdb(pageContent), indent = 4,ensure_ascii=False) 
    print("-------------------------------------------")
    print(json_object)
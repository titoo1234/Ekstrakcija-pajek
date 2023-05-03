from bs4 import BeautifulSoup, Comment
import os
from textdistance import levenshtein
import re

def zazeni_roadrunner(html_1, html_2):
    """
    Funkcija naredi dom strukturo (drevesi) za oba podana html-ja
    in pokliče funkcijo roadrunner.
    Vrne regularni izraz.
    """
    regex = "" # sproti bomo sestavljali regularni izraz
    # Najprej naredimo DOM drevesi za oba podana html-ja
    soup_1 = BeautifulSoup(html_1, "html.parser")
    soup_html_1 = soup_1.find("html")
    soup_2 = BeautifulSoup(html_2, "html.parser")
    soup_html_2 = soup_2.find("html")
    regex = roadrunner(soup_html_1, soup_html_2, regex)
    return regex

def roadrunner(soup_1, soup_2, regex):
    """
    Funkcija preleti oba html-ja ter poisce dele, kjer se razlikujeta.
    To zapise v poseben regularen izraz, ki predstavlja izhod funkcije.
    """
    local_regex = ""
    if ok_tag(soup_1.name) and ok_tag(soup_2.name):
        # pregledamo ujemanje vsebine
        soup_1_text = uredi_text(soup_1)
        soup_2_text = uredi_text(soup_2)
        if not prazno(soup_1) and not prazno(soup_2):
            local_regex += "<" + str(soup_1.name) + ">" # regex-u dodamo ime značke (začetek)
            print(local_regex)
            if levenshtein.distance(soup_1_text,soup_2_text) < 1: # če sta ista samo prepišemo text iz prvega html-ja
                # če imamo števlike 1., 2., 3., ... smatramo to kot različen tekst zaradi imdb-ja
                if re.match(r"[1-9]*\.", soup_1_text.strip()):
                    local_regex += "#text"
                else:
                    local_regex += soup_1_text

            else: # če ne, pa regularnemu izrazu dodamo #text
                local_regex += "#text"
            # rekurzivno ponovimo za otroke v drevesu
            prejsni_child_regex = ""
            ponavljanje = False
            children_1 = list(soup_1.children)
            filter(lambda x: ok_tag(x.name), children_1)
            children_2 = list(soup_2.children)
            filter(lambda x: ok_tag(x.name), children_2)
            while children_1:
                child_1 = children_1[0]
                if ok_tag(child_1.name):
                    while children_2:
                        child_2 = children_2[0]
                        if ok_tag(child_2.name):
                            if se_ujemata(child_1, child_2):
                                # če se izraza ujemata rekurzivno ponovimo postopek na otrocih
                                child_regex = roadrunner(child_1, child_2, regex)
                                # preverimo ali imamo ze tak izraz v nasem regex izrazu
                                if child_regex:
                                    # Če naletimo na enak izraz, ki se do zdaj se ni ponavljal, ga opremimo s "(...) +" 
                                    if levenshtein.distance(prejsni_child_regex, child_regex) < 1 and not ponavljanje:
                                        local_regex = local_regex.replace(child_regex, f"({child_regex}) +")
                                        ponavljanje = True
                                    # če se enak izraz ze dlje casa ponavlja, ne naredimo nicesar
                                    elif levenshtein.distance(prejsni_child_regex, child_regex) < 1 and ponavljanje:
                                        pass
                                    # če pa je izraz drugačen od prejšnega ga dodamo v local_regex
                                    else:
                                        local_regex += child_regex
                                    prejsni_child_regex = child_regex
                                children_2.pop(0)
                                child_2.extract()
                                break
                            else:
                                # pogledati moramo, ali se slučajno ujema s katerim od naslednjih child-ov
                                while children_2:
                                    child = children_2[0]
                                    if ok_tag(child.name):
                                        if se_ujemata(child_1, child):
                                            # našli smo ujemanje 
                                            print(f"se ne ujemata: {child.name}")
                                            child_regex = roadrunner(child_1, child, regex)
                                            # preverimo ali imamo ze tak izraz v nasem regex izrazu
                                            if child_regex:
                                                # Če naletimo na enak izraz, ki se do zdaj se ni ponavljal, ga opremimo s "(...) +" 
                                                if levenshtein.distance(prejsni_child_regex, child_regex) < 1 and not ponavljanje:
                                                    local_regex = local_regex.replace(child_regex, f"({child_regex}) +")
                                                    ponavljanje = True
                                                # če se enak izraz ze dlje casa ponavlja, ne naredimo nicesar
                                                elif levenshtein.distance(prejsni_child_regex, child_regex) < 1 and ponavljanje:
                                                    pass
                                                # če pa je izraz drugačen od prejšnega ga dodamo v local_regex
                                                else:
                                                    local_regex += child_regex
                                                prejsni_child_regex = child_regex
                                            children_2.pop(0)
                                            child_2.extract()
                                            break
                                        else:
                                            # naleteli smo na objekt, ki ga ni v prvem page-u v drugem pa je
                                            local_regex += "(<" + str(child.name) + " ... />)?"
                                    children_2.pop(0)
                                    child_2.extract()
                        try:
                            children_2.pop(0)
                            child_2.extract()
                        except:
                            pass
                children_1.pop(0)
                child_1.extract()
            local_regex += "</" + str(soup_1.name) + ">" # regex-u dodamo ime značke (konec)
    regex += local_regex
    return regex

def vsebuje_isti_tag(tag, tab):
    """
    funkcija vrne true, če se podan tag ujema s katerim v podani tabeli
    """
    for child in tab:
        if se_ujemata(tag, child):
            return True
    return False

def se_ujemata(soup_1, soup_2):
    """
    Funkcija vrne True, če sta podana tag-a podobne strukture in False sicer
    """
    if soup_1.name == soup_2.name:
        #  pogledamo, če imata enaka classa
        if "class" in soup_1.attrs.keys():
            if "class" in soup_2.attrs.keys():
                if levenshtein.distance(str(soup_1.attrs["class"]),str(soup_2.attrs["class"])) < 50:
                    return True
            else: 
                return False
        # pogledamo,  če  imata enaka id-ja
        elif "id" in soup_1.attrs.keys():
            if "id" in soup_2.attrs.keys():
                if levenshtein.distance(str(soup_1.attrs["id"]),str(soup_2.attrs["id"])) < 50:
                    return True
            else:
                return False
        else: # če nimata ne "class" in ne "id" atributa, imeni pa se ujemata, vrnemo true
            return True
    else:
        return False

def ok_tag(tag):
    """
    Funkcija vrne True, če spada podana html značka med značke, ki nas zanimajo
    in False sicer
    """
    not_ok_tags = ["", "None", "none", "\n", "head", "script", "iframe", "footer", "nav", "style", "map", "input"]
    if tag is not None and tag not in not_ok_tags:
        return True
    else:
        return False

def uredi_text(soup):
    """
    Funkcija kot argument dobi tabelo nizov, ki jih zdruzi in po potrebi uredi
    """
    for el in soup(text=lambda text: isinstance(text, Comment)):
        el.extract()
    tab = soup.findAll(string=True, recursive=False)
    tab = list(map(str.strip, tab))
    tab = list(filter(lambda x: x != "\n" and x != "", tab))
    return "".join(tab)

def prazno(soup):
    """
    Funkcija preveri ali je vozlišče v celoti prazno.
    T.j. v celotnem poddrevesu ni nobenega texta
    """
    tab = soup.findAll(string=True, recursive=True)
    tab = list(map(str.strip, tab))
    tab = list(filter(lambda x: x != "\n" and x != "", tab))
    if tab == []:
        return True
    return False

def ustreza_heuristikam(child):
    return True
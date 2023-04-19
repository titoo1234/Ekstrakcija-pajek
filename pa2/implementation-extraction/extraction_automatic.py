from bs4 import BeautifulSoup
import os


def roadrunner(html_1, html_2):
    """
    Funkcija preleti oba html-ja ter poisce dele, kjer se razlikujeta.
    To zapise v poseben regularen izraz, ki predstavlja izhod funkcije.
    """
    regex = "" # sproti bomo sestavljali regularni izraz
    # Najprej naredimo DOM drevesi za oba podana html-ja
    soup_1 = BeautifulSoup(html_1, "html.parser")
    html_tag_1 = soup_1.find("html")
    soup_2 = BeautifulSoup(html_2, "html.parser")
    html_tag_2 = soup_2.find("html")
    # Sprehodimo se čez drevesi, ter iščemo dele, ki se razlikujejo
    for child in html_tag_1.children:
        # Glede na heuristike se odločimo ali je trenutna značka primerna za primerjavo,
        # če ni jo samo prepišemo, če pa je, pa nadaljujemo s primerjanjem
        if ustreza_heuristikam(child):
            # Če sta značka in notranji del isti ga zapišemo v regularni izraz
            
            # Če znački razlikujejo, označimo drugo značko kot opcijski element

            # Če se razlikuje text dodamo "#text" v regularni izraz
            pass
        else:
            regex += child.text()
    return regex

def ustreza_heuristikam(child):
    return True
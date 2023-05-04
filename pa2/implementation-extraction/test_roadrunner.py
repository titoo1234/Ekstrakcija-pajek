from bs4 import BeautifulSoup
import os
from extraction_automatic import *
from textdistance import levenshtein
from textdistance import jaccard

# TESTNI PRIMER:
# ============================================================
html_test_1 = """
<html>
    Books of:
    <b>
        Paul Smith
    </b>
    <ul>
        <li>
            <i> Title:</i>
            Web mining
        </li>
        <li>
            <i> Title:</i>
            Data mining
        </li>
    </ul>
</html>
"""

html_test_2 = """
<html>
    Books of:
    <b>
        Mike Jones
    </b>
    <img src="mike.jpg" />
    <ul>
        <li>
            <i> Title:</i>
            Databases
        </li>
        <li>
            <i> Title:</i>
            HTML Premier
        </li>
        <li>
            <i> Title:</i>
            Javascript
        </li>
    </ul>
</html>
"""

# with open("roadrunner_test.txt", "w", encoding="utf-8") as write_file:
#     write_file.writelines(zazeni_roadrunner(html_test_1, html_test_2))
# with open("roadrunner_test.txt", encoding="windows-1252", errors="ignore") as file:
#     html_roadrunner = file.read()
# soup = BeautifulSoup(html_roadrunner, "html.parser")
# with open("roadrunner_test_pretty.txt", "w", encoding="utf-8") as write_file:
#     write_file.writelines(soup.prettify())

# OVERSTOCK:
# ============================================================
# Branje datoteke
# -------------------------
html_path_1 = r"pa2/input-extraction/WebPages/overstock.com/jewelry01.html"
html_path_2 = r"pa2/input-extraction/WebPages/overstock.com/jewelry02.html"
with open(html_path_1, encoding="windows-1252", errors="ignore") as file:
    html_1 = file.read()
with open(html_path_2, encoding="windows-1252", errors="ignore") as file:
    html_2 = file.read()
# --------------------------
# Zapis na datoteko
# --------------------------
with open("roadrunner_overstock.txt", "w", encoding="utf-8") as write_file:
    write_file.writelines(zazeni_roadrunner(html_1, html_2))
with open("roadrunner_overstock.txt", encoding="windows-1252", errors="ignore") as file:
    html_roadrunner = file.read()
soup = BeautifulSoup(html_roadrunner, "html.parser")
with open("roadrunner_overstock_pretty.txt", "w", encoding="utf-8") as write_file:
    write_file.writelines(soup.prettify())
# --------------------------

# RTVSLO:
# ============================================================
# Branje datoteke
# -------------------------
# html_path_1 = r"pa2/input-extraction/WebPages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
# html_path_2 = r"pa2/input-extraction/WebPages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljs╠îe v razredu - RTVSLO.si.html"
# with open(html_path_1, encoding="utf-8", errors="ignore") as file:
#     html_1 = file.read()
# with open(html_path_2, encoding="utf-8", errors="ignore") as file:
#     html_2 = file.read()
# --------------------------
# Zapis na datoteko
# # --------------------------
# with open("roadrunner_rtvslo.txt", "w", encoding="utf-8") as write_file:
#     write_file.writelines(zazeni_roadrunner(html_1, html_2))
# with open("roadrunner_rtvslo.txt", encoding="utf-8", errors="ignore") as file:
#     html_roadrunner = file.read()
# soup = BeautifulSoup(html_roadrunner, "html.parser")
# with open("roadrunner_rtvslo_pretty.txt", "w", encoding="utf-8") as write_file:
#     write_file.writelines(soup.prettify())
# --------------------------

# IMDB:
# ============================================================
# Branje datoteke
# -------------------------
# html_path_1 = r"pa2/input-extraction/WebPages/imdb.com/imdb1.html"
# html_path_2 = r"pa2/input-extraction/WebPages/imdb.com/imdb2.html"
# with open(html_path_1, encoding="windows-1252", errors="ignore") as file:
#     html_1 = file.read()
# with open(html_path_2, encoding="windows-1252", errors="ignore") as file:
#     html_2 = file.read()
# --------------------------
# Zapis na datoteko
# --------------------------
# with open("roadrunner_imdb.txt", "w", encoding="utf-8") as write_file:
#     write_file.writelines(zazeni_roadrunner(html_1, html_2))
# with open("roadrunner_imdb.txt", encoding="windows-1252", errors="ignore") as file:
#     html_roadrunner = file.read()
# soup = BeautifulSoup(html_roadrunner, "html.parser")
# with open("roadrunner_imdb_pretty.txt", "w", encoding="utf-8") as write_file:
#     write_file.writelines(soup.prettify())
# --------------------------

# soup_1 = BeautifulSoup(html_1, "html.parser")
# soup_2 = BeautifulSoup(html_2, "html.parser")

# html = soup_1.find("html")
# body = html.find("body")
# section1 = html.find("section")
# print(prazno(section1))
# print("\n\n")
# html = soup_2.find("html")
# body = html.find("body")
# section2 = html.find("section")
# print(section2.text)

# print(levenshtein.distance(section1, section2))
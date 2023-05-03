from parsel import Selector
from extraction_xpath import *
import json

# OVERSTOCK:
# ==============================================================================
# TEST - OVERSTOCK1
# -------------------
# html = odpri_datoteko(r"pa2/input-extraction/WebPages/overstock.com/jewelry01.html")
# htmls = []
# htmls.append(html)
# print(json.dumps(overstock(htmls), indent=4, ensure_ascii=False))

# TEST - OVERSTOCK2
# -------------------
# html = odpri_datoteko(r"pa2/input-extraction/WebPages/overstock.com/jewelry02.html")
# htmls = []
# htmls.append(html)
# print(json.dumps(overstock(htmls), indent=4, ensure_ascii=False))

# TEST - XPATH-OV
# -------------------
# with open(r"pa2/input-extraction/WebPages/overstock.com/jewelry02.html", encoding="utf-8", errors='ignore') as dat:
#     text = dat.read()
# sel = Selector(text)
# print(sel.xpath('/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span/text()').getall())

# XPATHS jewelry01/jewwlry02:
# --------------------------
# Title:  '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a/b/text()'
# ListPrice: '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()'
# Price: '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()'
# Saving: '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()' prvi del
# SavingPercent: '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()' drugi del
# Content: '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span/text()'

# ==============================================================================
# ------------------------------------------------------------------------------
# ==============================================================================

# RTVSLO:
# ==============================================================================
# TEST - RTVSLO1
# -------------------
html = odpri_datoteko(r"pa2/input-extraction/WebPages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")
htmls = []
htmls.append(html)
print(json.dumps(rtv_slo(htmls), indent=4, ensure_ascii=False))

# TEST - XPATH-OV
# -------------------
# with open(r"pa2/input-extraction/WebPages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html", encoding="utf-8") as dat:
#     text = dat.read()
# sel = Selector(text)
# print(sel.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]').get())

# XPATHS:
# --------------------------
# Title:  '//*[@id="main-container"]/div[3]/div/header/h1/text()'
# SubTitle: '//*[@id="main-container"]/div[3]/div/header/div[2]/text()'
# Lead: '//*[@id="main-container"]/div[3]/div/header/p/text()'
# Content: '//*[@id="main-container"]/div[3]/div/div[2]/article' tu nevem a potrebujemo tudi slike
# Author: '//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()'
# PublishedTime: '//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]' treba je se strip()-at

# ==============================================================================
# ------------------------------------------------------------------------------
# ==============================================================================

# IMDB:
# ==============================================================================
# TEST - IMDB1
# -------------------
# html = odpri_datoteko(r"pa2/input-extraction/WebPages/imdb.com/imdb1.html")
# htmls = []
# htmls.append(html)
# print(json.dumps(imdb(htmls), indent=4, ensure_ascii=False))

# TEST - IMDB2
# -------------------
# html = odpri_datoteko(r"pa2/input-extraction/WebPages/imdb.com/imdb2.html")
# htmls = []
# htmls.append(html)
# print(json.dumps(imdb(htmls), indent=4, ensure_ascii=False))

# TEST - XPATH-OV
# -------------------
# with open(r"pa2/input-extraction/WebPages/imdb.com/imdb1.html", encoding="utf-8") as dat:
#     text = dat.read()
# sel = Selector(text)
# print(sel.xpath('//*[@id="main"]/div/div[3]/div/div/div[3]/p[2]/text()').getall())

# XPATHS:
# --------------------------
# Title:  '//*[@id="main"]/div/div[3]/div/div/div[3]/h3/a/text()'
# Year: '//*[@id="main"]/div/div[3]/div/div/div[3]/h3/span[2]/text()'
# Runtime: '//*[@id="main"]/div/div[3]/div/div/div[3]/p[1]/span[@class="runtime"]/text()'
# Genre: '//*[@id="main"]/div/div[3]/div/div/div[3]/p[1]/span[@class="genre"]/text()'
# Rating: '//*[@id="main"]/div/div[3]/div/div/div[3]/div/div[1]/strong/text()'
# Content: '//*[@id="main"]/div/div[3]/div/div/div[3]/p[2]/text()'

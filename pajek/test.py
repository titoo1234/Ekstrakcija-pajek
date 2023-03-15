import threading
import psycopg2
from selenium.webdriver.common.by import By
import pathlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
#from urlparse import urljoin
import requests

pot = pathlib.Path().absolute()
WEB_DRIVER_LOCATION = str(pot) + "\..\chromedriver.exe"
lastnosti = Options()
lastnosti.add_argument("--headless")
vmesnik = webdriver.Chrome(WEB_DRIVER_LOCATION, options=lastnosti)
#conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
#vmesnik.get("http://gov.si/robots.txt")
link = "http://evem.gov.si//robots.txt"
domena = urlparse(link).netloc
print(domena)
dolzina_domene = len(domena)
for i in range(len(link)):
    if link[i:(i+dolzina_domene)] == domena:
        j = i + dolzina_domene

c = link[:j] + "/robots.txt"
print(c)

vmesnik.get(link)
html_robot = vmesnik.page_source
print(html_robot)
sitemap = html_robot.split("Sitemap:")[1].split("\n")[0].strip()
print(sitemap)
#print(domain)
#vmesnik.get(urljoin(domain, "robots.txt"))
#a = "https://" + domain + "/robots.txt"
#print(a)
#vmesnik.get(link)
#print(vmesnik.page_source)
#sitemap = vmesnik.page_source.split("Sitemap:")[1].split("\n")[0].strip()

#print(sitemap)

# cur = conn.cursor()
# cur.execute(f"SELECT * FROM crawldb.page_type")# WHERE domain = '{domain}'")
# a = cur.fetchone()
# print(a)
# cur.close()
#linki = vmesnik.find_elements("xpath", "//*[@href]")
#html = vmesnik.page_source
#print(html)
#t = []
#for i in linki:
#    print(i.get_attribute("src"))
    # a = i.get_attribute("href")
    # if a == "":
    #     continue
    # if a[-1] == "/":
    #     pass
    #     # print(a)
    # else:
    #     t.append(a)

#print(t)
#print(len(t))
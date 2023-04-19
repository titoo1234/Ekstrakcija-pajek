from bs4 import BeautifulSoup
import os

html_path = os.getcwd() +  "/pa2/input-extraction/WebPages/overstock.com/jewelry01.html"
with open(html_path, encoding="windows-1252", errors="ignore") as file:
    html = file.read()
soup = BeautifulSoup(html, "html.parser")
html_tag = soup.find("html")
# print(html_tag.getText())
tag = html_tag.find("body")
tag = tag.find("table")
while True:
    if tag.findChildren() == []:
        print(tag)
        break
    else: tag = tag.findChild()
# print(html_tag.findChildren(recursive=False)[0])

# [print(children) for children in soup.children]
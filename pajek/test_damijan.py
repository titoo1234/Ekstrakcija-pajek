from page import *
from vmesnik import * 
from baza import * 
from robots import * 
from datetime import datetime

vmesnik = Vmesnik()
baza = Baza()
# page = Page("http://gov.si/",vmesnik, baza)

cur = baza.conn.cursor()
poizvedba = "INSERT INTO crawldb.page (site_id, page_type_code, url, http_status_code, accessed_time) VALUES (%s, %s, %s, %s, %s) RETURNING id"
cur.execute(poizvedba, (333, "BINARY", "http://gov.si/nekitajga2.pdf", 200, datetime.now()))
id = cur.fetchone()[0]
print(id)

# print(page.site_id)
# print(page.page_type_code)
# print(page.url)
# print(page.html_content)
# print(page.http_status_code)
# print(page.accessed_time)
# print(page.filename)
# print(page.content_type)
# print(page.data)
# print(page.data_type_code)


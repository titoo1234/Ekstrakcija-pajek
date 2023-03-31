from page import *
from vmesnik import * 
from baza import * 
from robots import * 

vmesnik = Vmesnik()
baza = Baza()
page = Page("http://gov.si/",vmesnik, baza)


print(page.site_id)
print(page.page_type_code)
print(page.url)
print(page.html_content)
print(page.http_status_code)
print(page.accessed_time)
print(page.filename)
print(page.content_type)
print(page.data)
print(page.data_type_code)


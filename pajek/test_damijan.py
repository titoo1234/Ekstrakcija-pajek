from page import *
from vmesnik import * 
from baza import * 
from robots import * 
from datetime import datetime

# vmesnik = Vmesnik()
# baza = Baza()
# page = Page("http://gov.si/",vmesnik, baza)

# cur = baza.conn.cursor()
# poizvedba = "INSERT INTO crawldb.page (site_id, page_type_code, url, http_status_code, accessed_time) VALUES (%s, %s, %s, %s, %s) RETURNING id"
# cur.execute(poizvedba, (333, "BINARY", "http://gov.si/nekitajga2.pdf", 200, datetime.now()))
# id = cur.fetchone()[0]
# print(id)
FORMATI_SLIK = ['.ico', '.cur','.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp','.png','.svg','.apng','.gif']

def nepravilen_url(url):
        """
        metoda preveri url in če nima ustrezne končnice vrne true
        """
        koncnica = vrni_koncnico(url)
        print(koncnica)
        if koncnica != "": 
            # url ima koncnico - ni navaden url
            formati_dat = ["PDF", "DOC", "DOCX", "PPT", "PPTX"]
            formati_dat = list(map(lambda x: "." + x.lower(), formati_dat))# to naredimo, ker imamo opravka s tupli npr. ('PDF',)
            dovoljene_koncnice = FORMATI_SLIK + formati_dat + [".html"]
            print(dovoljene_koncnice)
            if koncnica not in dovoljene_koncnice:
                return True
            return False
        else:
            return False
        
def vrni_koncnico(url):
        tuple = os.path.splitext(url)
        return tuple[1]

print(nepravilen_url("/Users/damijanrandl/Desktop/ISRM/letnik_1/IEPS/projekt/Ekstrakcija-pajek/04_vloga_NAMENSKA_RABA_0.pdf"))

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


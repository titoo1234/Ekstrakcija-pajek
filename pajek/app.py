from vec_nitni_pajek import VecNitniPajek

SEMENSKE_STRANI = ["http://gov.si/",
                   "http://evem.gov.si/",
                   "http://e-uprava.gov.si/",
                   "http://e-prostor.gov.si/"]
ST_PAJKOV = 4
DOMENA = "gov.si"

if __name__ == '__main__':
    semenske_strani = False
    pajek = VecNitniPajek(SEMENSKE_STRANI, ST_PAJKOV, DOMENA, semenske_strani)
    if not semenske_strani:
        pajek.zazeni_pajka()
    pajek.info()  

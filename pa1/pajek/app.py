from vec_nitni_pajek import VecNitniPajek
import sys

SEMENSKE_STRANI = ["http://gov.si/",
                   "http://evem.gov.si/",
                   "http://e-uprava.gov.si/",
                   "http://e-prostor.gov.si/"]
ST_PAJKOV = 4
DOMENA = "gov.si"

if __name__ == '__main__':
    semenske_strani = False
    try:
        ST_PAJKOV = int(sys.argv[1])
        semenske_strani = sys.argv[2]
        if semenske_strani == "T":
            semenske_strani = True
        else:
            semenske_strani = False
    except:
        pass
    pajek = VecNitniPajek(SEMENSKE_STRANI, ST_PAJKOV, DOMENA, semenske_strani)
    if not semenske_strani:
        pajek.zazeni_pajka()
    pajek.info()  

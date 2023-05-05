import extraction_regular_exp
import extraction_automatic
import extraction_xpath
def extraction(metoda):

    if metoda  == 'A':
        extraction_regular_exp.zazeni()
    if metoda  == 'B':
        extraction_xpath.zazeni()
    if metoda  == 'C':
        extraction_automatic.zazeni()
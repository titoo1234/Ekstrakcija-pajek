import os
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from stopwords import stop_words_slovene
from dokument import Dokument
# from baza import Baza

# from nltk.corpus import stopwords
import string
# os.chdir(r'pa3/implementation-indexing')
directory = r'PA3-data'
mape = os.listdir(directory)
try:
    mape.remove('__MACOSX')
except:
    pass

for mapa in mape:
    dir = r'PA3-data/' + mapa
    dokumenti = os.listdir(dir)
    try:
        dokumenti.remove('.DS_Store')
    except:
        pass

    for dokument in dokumenti:
        pot = dir + '/' +dokument
        dokument = Dokument(dokument, pot)
        print(dokument.tokens)
        break
    break



    


    





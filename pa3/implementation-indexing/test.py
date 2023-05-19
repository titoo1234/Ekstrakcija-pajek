import os
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from stopwords import stop_words_slovene
# from baza import Baza

# from nltk.corpus import stopwords
import string
os.chdir(r'pa3\implementation-indexing')
directory = r'PA3-data'
mape = os.listdir(directory)
mape.remove('__MACOSX')

for mapa in mape:
    dir = r'PA3-data/' + mapa
    dokumenti = os.listdir(dir)
    dokumenti.remove('.DS_Store')

    for dokument in dokumenti:
        pot = dir + '/' +dokument
        with open(pot,'r',encoding='utf-8') as file:
            tekst = BeautifulSoup(file.read(),'html.parser')
            besedilo = tekst.get_text()
            tokens = word_tokenize(besedilo,language='slovene')
            # stopword_list = stopwords.words('slovene')
            filtered_tokens = [token for token in tokens if token.lower() not in stop_words_slovene]
            filtered_tokens = [token for token in filtered_tokens if token not in string.punctuation]
            # Baza.dodaj_dokument(dokument,text)
            print(filtered_tokens)
        break
    break



    


    





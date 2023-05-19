import sqlite3
from beseda import Beseda
class Baza():
    def __init__(self):
        self.conn = sqlite3.connect('inverted-index.db')


    def dodaj_besedo_v_bazo(self,beseda):
        poizvedba = '''INSERT into Posting (word, documentName,frequency,indexes) values (?,?,?,?)'''
        cursor = self.conn.cursor()
        cursor.execute(poizvedba,[beseda.beseda,beseda.dokument,beseda.frekvenca,beseda.indeks])
        cursor.close()


    def preveri_besedo(self,beseda):
        poizvedba = '''SELECT count(*) from IndexWord where word = ?'''
        cursor = self.conn.cursor()
        cursor.execute(poizvedba,[beseda.beseda])
        cursor.close()
        return cursor.fetchone() == 1
    
    def dodaj_besedo_v_index_word(self,beseda):
        poizvedba = '''INSERT into IndexWord values (?,)'''
        cursor = self.conn.cursor()
        cursor.execute(poizvedba,[beseda.beseda])
        cursor.close()
    

    def dodaj_dokument(self,dokument,text):
        poizvedba = '''INSERT into Document values (?,?)'''
        cursor = self.conn.cursor()
        cursor.execute(poizvedba,[dokument,text])
        cursor.close()

        


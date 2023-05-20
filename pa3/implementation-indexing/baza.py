import sqlite3
# from beseda import Beseda
class Baza():
    def __init__(self):
        self.conn = sqlite3.connect('inverted-index.db',isolation_level=None)
        

    def dodaj_besedo_v_bazo(self,beseda):
        poizvedba = '''INSERT into Posting (word, documentName,frequency,indexes) values (?,?,?,?)'''
        cursor = self.conn.cursor()
        cursor.execute(poizvedba,(beseda.beseda.lower(),beseda.dokument.ime,beseda.frekvenca,beseda.indeks))
        cursor.close()

    def preveri_besedo(self,beseda):
        poizvedba = '''SELECT count(*) from IndexWord where word = ?'''
        cursor = self.conn.cursor()
        cursor.execute(poizvedba,[beseda.beseda.lower()])
        rez = cursor.fetchone()[0]
        return  rez == 1
    
    def dodaj_besedo_v_index_word(self,beseda):
        poizvedba = '''INSERT into IndexWord values (?)'''
        cursor = self.conn.cursor()
        cursor.execute(poizvedba,(beseda.beseda.lower(),))
        cursor.close()
    
    def dodaj_dokument(self,dokument,text,tokens):
        poizvedba = '''INSERT into Document values (?,?,?)'''
        cursor = self.conn.cursor()
        cursor.execute(poizvedba,(dokument,text,tokens))
        cursor.close()

        


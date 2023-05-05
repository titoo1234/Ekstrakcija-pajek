import sys
from extraction import extraction


if __name__ == '__main__':
    semenske_strani = False
    try:
        METODA = sys.argv[1]
        if METODA not in 'ABC':
            METODA = 'A'
    except Exception as e:
        METODA = 'A'
    extraction(METODA)
 

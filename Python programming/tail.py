"""
tail.py stringa [-c] carattere | [-]numero stampa la sottostringa a partire dall'ultima occorrenza
di carattere, opzionalmente specificato con il parametro '-c', ovvero stampa la sottostringa a partire
dalla posizione specificata da numero eventualmente anche negativo
"""

import sys


def lastIndexOf(s, c):
    """
    lastIndexOf(stringa, carattere) restituisce un intero
    nell'intervallo 0 - len(stringa) che corrisponde all'indice dell'ultima
    occorrenza di carattere in stringa. Se il risultato è esattamente 
    len(stringa) allora carattere non è presente in stringa.
    """

    index = s[::-1].find(c)

    if index == -1:
        return len(s)
    else:
        return len(s) - 1 - index


def main():

    if (len(sys.argv) < 3 or len(sys.argv) > 4): 
        print('Argomenti errati\n\nUtilizzo: tail2.py stringa [-c] carattere | [-]numero')
        sys.exit()
    elif len(sys.argv) == 3 and \
        not(sys.argv[2].isdigit() or (sys.argv[2][0]=='-' and sys.argv[2][1::].isdigit())) and \
        len(sys.argv[2])!=1:
        print('Argomenti errati\n\nUtilizzo: tail2.py stringa [-c] carattere | [-]numero')
        sys.exit()
    elif len(sys.argv) == 4 and sys.argv[2]!='-c':
        print('Argomenti errati\n\nUtilizzo: tail2.py stringa [-c] carattere | [-]numero')
        sys.exit()
    else:
        if sys.argv[2].isdigit() or (sys.argv[2][0]=='-' and sys.argv[2][1::].isdigit()):
            index = int(sys.argv[2])
            if index < -len(sys.argv[1]) or index >= len(sys.argv[1]):
                print('Indice specificato fuori dal range\n\n')
                sys.exit()
            else:
                print(sys.argv[1][index::])
        else:
            if sys.argv[2] == '-c':
                position = lastIndexOf(sys.argv[1],sys.argv[3])
            else:
                position = lastIndexOf(sys.argv[1],sys.argv[2])
            if position == len(sys.argv[1]):
                print('Il carattere non è presente nella stringa\n\n')
                sys.exit()
            else:
                print(sys.argv[1][position::])


if __name__ == '__main__':
    main()
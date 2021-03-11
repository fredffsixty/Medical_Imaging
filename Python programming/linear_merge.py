"""
linear_merge <lista 1 separata da ','> <lista 2 separata da ','> [-r]

fonde lista 1 e lista 2 in un'unica lista ordinata senza duplicati e genera
la lista inversa se è specificato l'argomento -r
"""

import sys

def main():

    if (len(sys.argv) < 3 or len(sys.argv) > 4) or \
        (len(sys.argv) == 4 and sys.argv[3]!='-r'):
        print('Errore nei parametri:\nUso corretto: linear_merge.py <lista1> <lista2> [-r]')
    else:
        # crea le due liste dalle stringhe di input separandele con il carattere ','
        l1=sys.argv[1].split(',')
        l2=sys.argv[2].split(',')

        # accoda tutti gli elementi di l2 all'intrerno di l1
        l1.extend(l2)

        # crea un set dagli elementi di l1 (senza ripetizioni)
        # e poi ricrea una lista dal set
        out_list = list(set(l1))

        # se è stato specificato '-r' la lista viene invertita
        if(len(sys.argv)==4):
            out_list.sort(reverse=True)
        else:
            out_list.sort()

        print(out_list)



if __name__ == '__main__':
  main()
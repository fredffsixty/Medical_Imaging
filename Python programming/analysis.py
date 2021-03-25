"""
analysis.py <nome_file> <operatore> [<nome_campo>]

<operatore> ::= max | min | avg | stddev | plot | stat | corr

Gli argomenti max, min, avg e stddev hanno ovvio significato e richiedono 
obbligatoriamente il nome del campo cui si applicano.

L'operatore plot, se seguito da un numero n, stampa le prime n righe 
del file in forma di tabella altrimenti le stampa tutte.

L'operatore stat, se seguito dal nome di un campo, stampa i valori 
di min, max, avg e stddev per quel campo, altrimenti stampa una tabella 
che riporta nelle righe i campi e in colonna i valori di min, max, 
avg e stddev per la riga corrispondente.

Infine, l'operatore corr, rigorosamente senza argomenti, 
genera una tabella quadrata in cui sia le righe che le colonne 
sono i campi del file di input e in ogni cella è riportato 
il valore di correlazione tra il campo in riga e quello in colonna.
"""

import csv
import json
import os.path
import sys
import statistics


def read_data_file(filename, extension):
    """
    read_data_file restituisce una dict di dict contenente
    le righe del file riferito da filename e il set dei nomi di campo

    Es. {'1': {'campo_1': #, 'campo_2': #, ..., 'campo_n': #},
         '2': {'campo_1': #, 'campo_2': #, ..., 'campo_n': #},
         ....
         'M': {'campo_1': #, 'campo_2': #, ..., 'campo_n': #}}

         {'campo_1', 'campo_2', ... , 'campo_n'}
    """
    csv.register_dialect('myDialect',
                        delimiter = ',',       # nuovo delimitatore
                        quoting=csv.QUOTE_ALL, # tutti i campi vengono racchiusi da virgolette per omogeneità
                        skipinitialspace=True) # ci sono spazi dopo il delimitatore

    data = {} # creo il dict dei dati vuoto 
    
    with open(filename, 'r', encoding='utf-8') as datafile:
        
        # seleziona la procedura di lettura in base all'estensione
        if extension == '.csv':
            reader = csv.DictReader(datafile, dialect='myDialect')
        else:
            reader = json.load(datafile)
        
        # inizializza i numeri di riga
        i = 1

        for row in reader:
            # solo per la prima riga crea i set dei nomi dei campi
            if i == 1:
                fieldset=set(row.keys())
            
            # crea il dict associato ad ogni riga in base all'estensione
            # nel caso dei file .csv i campi sono stringhe e li riconvertiamo in
            # valori numerici (codice valido per Python >= 3.8)
            if extension == '.csv':
                data[str(i)]=dict(zip(row.keys(),[float(v) for v in row.values()]))
            else:
                data[str(i)]=row
            
            i += 1
    
    return data, fieldset


def plot(data,numlines=None):
    """
    Stampa un forma tabellare i dati in un dict di dict
    """
    
    # funzione interna che stampa la line del titolo ovvero una liea di dati
    def print_line(lineno=None, title=False):
        
        if title:   # linea del titolo: stampa un campo vuoto e poi ogni 
                    # singolo nome di campo in 10 caratteri separati da ' | '
            empty = ''
            print(f'|{empty:^10s}',end='')
            for field in data['1'].keys():
                print(f'|{field:^10s}',end='')
        
        else:       # linea di dati: nel primo campo viene stampato il numero di linea
                    # e poi i valori della linea stessa sempre allineati in 10 caratteri separati da ' | '
            print(f'|{str(lineno):^10s}',end='')
            for val in data[str(lineno)].values():
                print(f'|{val:^10f}',end='')
        print('|')

    def print_hor_rule(numcol):

        # stampa una serie di ' - ' per un numero di carattreri pari al numero
        # di colonne per la larghezza di ogni campo incluso il suo separatore
        for i in range(11*numcol+1):
            print('-',end='')
        print()

    # imposta il numero di linee da stampare in base al valore del parametro numlines
    if numlines == None or numlines > len(data):
        lines = len(data)
    else:
        lines = numlines
    
    #stampa la tabella
    numcol =  len(data['1'].keys())

    print_hor_rule(numcol)
    print_line(title=True)
    print_hor_rule(numcol)

    for i in range(1,lines+1):
        print_line(i)
    
    print_hor_rule(numcol)




def field_values(data,field):
    """
    Estrae i valori nella colonna field di data
    """
    pass


def stat(data):
    """
    Calcola la tabella delle statistiche dalla tabella dei dati
    """
    pass


def corr(data):
    """
    Calcola la tabella delle correlazioni dalla tabella dei dati
    """
    pass


def main():
    try:
        if len(sys.argv) < 3 or len(sys.argv) > 4:
            raise SyntaxError
        else: 
            name, ext = os.path.splitext(sys.argv[1])
            if ext != '.json' and ext != '.csv':
                raise SyntaxError
            else:
                mydata, fieldset = read_data_file(sys.argv[1], ext)
                if sys.argv[2] not in {'max','min','avg','stdev','plot','stat','corr'}:
                    raise SyntaxError
                elif sys.argv[2] in {'max','min','avg','stdev'} and sys.argv[3] not in fieldset:
                    raise SyntaxError
                elif sys.argv[2] == 'plot' and sys.argv[3]:
                    try:
                        numlines = int(sys.argv[3])
                    except ValueError:
                        raise SyntaxError
                elif sys.argv[2] == 'stat' and sys.argv[3] and sys.argv[3] not in fieldset:
                    raise SyntaxError
    except SyntaxError:
        print("Utilizzo: analysis.py <nome_file> <operatore> [<argomento>]")
    else:
        if sys.argv[2] == 'corr':
            correlations = corr(mydata)
            plot(correlations)
        else:
            stats = stat(mydata)
            if sys.argv[2] in {'max','min','avg','stdev'}:
                print(f'{sys.argv[3]}: {stats[sys.argv[3]][sys.argv[2]]}')
            if sys.argv[2] == 'plot':
                if sys.argv[3]:
                    plot(mydata,int(sys.argv[3]))
                else:
                    plot(mydata)
            if sys.argv[2] == 'stat':
                if sys.argv[3]:
                    plot({sys.argv[3]:stats[sys.argv[3]]})
                else:
                    plot(stats)



if __name__ == "__main__":
    main()

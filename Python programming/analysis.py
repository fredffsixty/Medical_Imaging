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
import math
import statistics


def read_data_file(filename, extension):
    """
    read_data_file restituisce una dict di dict contenente
    le righe del file riferito da filename e la lista dei nomi di campo

    Es. {'1': {'campo_1': #, 'campo_2': #, ..., 'campo_n': #},
         '2': {'campo_1': #, 'campo_2': #, ..., 'campo_n': #},
         ....
         'M': {'campo_1': #, 'campo_2': #, ..., 'campo_n': #}}

         ['campo_1', 'campo_2', ... , 'campo_n']
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
            # solo per la prima riga crea la lista dei nomi dei campi
            if i == 1:
                field_list=list(row.keys())
            
            # crea il dict associato ad ogni riga in base all'estensione
            # nel caso dei file .csv i campi sono stringhe e li riconvertiamo in
            # valori numerici (codice valido per Python >= 3.8)
            if extension == '.csv':
                data[str(i)]=dict(zip(row.keys(),[float(v) for v in row.values()]))
            else:
                data[str(i)]=row
            
            i += 1
    
    return data, field_list


def plot(data,numlines=None):
    """
    Stampa un forma tabellare i dati in un dict di dict
    """
    
    # funzione interna che stampa la line del titolo ovvero una liea di dati
    def print_line(field=None, title=False):
        
        if title:   # linea del titolo: stampa un campo vuoto e poi ogni 
                    # singolo nome di campo in 10 caratteri separati da ' | '

            it = iter(data)         # creo un iteratore sulle chiavi dei dati
            first_line = next(it)   # per avere la chiave della prima linea e poi lo cancello
            del it

            empty = ''
            print(f'|{empty:^10s}',end='')
            for field in data[first_line].keys():
                print(f'|{field:^10s}',end='')
            print('|')
    
        elif field != None:        # linea di dati: nel primo campo viene stampato il numero di linea
                                    # e poi i valori della linea stessa sempre allineati in 10 caratteri separati da ' | '
            print(f'|{field:^10s}',end='')
            for val in data[field].values():
                print(f'|{val:^10f}',end='')
            print('|')
        else:
            print()

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
    it = iter(data)         # creo un iteratore sulle chiavi dei dati 
    first_line = next(it)   # per avere la chiave della prima linea e poi lo cancello
    del it

    # stampo sempre una colonna in più del numero dei campi
    numcol =  len(data[first_line].keys())+1

    print_hor_rule(numcol)
    print_line(title=True)
    print_hor_rule(numcol)

    i = 1
    for key in data.keys():
        if i <= lines:
            print_line(key)
            i += 1
        else:
            break

    print_hor_rule(numcol)


def field_values(data,field):
    """
    Estrae i valori nella colonna field di data
    """
    
    column = []     # contiene la lista dei valori di colonna

    for row in data.values():
        column.append(row[field])
    
    return column


def stat(data, fields):
    """
    Calcola la tabella delle statistiche dalla tabella dei dati

    Riceve in ingresso la tabella dei dati e la lista dei nomi di campo

    Restituisce la tabella delle statistiche indicizzata dai nomi di campo
    """
    stats = {}

    for field in fields:
        field_data = field_values(data, field)
        stats[field] = {\
            'max': max(field_data),\
            'min': min(field_data),\
            'avg': statistics.mean(field_data),\
            'stdev': statistics.stdev(field_data)
            }
    
    return stats


def corr(data, fields):
    """
    Calcola la tabella delle correlazioni dalla tabella, per ogni colonna, rapporto tra la covarianza
    delle due colonne fratto il prodotto delle due rispettive deviazioni standard

    Riceve in ingresso la tabella dei dati e una lista con i nomi di campo

    Restituisce la tabella delle correlazioni indicizzata con i nomi di campo sia in riga sia in colonna

    NOTA BENE: reimplementare usando NumPy
    """
    corr = {}

    # strutture dati di appoggio
    data_values = {}
    avg_values = {}

    # lunghezza di una colonna di dati
    size = len(data)

    # estrae le liste dei valori e ne calcola le medie
    # colonna per colonna
    for field in fields:
        field_data = field_values(data, field)
        data_values[field]=field_data
        avg_values[field]=statistics.mean(data_values[field])
    

    # calcola la matrice delle correlazioni
    for field in fields:
        corr[field]={}

    for field in fields:

        # La matrice delle correlazioni è simmetrica e quindi calcoliamo solo
        # la triangolare superiore
        for other_field in fields[fields.index(field):]:
            if other_field == field: # la correlazione di una colonna con se' stessa è unitaria
                corr[field][other_field] = 1.0
            else:
                num=0
                den_sqrt1 = 0
                den_sqrt2 = 0
                for i in range(size):
                    num += (data_values[field][i]-avg_values[field])*\
                        (data_values[other_field][i]-avg_values[other_field]) # calcola la covarianza
                    den_sqrt1 += (data_values[field][i]-avg_values[field])**2 # calcola le due varianze
                    den_sqrt2 += (data_values[other_field][i]-avg_values[other_field])**2
                
                # correlazione = covarianza/(prodotto delle deviazioni standard)
                # calcolata direttamente per i due elementi simmetrici
                corr[field][other_field] = num/(math.sqrt(den_sqrt1)*math.sqrt(den_sqrt2))
                corr[other_field][field] = corr[field][other_field]
    
    return corr
                    

def main():
    try:
        if len(sys.argv) < 3 or len(sys.argv) > 4:
            raise SyntaxError
        else: 
            name, ext = os.path.splitext(sys.argv[1])
            if ext != '.json' and ext != '.csv':
                raise SyntaxError
            else:
                mydata, field_list = read_data_file(sys.argv[1], ext)
                if sys.argv[2] not in {'max','min','avg','stdev','plot','stat','corr'}:
                    raise SyntaxError
                elif sys.argv[2] in {'max','min','avg','stdev'} and sys.argv[3] not in field_list:
                    raise SyntaxError
                elif sys.argv[2] == 'plot' and len(sys.argv) == 4:
                    try:
                        numlines = int(sys.argv[3])
                    except ValueError:
                        raise SyntaxError
                elif sys.argv[2] == 'stat' and len(sys.argv)==4 and sys.argv[3] not in set(field_list):
                    raise SyntaxError
    except SyntaxError:
        print("Utilizzo: analysis.py <nome_file> <operatore> [<argomento>]")
    else:
        if sys.argv[2] == 'corr':
            correlations = corr(mydata, field_list)
            plot(correlations)
        else:
            stats = stat(mydata,field_list)
            if sys.argv[2] in {'max','min','avg','stdev'}:
                print(f'{sys.argv[3]}: {stats[sys.argv[3]][sys.argv[2]]}')
            if sys.argv[2] == 'plot':
                if len(sys.argv) == 4:
                    plot(mydata,numlines)
                else:
                    plot(mydata)
            if sys.argv[2] == 'stat':
                if len(sys.argv) == 4:
                    plot({sys.argv[3]:stats[sys.argv[3]]})
                else:
                    plot(stats)



if __name__ == "__main__":
    main()

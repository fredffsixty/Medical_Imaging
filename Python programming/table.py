"""
Modulo table: implementa una classe Table che gestisce una tabella di dati
attraverso un dict di dict in modo tale da indicizzare ogni elemento
tramite il nome della riga e il nome della colonna
"""
import csv
import json
import os.path
import sys
import math
import statistics


class Table:
    """
    Implementazione della classe delle tabelle: può essere inizializzata da file
    liste di liste, liste di dict o dict di dict
    Fornisce metodi di plot, estrazione di sotto tabelle, aggiunta e cancellazione
    di righe e/o colonne, estrazione di liste di dati riga o colonna
    """

    def __read_data_file(self,filename):
        """
        read_data_file restituisce una dict di dict contenente
        le righe del file riferito da filename e la lista dei nomi di campo

        Es. {'1': {'campo_1': #, 'campo_2': #, ..., 'campo_n': #},
                '2': {'campo_1': #, 'campo_2': #, ..., 'campo_n': #},
                ....
                'M': {'campo_1': #, 'campo_2': #, ..., 'campo_n': #}}

                ['campo_1', 'campo_2', ... , 'campo_n']
        """
        name, ext = os.path.splitext(filename)
        if ext != '.json' and ext != '.csv':
            return ({}, [])

        csv.register_dialect('myDialect',
                            delimiter = ',',       # nuovo delimitatore
                            quoting=csv.QUOTE_ALL, # tutti i campi vengono racchiusi da virgolette per omogeneità
                            skipinitialspace=True) # ci sono spazi dopo il delimitatore

        data = {} # creo il dict dei dati vuoto 

        with open(filename, 'r', encoding='utf-8') as datafile:
            
            # seleziona la procedura di lettura in base all'estensione
            if ext == '.csv':
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
                if ext == '.csv':
                    data[str(i)]=dict(zip(row.keys(),[float(v) for v in row.values()]))
                else:
                    data[str(i)]=row
                
                i += 1

        return data, field_list

    def __init__(self,data_src,rows=None,cols=None):
        """
        Costruttore polimorfo

        Table(nome_file): crea la tabella da un percorso valido di file dati .csv o .json

        Table([[lista riga 1],...,[lista riga n]],rows=None,cols=None): crea la tabella da una lista
        di liste e opzionalmente richiede la lista delle etichette di riga e di colonna; la nomenclatura
        di default è '1','2', ...  per le righe mentre è 'A','B',... per le colonne

        Table([{dict riga 1},...,{dict riga n}],rows=None): crea la tabella da una lista
        di dict e opzionalmente richiede la lista delle etichette di riga

        Table({nome_riga_1:{dict riga 1},...,nome_riga_n:{dict riga n}}): crea la tabella da un dict
        di dict
        """
        super().__init__()

        self._data = {}
        self._fieldlist = []

        if isinstance(data_src,str) and os.path.isfile(data_src):
            self._data, self._fieldlist = self._Table__read_data_file(data_src)
        
        # Lista di liste
        elif isinstance(data_src,list) and isinstance(data_src[0],list):
            if rows is None:
                rows = [str(i) for i in range(1,len(data_src)+1)]

            if cols is None:
                cols = [chr(ord('A')+i) for i in range(len(data_src[0]))]

            for i in range(len(data_src)):
                self._data[rows[i]]=dict(zip(cols,data_src[i]))
            
            self._fieldlist = cols
        

        # Lista di dict
        elif isinstance(data_src,list) and isinstance(data_src[0],dict):
            if rows is None:
                rows = [str(i) for i in range(1,len(data_src)+1)]

            for i in range(len(data_src)):
                self._data[rows[i]]=data_src[i]
            
            self._fieldlist = list(data_src[0].keys())


        # Dict di dict
        elif isinstance(data_src,dict):
            row_list = list(data_src.keys())
            
            if isinstance(data_src[row_list[0]],dict):
                self._data = data_src
                self._fieldlist = list(data_src[row_list[0]].keys())

        # Impostiamo le dimensioni della tabella
        self._height = len(self._data)
        self._width = len(self._fieldlist)

    # definiamo i getter per le strutture dati interne
    @property
    def size(self):
        return (self._height, self._width)
    
    @property
    def fields(self):
        return self._fieldlist
    
    def val(self,row,col):
        """
        Restituisce il valore all'incrocio tra l'etichetta di riga e quella di colonna
        ovvero None in caso di errore nella specifica della riga e/o colonna
        """
        if row in self._data.keys() and col in self._fieldlist:
            return self._data[row][col]
        else:
            return None
    
    def plot(self,numlines=None):
        """
        Stampa un forma tabellare i dati della tabella e opzionalmente può stamaprne solo le prime
        numlines righe
        """
        
        # funzione interna che stampa la line del titolo ovvero una liea di dati
        def print_line(field=None, title=False):
            
            if title:   # linea del titolo: stampa un campo vuoto e poi ogni 
                        # singolo nome di campo in 10 caratteri separati da ' | '

                empty = ''
                print(f'|{empty:^10s}',end='')
                for field in self._fieldlist:
                    print(f'|{field:^10s}',end='')
                print('|')
        
            elif field != None:        # linea di dati: nel primo campo viene stampato il numero di linea
                                        # e poi i valori della linea stessa sempre allineati in 10 caratteri separati da ' | '
                print(f'|{field:^10s}',end='')
                for val in self._data[field].values():
                    print(f'|{val!r:^10}',end='')
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
        if numlines == None or numlines > len(self._data):
            lines = len(self._data)
        else:
            lines = numlines

        #
        # inizia la stampa della tabella
        #

        # stampo sempre una colonna in più del numero dei campi
        numcol =  len(self._fieldlist)+1

        print_hor_rule(numcol)
        print_line(title=True)
        print_hor_rule(numcol)

        i = 1
        for key in self._data.keys():
            if i <= lines:
                print_line(key)
                i += 1
            else:
                break

        print_hor_rule(numcol)

    def __repr__(self):
        self.plot()
        return ''

    def get_column(self,col):
        """
        Estrae in una lista i valori della colonna etichettata con col
        """
        
        column = []     # contiene la lista dei valori di colonna

        if col in self._fieldlist:

            for row in self._data.values():
                column.append(row[col])
        
        return column

    def get_row(self,row):
        """
        Estrae in una lista i valori della riga etichettata con row
        """

        row_data = []     # contiene la lista dei valori di riga

        if row in self._data.keys():
            row_data = list(self._data[row].values())
        
        return row_data

    def add_row(self,data,row_label):
        """
        Aggiunge una riga in fondo con la propria etichetta e ritorna la tabella modificata
        """

        if isinstance(row_label,str) and isinstance(data,list) and len(data) == self._width:
            self._data[row_label] = dict(zip(self._fieldlist,data))
            self._height += 1
        
        return self
    
    def add_column(self,data,col_label):
        """
        Aggiunge una colonna a destra con la propria etichetta e ritorna la tabella modificata
        """

        if isinstance(col_label,str) and isinstance(data,list) and len(data) == self._height:
            i = 0
            for k in self._data.keys():
                self._data[k][col_label]=data[i]
                i += 1
            
            self._width += 1
            self._fieldlist.append(col_label)
        
        return self

    def del_row(self, row):
        """
        Cancella una riga con la propria etichetta e ritorna la tabella modificata
        """

        if isinstance(row,str) and row in self._data.keys():
            del self._data[row]
            self._height -=1
        
        return self
    
    def del_column(self, col):
        """
        Cancella una riga con la propria etichetta e ritorna la tabella modificata
        """

        if isinstance(col,str) and col in self._fieldlist:
            for k in self._data.keys():
                del self._data[k][col]
            
            self._width -=1
            self._fieldlist.pop(self._fieldlist.index(col))
        
        return self

    def sub_table(self, row_list=[], col_list=[]):   
        """
        Restituisce una nuova tabella che contiene solo i valori indicizzati dalle chiavi
        di riga e colonna fornite come argomento.
        Se una delle due liste è vuota allora verrà restituita la sotto tabella con 
        le sole righe/colonne selezionate, prese per intero
        """
        if isinstance(row_list,list) and isinstance(col_list,list) and \
            set(row_list) <= set(self._data.keys()) and set(col_list) <= set(self._fieldlist):

            subTable = Table(self._data) # Nuova tabella copia della tabella corrente

            # usiamo la generazione dinamica delle liste sotto la condizione che il
            # campo non appartenga alla lista di ingresso
            # e gestiamo il caso in cui una sola delle due liste è vuota
            not_in_rl = []
            not_in_cl = []
            
            if row_list != []:
                not_in_rl = [r for r in self._data.keys() if r not in row_list]
            
            if col_list != []:
                not_in_cl = [c for c in self._fieldlist if c not in col_list]

            # Rimuoviamo le righe
            for r in not_in_rl:
                subTable.del_row(r)

            # Rimuoviamo le colonne
            for c in not_in_cl:
                subTable.del_column(c)
            
            return subTable
        
        else:
            return Table([[]])

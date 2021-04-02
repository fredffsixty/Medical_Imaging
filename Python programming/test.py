#!/usr/bin/env python
import sys
sys.path.extend(['/Users/pirrone/src/github repositories/Medical_Imaging/Python programming'])
from table import Table

def main():
    tt=Table('../Data/dati.json')
    print(tt.size, tt.fields)
    st=tt.sub_table(col_list=['Topolino'])
    st.plot()
    print(st.size, st.fields, st.val('2','Topolino'))

if __name__ == '__main__':
  main()
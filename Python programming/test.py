#!/usr/bin/env python
import sys
sys.path.extend(['/Users/pirrone/src/github repositories/Medical_Imaging/Python programming'])
from table import Table

def main():
    tt=Table([[1,True,'Pippo'],[5,True,'Pluto'],[-3,False,'Topolino']],cols=['Qty','Check','Name'],\
      rows=['1st Q','2nd Q','3rd Q'])
    tt.plot()

if __name__ == '__main__':
  main()
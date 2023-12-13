import pandas as pd
import numpy as np
import sys
from datetime import datetime
from more_itertools import collapse
sys.stdout = open('output.txt','w')

inv = pd.read_csv('data/inv.csv')
pnr = pd.read_csv('data/pnr.csv')
sch = pd.read_csv('data/sch.csv')

inv.set_index('InventoryId',inplace=True)
sch.set_index('ScheduleID',inplace=True)
pnr['ind'] = [i for i in range(len(pnr))]
pnr.set_index('RECLOC',inplace=True)

print(pnr.loc['FMGPWR'])
import pandas as pd
import numpy as np
excel_file = pd.ExcelFile(r"C:\IIT Jodhpur\Inter IIT\Tinkering_Lab_Project\data\SCH-ZZ-20231127_213356.xlsx")
f1 = pd.read_excel(excel_file, engine="openpyxl")
# f2

f11 = f1['FLT_NUM']

f21 = f2['FlightNumber']
source = f2['DepartureAirport']
destination = f2['ArrivalAirport']
start_date = f2['StartDate']
end_date = f2['EndDate']
depart_time = f2['DepartureTime']
arr_time = f2['ArrivalTime']

val = {}
dt,at = [],[]
for i in range(start_date):
    dt.append(start_date[i] + " " + depart_time[i])
    at.append(end_date[i] + " " + arr_time[i])
    if f21[i] not in val:
        val[f21[i]] = (start_date[i] + " " + depart_time[i],end_date[i] + " " + arr_time[i])

dt = np.array(dt)
at = np.array(at)

d11 = list(set(list(f11)))
d21 = list(set(list(f21)))

mapping = {}
for i in range(len(d11)):
    mapping[d11[i]] = d21[i]

dep = []
arr = []
for i in range(len(f11)):
    f11[i] = mapping[f11[i]]
    d,a = val[mapping[f11[i]]]
    dep.append(d)
    arr.append(a)

f11['DEP_DTMZ'] = dep
f11['ARR_DTMZ'] = arr

pd.drop(['DEP_DTML','ARR_DTML'], inplace = True)

f11.to_csv('1.csv')


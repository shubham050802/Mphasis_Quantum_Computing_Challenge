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






# Make a general graph structure using class

def get_time_diff(d1,t1,d2,t2):
    format = '%m/%d/%Y %H:%M'
    t1 = datetime.strptime(str(d1)+' '+str(t1),format)
    t2 = datetime.strptime(str(d2)+' '+str(t2),format)
    return (t2-t1).total_seconds()/3600

def print_matrix(matrix):
    for entry in matrix:
        print(entry)



class Graph:

    def __init__(self, vertices):
        self.V = len(vertices)
        # print(vertices)
        self.graph = [[[] for x in range(self.V)] for y in range(self.V)]
        # print(self.graph)
        vertices.sort()
        self.city_mapping = dict(zip(vertices,range(self.V)))
        self.path_city_compatibility = None
        self.path_mapping=None
        
    def add_edge(self, u, v, w):
        u=self.city_mapping[u]
        v=self.city_mapping[v]

        self.graph[u][v]+=[w]

    def find_all_paths_single_pair(self,source,dest,path=[]):
        if(len(path)>4):
            return []
        path=path+[source]
        if(source==dest):
            return [path]
        paths=[]
        for i in range(self.V):
            if(self.graph[source][i]!=[] and i not in path):
                newpaths=self.find_all_paths_single_pair(i,dest,path)
                for newpath in newpaths:
                    if(len(newpath)!=0):
                        paths.append(newpath)
        return paths
    
    def all_city_paths_all_pairs(self):
        all_paths=[[[] for x in range(self.V)] for y in range(self.V)]
        for i in range(self.V):
            for j in range(self.V):
                if(i!=j):
                    paths=self.find_all_paths_single_pair(i,j)
                    all_paths[i][j]=paths

        # print_matrix(all_paths)
        return all_paths
    

    def find_all_flight_paths_all_pairs(self):
        self.path_mapping=[]
        possible_paths_all_pairs=self.all_city_paths_all_pairs()
        for _i,possible_paths_one_pair in enumerate(possible_paths_all_pairs):
            for _j,possible_paths in enumerate(possible_paths_one_pair):
                if(len(possible_paths)>0):
                    for _k,path in enumerate(possible_paths):

                        curr_paths = [[entry] for entry in self.graph[path[0]][path[1]]]
                        temp_paths = []
                        
                        for i in range(2,len(path)):
                            if(len(curr_paths)==0):
                                break
                            available_flights = self.graph[path[i-1]][path[i]]
                            # print(available_flights)
                            temp_paths = []
                            for flight in available_flights:
                                for curr_path in curr_paths:
                                    # print(curr_path)
                                    prev_arrival_time = sch.loc[inv.loc[curr_path[-1]]['ScheduleId']]['ArrivalTime']
                                    prev_arrival_date = inv.loc[curr_path[-1]]['ArrivalDate']
                                    # print(prev_arrival_time,prev_arrival_date)

                                    curr_departure_time = sch.loc[inv.loc[flight]['ScheduleId']]['DepartureTime']  
                                    curr_departure_date = inv.loc[flight]['DepartureDate']

                                    time_diff = get_time_diff(prev_arrival_date,prev_arrival_time,curr_departure_date,curr_departure_time)

                                
                                    if(1<=time_diff<=12):
                                        temp_paths.append(curr_path+[flight])

                            curr_paths = temp_paths
                        
                        curr_path_mapping=[]
                        m=0
                        for path in curr_paths:
                            if(len(path)>0):
                                self.path_mapping.append(path)
                                curr_path_mapping.append(len(self.path_mapping)-1)
                        # print(curr_paths)
                        # print(curr_path_mapping)
                        # print()
                        possible_paths_all_pairs[_i][_j][_k] = curr_path_mapping

                    possible_paths_all_pairs[_i][_j] = list(filter(lambda x: len(x)>0,possible_paths_all_pairs[_i][_j]))
                    possible_paths_all_pairs[_i][_j] = list(collapse(possible_paths_all_pairs[_i][_j]))

        self.path_city_compatibility = possible_paths_all_pairs
        return possible_paths_all_pairs
    

    def gen_path_pnr_compatibility_matrix(self):
        if self.path_city_compatibility is None:
            self.find_all_flight_paths_all_pairs()
        self.path_pnr_compatibility = [[0 for x in range(len(self.path_mapping))] for y in range(len(pnr))]

        for index,row in pnr.iterrows():
            source = self.city_mapping[row['ORIG_CD']]
            dest = self.city_mapping[row['DEST_CD']]

            for path in self.path_city_compatibility[source][dest]:
                self.path_pnr_compatibility[row['ind']][path]=1

        return self.path_pnr_compatibility
        

        
    



    def print_graph(self):
        print_matrix(self.graph)


def main():
    all_cities = list(set(inv['DepartureAirport']).union(set(inv['ArrivalAirport'])))

    g = Graph(all_cities)

    for index,row in inv.iterrows():
        g.add_edge(row['DepartureAirport'],row['ArrivalAirport'],index)


    g.gen_path_pnr_compatibility_matrix()


    



if __name__ == "__main__":
    main()






            








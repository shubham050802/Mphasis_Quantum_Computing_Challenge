import pandas as pd
import numpy as np
import sys
from datetime import datetime
sys.stdout = open('output.txt','w')

inv = pd.read_csv('data/inv.csv')
pnr = pd.read_csv('data/pnr.csv')
sch = pd.read_csv('data/sch.csv')

inv.set_index('InventoryId',inplace=True)
sch.set_index('ScheduleID',inplace=True)




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
        self.mapping = dict(zip(vertices,range(self.V)))
        
    def add_edge(self, u, v, w):
        u=self.mapping[u]
        v=self.mapping[v]

        self.graph[u][v]+=[w]

    def find_all_paths_dfs(self,source,dest,path=[]):
        if(len(path)>4):
            return []
        path=path+[source]
        if(source==dest):
            return [path]
        paths=[]
        for i in range(self.V):
            if(self.graph[source][i]!=[] and i not in path):
                newpaths=self.find_all_paths_dfs(i,dest,path)
                for newpath in newpaths:
                    if(len(newpath)!=0):
                        paths.append(newpath)
        return paths
    
    def all_paths_all_pairs(self):
        all_paths=[[[] for x in range(self.V)] for y in range(self.V)]
        for i in range(self.V):
            for j in range(self.V):
                if(i!=j):
                    paths=self.find_all_paths_dfs(i,j)
                    all_paths[i][j]=paths
        return all_paths
    

    def find_all_flight_paths_all_pairs(self):
        possible_paths_all_pairs=self.all_paths_all_pairs()
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
                        
                        possible_paths_all_pairs[_i][_j][_k] = curr_paths
        return possible_paths_all_pairs


    def print_graph(self):
        print_matrix(self.graph)


def main():
    all_cities = list(set(inv['DepartureAirport']).union(set(inv['ArrivalAirport'])))

    g = Graph(all_cities)

    for index,row in inv.iterrows():
        g.add_edge(row['DepartureAirport'],row['ArrivalAirport'],index)


    print_matrix(g.find_all_flight_paths_all_pairs())



if __name__ == "__main__":
    main()






            







